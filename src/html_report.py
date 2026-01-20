import os
from jinja2 import Environment, FileSystemLoader, select_autoescape


def write_html_report(per_config_results, out_dir: str) -> str:
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )
    tpl = env.get_template("report.html")

    top_findings_png = "top_findings.png" if os.path.exists(os.path.join(out_dir, "top_findings.png")) else None
    risk_per_config_png = "risk_per_config.png" if os.path.exists(os.path.join(out_dir, "risk_per_config.png")) else None

    html = tpl.render(
        results=per_config_results,
        top_findings_png=top_findings_png,
        risk_per_config_png=risk_per_config_png,
    )

    out_path = os.path.join(out_dir, "report.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    return out_path
