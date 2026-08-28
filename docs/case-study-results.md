# Modeled case-study results

Generated from the committed scenario assumptions. These are not customer outcomes and do not use negotiated Azure prices.

| Workflow | Deployment | Effective unit cost | Monthly cost | Operating ROI | Risk-adjusted ROI | Decision |
|---|---:|---:|---:|---:|---:|---|
| Customer diligence | Azure | $2.5946 | $908.10 | 85.05× | 165.98× | Promote |
| Customer diligence | On-prem allocation | $9.5791 | $3,352.68 | 22.31× | 44.23× | Promote |
| ISO evidence | Azure | $0.4070 | $732.55 | 75.79× | 193.73× | Promote |
| ISO evidence | On-prem allocation | $0.9697 | $1,745.37 | 31.23× | 80.73× | Promote |
| Network change review | Azure | $0.2536 | $608.53 | 173.67× | 670.60× | Promote |
| Network change review | On-prem allocation | $0.8727 | $2,094.45 | 49.75× | 194.13× | Promote |
| SOC triage | Azure | $0.0507 | $608.88 | 107.11× | 205.65× | Promote |
| SOC triage | On-prem allocation | $0.2036 | $2,443.52 | 25.94× | 50.49× | Promote |

## Interpretation

Azure wins these baseline scenarios because the modeled volumes do not absorb the allocated on-premises capacity floor. That is a scenario result—not a universal cloud conclusion. At sustained high utilization, with sunk hardware and qualified operations already funded, on-premises marginal cost can cross below Azure.

The large ROI values are driven primarily by modeled workflow revenue and captured labor, not compute price. They must be replaced with observed completion rates, actual loaded labor and contract revenue. Risk-adjusted ROI is substantially higher because it includes expected loss avoided; release policy deliberately ignores that uplift and uses operating ROI plus pre-risk net value.

## Required decision packet

Before presenting any result as financially validated:

1. Attach the exact Azure retail or negotiated price snapshot.
2. Reconcile one month of usage receipts to the Azure invoice/export.
3. Reconcile completed units to billed or recognized workflow revenue.
4. Measure human-review and rework time.
5. Calibrate failure probabilities from incidents or a controlled evaluation.
6. Run downside, baseline and upside cases.

