from typing import List
from .matcher import Finding

def compute_risk_score(findings: List[Finding]) -> int:
    total = sum(f.severity for f in findings)

    # 80 severity -> 100 risk
    risk = round((total / 80) * 100)

    return max(0, min(100, risk))

