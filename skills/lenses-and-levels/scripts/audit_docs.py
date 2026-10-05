#!/usr/bin/env python3
"""
Lenses & Levels Architecture Documentation Automated Auditor

Scans markdown and HTML documentation files for compliance with the Lenses & Levels framework:
1. Lens and Level Structure Detection
2. Overview Discipline (Bloat & Centrality Filter check in Level 1)
3. Downward Self-Containment (Upward reference detection in Level 2/3)
4. Cross-Lens Duplication / Content Overlap
5. Living Artifact Anchoring in Level 3
6. Misplaced Content Heuristics (e.g. SQL DDL in System Lens, CI/CD in Runtime Lens)
"""

import os
import sys
import re
import argparse
import json
from pathlib import Path
from collections import defaultdict

KNOWN_LENSES = {
    "system": "System Lens",
    "capability": "Capability Lens",
    "domain": "Domain Lens",
    "data": "Data Lens",
    "integration": "Integration Lens",
    "runtime": "Runtime Lens",
    "deployment": "Deployment Lens",
    "security": "Security Lens",
    "quality_attributes": "Quality Attributes Lens",
    "governance_decision": "Governance & Decision Lens",
    "governance": "Governance & Decision Lens",
    "evolution": "Evolution Lens",
    "ux": "UX & Interaction Lens",
    "organization": "Organization Lens",
    "cost": "Cost Lens",
    "compliance": "Compliance Lens",
}

UPWARD_DEPENDENCY_PATTERNS = [
    r"as (?:described|mentioned|stated|noted|discussed) in (?:level\s*1|the overview|section 1)",
    r"refer to (?:level\s*1|the overview|above) for (?:more|details|context)",
    r"see (?:level\s*1|the overview) above",
    r"as defined (?:earlier|previously|above) in level 1",
    r"review level 1 before",
]

MISPLACED_PATTERNS = [
    {
        "pattern": r"(?i)\b(create\s+table|primary\s+key|foreign\s+key|alter\s+table)\b",
        "expected_lens": "Data Lens",
        "allowed_lenses": ["Data Lens"],
        "reason": "Database DDL and table definitions belong canonically in Data Lens (Level 3)."
    },
    {
        "pattern": r"(?i)\b(terraform|k8s|kubernetes\s+pod|helm\s+chart|cloudformation|dockerfile)\b",
        "expected_lens": "Deployment Lens",
        "allowed_lenses": ["Deployment Lens"],
        "reason": "Infrastructure definitions, Kubernetes manifests, and IaC belong canonically in Deployment Lens."
    },
    {
        "pattern": r"(?i)\b(openapi|swagger\s*2\.0|asyncapi|graphql\s+schema)\b",
        "expected_lens": "Integration Lens",
        "allowed_lenses": ["Integration Lens", "Data Lens"],
        "reason": "API contracts and protocol specifications belong canonically in Integration Lens."
    },
]

def find_docs_files(base_path: Path):
    if base_path.is_file():
        return [base_path]
    files = []
    for ext in ("*.md", "*.markdown", "*.html", "*.htm"):
        for p in base_path.rglob(ext):
            # Skip git and hidden dirs
            if any(part.startswith(".") for part in p.parts):
                continue
            files.append(p)
    return sorted(files)

