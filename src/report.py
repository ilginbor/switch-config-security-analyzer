import json
import os
from typing import Any, Dict, List

import pandas as pd

from .matcher import Finding


def findings_to_dict(findings: List[Finding]) -> List[Dict[str, Any]]:
    out = []
    for f in findings:
        out.append(
            {
                "rule_id": f.rule_id,
                "title": f.title,
                "severity": f.severity,
                "description": f.description,
                "recommendation": f.recommendation,
                "evidence": f.evidence,
            }
        )
    return out


def write_outputs(
    out_dir: str,
    per_config_results: List[Dict[str, Any]],
) -> None:
    os.makedirs(out_dir, exist_ok=True)

    # 1) JSON (tüm detay)
    json_path = os.path.join(out_dir, "findings.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(per_config_results, f, ensure_ascii=False, indent=2)

    # 2) CSV (özet)
    rows = []
    for r in per_config_results:
        rows.append(
            {
                "config": r["config"],
                "risk_score": r["risk_score"],
                "finding_count": len(r["findings"]),
            }
        )
    df = pd.DataFrame(rows).sort_values(by="risk_score", ascending=False)
    csv_path = os.path.join(out_dir, "summary.csv")
    df.to_csv(csv_path, index=False)

    # 3) Top findings istatistiği
    all_findings = []
    for r in per_config_results:
        for f in r["findings"]:
            all_findings.append({"config": r["config"], "rule_id": f["rule_id"], "severity": f["severity"]})

    if all_findings:
        df2 = pd.DataFrame(all_findings)
        top = df2["rule_id"].value_counts().head(10)
        top_path = os.path.join(out_dir, "top_findings.csv")
        top.to_csv(top_path, header=["count"])
