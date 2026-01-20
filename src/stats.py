import os
import pandas as pd
import matplotlib.pyplot as plt


def generate_stats_and_charts(per_config_results, out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)

    # Flatten findings
    rows = []
    for r in per_config_results:
        for f in r["findings"]:
            rows.append({
                "config": r["config"],
                "risk_score": r["risk_score"],
                "rule_id": f["rule_id"],
                "title": f["title"],
                "severity": f["severity"],
            })

    if not rows:
        return

    df = pd.DataFrame(rows)

    # Top findings
    top = df["rule_id"].value_counts().head(10)
    top.to_csv(os.path.join(out_dir, "top_findings.csv"), header=["count"])

    # Chart: top findings bar
    plt.figure()
    top.plot(kind="bar")
    plt.title("Top Findings (Rule IDs)")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "top_findings.png"))
    plt.close()

    # Chart: risk per config
    risk_df = df.groupby("config")["risk_score"].max().sort_values(ascending=False)
    plt.figure()
    risk_df.plot(kind="bar")
    plt.title("Risk Score per Config")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "risk_per_config.png"))
    plt.close()