def parse_markdown_sections(content: str, file_path: Path):
    lines = content.splitlines()
    sections = []
    current_lens = None
    current_level = None
    current_text = []
    start_line = 1

    # Heuristic for lens based on filename
    file_stem = file_path.stem.lower()
    for key, name in KNOWN_LENSES.items():
        if key in file_stem:
            current_lens = name
            break

    heading_regex = re.compile(r"^(#{1,4})\s+(.+)$")
    level_regex = re.compile(r"(?i)level\s*([123])|(overview|map|detail)")

    for idx, line in enumerate(lines, start=1):
        match = heading_regex.match(line)
        if match:
            heading_text = match.group(2).strip()
            # Check if heading names a lens
            h_lower = heading_text.lower()
            for key, name in KNOWN_LENSES.items():
                if key in h_lower or name.lower() in h_lower:
                    if current_text:
                        sections.append({
                            "lens": current_lens or "Unknown Lens",
                            "level": current_level or "Unknown Level",
                            "start_line": start_line,
                            "end_line": idx - 1,
                            "text": "\n".join(current_text),
                            "file": str(file_path),
                        })
                        current_text = []
                    current_lens = name
                    current_level = None
                    start_line = idx

            # Check if heading names a level
            lvl_match = level_regex.search(h_lower)
            if lvl_match:
                if current_text:
                    sections.append({
                        "lens": current_lens or "Unknown Lens",
                        "level": current_level or "Unknown Level",
                        "start_line": start_line,
                        "end_line": idx - 1,
                        "text": "\n".join(current_text),
                        "file": str(file_path),
                    })
                    current_text = []
                start_line = idx
                if lvl_match.group(1):
                    current_level = f"Level {lvl_match.group(1)}"
                else:
                    mapped = {"overview": "Level 1", "map": "Level 2", "detail": "Level 3"}
                    current_level = mapped.get(lvl_match.group(2).lower(), "Unknown Level")
        current_text.append(line)

    if current_text:
        sections.append({
            "lens": current_lens or "Unknown Lens",
            "level": current_level or "Unknown Level",
            "start_line": start_line,
            "end_line": len(lines),
            "text": "\n".join(current_text),
            "file": str(file_path),
        })

    return sections

def audit_section(section):
    findings = []
    text = section["text"]
    words = text.split()
    word_count = len(words)
    level = section["level"]
    lens = section["lens"]
    file_info = f"{section['file']}#L{section['start_line']}-L{section['end_line']}"

    # 1. Overview Discipline Check
    if level == "Level 1":
        if word_count > 450:
            findings.append({
                "type": "Overview Bloat",
                "severity": "Warning",
                "location": file_info,
                "lens": lens,
                "level": level,
                "message": f"Level 1 section has {word_count} words. Overview should be concise narrative under ~300 words. Consider demoting non-central items."
            })
        if "```sql" in text or "```terraform" in text or "```yaml" in text:
            findings.append({
                "type": "Overview Bloat",
                "severity": "Major",
                "location": file_info,
                "lens": lens,
                "level": level,
                "message": "Level 1 contains detailed code or configuration blocks. Push concrete schemas and configs to Level 2 or Level 3."
            })

    # 2. Downward Self-Containment (Upward Traps) in Level 2 / Level 3
    if level in ("Level 2", "Level 3"):
        for pattern in UPWARD_DEPENDENCY_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                findings.append({
                    "type": "Upward Dependency",
                    "severity": "Major",
                    "location": file_info,
                    "lens": lens,
                    "level": level,
                    "message": f"Detected upward dependency phrase: '{match.group(0)}'. Lower levels must be self-contained so readers do not have to jump back up to Level 1."
                })

    # 3. Living Artifact check for Level 3
    if level == "Level 3":
        has_link = bool(re.search(r"\[.+?\]\(.+?\)|https?://", text))
        has_code = "```" in text or "<code>" in text
        if not (has_link or has_code) and word_count > 50:
            findings.append({
                "type": "Living Artifact Gap",
                "severity": "Minor",
                "location": file_info,
                "lens": lens,
                "level": level,
                "message": "Level 3 (Detail) lacks links or code references to living artifacts (e.g. OpenAPI specs, IaC code, migrations, ADRs)."
            })

    # 4. Misplaced content heuristics
    for rule in MISPLACED_PATTERNS:
        if lens not in rule["allowed_lenses"]:
            match = re.search(rule["pattern"], text)
            if match:
                findings.append({
                    "type": "Misplaced Lens Content",
                    "severity": "Major",
                    "location": file_info,
                    "lens": lens,
                    "level": level,
                    "message": f"Detected '{match.group(0)}' in {lens}. {rule['reason']}"
                })

    return findings

