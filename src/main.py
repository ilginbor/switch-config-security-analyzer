import os
from glob import glob
from typing import List

from .parser import parse_config_file
from .matcher import load_rules, match_rules
from .scorer import compute_risk_score
from .report import findings_to_dict, write_outputs

from .stats import generate_stats_and_charts
from .html_report import write_html_report


def detect_vendor(lines) -> str:
    """
    Vendor detection that works with either:
    - List[str]
    - List[ConfigLine] (objects with .text or .line or similar)
    """
    extracted = []
    for item in lines:
        # If it's already a string
        if isinstance(item, str):
            extracted.append(item)
            continue

        # If it's a dataclass/object from parser (ConfigLine)
        # Try common attribute names safely
        for attr in ("text", "line", "raw"):
            if hasattr(item, attr):
                val = getattr(item, attr)
                if isinstance(val, str):
                    extracted.append(val)
                    break
        else:
            # Fallback: stringify object (worst case)
            extracted.append(str(item))

    text = "\n".join(extracted).lower()

    huawei_markers = [
        "sysname ",
        "stelnet",
        "info-center",
        "undo ",
        "snmp-agent",
        "ntp-service",
    ]
    if any(m in text for m in huawei_markers):
        return "huawei"

    return "cisco"


    # Huawei hints
    huawei_markers = [
        "sysname ",
        "stelnet",
        "info-center",
        "undo ",
        "snmp-agent",
        "ntp-service",
    ]
    if any(m in text for m in huawei_markers):
        return "huawei"

    # Default to Cisco-like
    return "cisco"


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    configs_dir = os.path.join(base_dir, "configs")
    rules_dir = os.path.join(base_dir, "rules")
    out_dir = os.path.join(base_dir, "out")

    # Config files
    config_files = sorted(glob(os.path.join(configs_dir, "*")))
    if not config_files:
        print("configs/ klasöründe dosya yok. Örn: configs/cisco1.cfg, configs/huawei1.cfg ekleyin.")
        return

    per_config_results = []

    for path in config_files:
        name = os.path.basename(path)
        lines = parse_config_file(path)

        vendor = detect_vendor(lines)

        # Vendor-specific rules
        if vendor == "huawei":
            rules_path = os.path.join(rules_dir, "huawei.yaml")
        else:
            rules_path = os.path.join(rules_dir, "cisco.yaml")

        rules = load_rules(rules_path)

        findings = match_rules(lines, rules)
        risk_score = compute_risk_score(findings)

        per_config_results.append(
            {
                "config": name,
                "vendor": vendor,
                "rules_file": os.path.basename(rules_path),
                "risk_score": risk_score,
                "findings": findings_to_dict(findings),
            }
        )

        print(f"\n=== {name} ===")
        print(f"Vendor: {vendor} | Rules: {os.path.basename(rules_path)}")
        print(f"Risk score: {risk_score}/100 | Findings: {len(findings)}")
        for f in findings:
            print(f"- [{f.severity}/10] {f.title} ({f.rule_id})")

    # Write outputs (json/csv)
    write_outputs(out_dir, per_config_results)

    # Generate charts + HTML report
    generate_stats_and_charts(per_config_results, out_dir)
    report_path = write_html_report(per_config_results, out_dir)

    print(f"\nÇıktılar yazıldı: {out_dir}")
    print("- findings.json (detay)")
    print("- summary.csv (özet)")
    print("- top_findings.csv (en sık bulgular)")
    print(f"- report.html (HTML rapor): {report_path}")
    print("- top_findings.png (grafik)")
    print("- risk_per_config.png (grafik)")


if __name__ == "__main__":
    main()
