import re
from dataclasses import dataclass
from typing import Any, Dict, List

import yaml
from .parser import ConfigLine


@dataclass
class Finding:
    rule_id: str
    title: str
    severity: int
    description: str
    recommendation: str
    evidence: List[Dict[str, Any]]  # [{"lineno":..., "line":...}, ...]


def load_rules(rules_path: str) -> List[Dict[str, Any]]:
    with open(rules_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, list):
        raise ValueError("rules.yaml must be a list of rule objects")
    return data


def match_rules(lines: List[ConfigLine], rules: List[Dict[str, Any]]) -> List[Finding]:
    findings: List[Finding] = []

    for rule in rules:
        rule_id = rule["id"]
        title = rule["title"]
        rule_type = rule["type"]  # presence / absence
        regex = rule["regex"]
        severity = int(rule["severity"])
        description = rule.get("description", "")
        recommendation = rule.get("recommendation", "")

        pattern = re.compile(regex)

        matches = []
        for cl in lines:
            if pattern.search(cl.line):
                matches.append({"lineno": cl.lineno, "line": cl.line})

        if rule_type == "presence":
            if matches:
                findings.append(
                    Finding(
                        rule_id=rule_id,
                        title=title,
                        severity=severity,
                        description=description,
                        recommendation=recommendation,
                        evidence=matches[:10],  # kanıtı çok şişirmeyelim
                    )
                )

        elif rule_type == "absence":
            if not matches:
                findings.append(
                    Finding(
                        rule_id=rule_id,
                        title=title,
                        severity=severity,
                        description=description,
                        recommendation=recommendation,
                        evidence=[],
                    )
                )
        else:
            raise ValueError(f"Unknown rule type: {rule_type} for {rule_id}")

    return findings