def check_cross_lens_duplication(sections):
    findings = []
    # Compare sections with similar text
    token_sets = []
    for s in sections:
        clean = re.sub(r"[^\w\s]", "", s["text"].lower())
        tokens = set(word for word in clean.split() if len(word) > 4)
        token_sets.append((s, tokens))

    n = len(token_sets)
    for i in range(n):
        s1, t1 = token_sets[i]
        if not t1 or s1["lens"] == "Unknown Lens":
            continue
        for j in range(i + 1, n):
            s2, t2 = token_sets[j]
            if s1["lens"] == s2["lens"]:
                continue
            if not t2:
                continue
            intersection = t1.intersection(t2)
            smaller_len = min(len(t1), len(t2))
            if smaller_len > 15 and len(intersection) / smaller_len > 0.65:
                findings.append({
                    "type": "Cross-Lens Duplication",
                    "severity": "Major",
                    "location": f"{s1['file']} ({s1['lens']}) <-> {s2['file']} ({s2['lens']})",
                    "lens": f"{s1['lens']} & {s2['lens']}",
                    "level": f"{s1['level']} & {s2['level']}",
                    "message": f"High textual overlap detected between {s1['lens']} and {s2['lens']}. Choose a canonical owner and use references instead of duplicate copy."
                })
    return findings

def main():
    parser = argparse.ArgumentParser(description="Lenses & Levels Architecture Documentation Auditor")
    parser.add_argument("--path", "-p", default=".", help="File or directory path to audit")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    target = Path(args.path).resolve()
    if not target.exists():
        print(f"Error: Target path '{target}' does not exist.", file=sys.stderr)
        sys.exit(1)

    files = find_docs_files(target)
    if not files:
        print(f"No documentation files (*.md, *.html) found in {target}")
        sys.exit(0)

    all_sections = []
    all_findings = []

    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            sections = parse_markdown_sections(content, f)
            all_sections.extend(sections)
            for s in sections:
                findings = audit_section(s)
                all_findings.extend(findings)
        except Exception as e:
            all_findings.append({
                "type": "Read Error",
                "severity": "Critical",
                "location": str(f),
                "lens": "None",
                "level": "None",
                "message": f"Failed to parse file: {e}"
            })

    # Check duplication
    duplication_findings = check_cross_lens_duplication(all_sections)
    all_findings.extend(duplication_findings)

    if args.json:
        output = {
            "target": str(target),
            "files_scanned": [str(f) for f in files],
            "total_sections": len(all_sections),
            "findings_count": len(all_findings),
            "findings": all_findings,
        }
        print(json.dumps(output, indent=2))
        return

    # Text report
    print("\n" + "="*70)
    print(" 🔍 LENSES & LEVELS DOCUMENTATION AUDIT REPORT")
    print("="*70)
    print(f"Target Path     : {target}")
    print(f"Files Scanned   : {len(files)}")
    print(f"Sections Audited: {len(all_sections)}")
    print(f"Issues Detected : {len(all_findings)}")
    print("-"*70)

    if not all_findings:
        print("✅ Excellent! No structural violations or anti-patterns detected.")
        print("   Documentation adheres to Lenses & Levels invariants.")
        print("="*70 + "\n")
        return

    # Group findings by type
    by_type = defaultdict(list)
    for f in all_findings:
        by_type[f["type"]].append(f)

    for issue_type, issues in by_type.items():
        print(f"\n📌 {issue_type} ({len(issues)} occurrences):")
        for idx, item in enumerate(issues, 1):
            sev_icon = "🔴" if item["severity"] in ("Critical", "Major") else "🟡"
            print(f"  {sev_icon} [{item['severity']}] {item['location']}")
            print(f"     Lens: {item['lens']} | Level: {item['level']}")
            print(f"     Details: {item['message']}")

    print("\n" + "="*70)
    print(" 💡 Recommended Action: Review findings and restructure using SKILL.md")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
