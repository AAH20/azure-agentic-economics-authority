# Azure Agentic Economics Authority

An executable control plane that answers one question before an agentic workflow is promoted:

> Does this workflow create enough revenue, labor capacity and risk reduction to justify its fully loaded cost—and is Azure or self-hosted infrastructure the better decision at this volume?

The repository combines:

- Microsoft Foundry / LangGraph-compatible usage receipts;
- timestamped Azure Retail Prices API snapshots;
- on-premises total cost of ownership, including utilization and staffing;
- unit revenue, labor value and expected-loss reduction;
- ROI, gross margin, payback and release-policy gates;
- Bicep and Terraform observability foundations;
- four modeled case studies with every assumption exposed.

## Why it matters

Agent prototypes report token cost. Enterprise operators need the entire economic contract: model, compute, tools, retrieval, logs, storage, network, human review, operations, capex, power, risk and revenue. This project turns those variables into an auditable release decision.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
agent-econ evaluate scenarios/soc-triage.json --deployment both
python -m unittest discover -s tests -v
```

Capture exact retail meters at decision time:

```bash
agent-econ snapshot-prices \
  --filter "serviceName eq 'Virtual Machines' and armRegionName eq 'eastus' and armSkuName eq 'Standard_D4s_v5' and priceType eq 'Consumption'" \
  --output artifacts/prices/d4s-v5-eastus.json
```

## ROI contract

For each workflow and deployment:

```text
monthly benefit = workflow revenue + captured labor value + expected loss avoided
monthly net value = monthly benefit - fully loaded monthly operating cost
operating ROI = (revenue + captured labor value - cost) / cost
risk-adjusted ROI = (revenue + captured labor value + expected loss avoided - cost) / cost
payback months = upfront implementation cost / monthly net value
gross margin = (workflow revenue - monthly operating cost) / workflow revenue
```

Expected loss avoided is not booked revenue. Release policy uses operating ROI and pre-risk net value; risk-adjusted ROI is reported separately so optimistic incident assumptions cannot authorize a weak workflow.

## Case studies

| Workflow | Economic unit | Primary value | Critical risk gate |
|---|---|---|---|
| SOC triage | alert | analyst capacity + MDR revenue | missed/escalated incident |
| ISO evidence | evidence item | audit-readiness retainer | unsupported control claim |
| Customer diligence | approved answer | sales velocity + advisory revenue | fabricated/stale evidence |
| Network change review | proposed change | engineering capacity + outage loss avoided | unsafe autonomous action |

All numbers are modeled inputs, not claimed customer outcomes. Replace every assumption with measured traces, contracts, loaded labor rates, incident data and actual Azure price snapshots before making an investment decision.

See the reproducible baseline comparison in [`docs/case-study-results.md`](docs/case-study-results.md).

## `langchain-azure-ai` integration

`EconomicsTraceHandler` implements a lightweight LangChain callback surface for tokens, tool calls and node duration. Use it alongside `langchain-azure-ai` Application Insights tracing. The Azure package supports Foundry models, Agent Service nodes, LangGraph hosting, tools, content safety, AI Search and OpenTelemetry; this project supplies the missing economic and risk receipt.

```python
from agentic_economics.tracing import EconomicsTraceHandler

economics = EconomicsTraceHandler(workflow="customer-diligence")
result = graph.invoke(payload, config={"callbacks": [economics]})
receipt = economics.receipt()
```

Keep content recording disabled by default in production traces. Price, evidence and decision receipts should contain identifiers and aggregates—not prompts, secrets or customer evidence bodies.

## Decision discipline

- Azure retail prices are public list prices, not negotiated invoice prices.
- Foundry Agent Service charges flow through model inference and enabled tools; agent orchestration itself has no separate quota according to Microsoft’s FAQ.
- On-premises is not “free after capex.” The model includes depreciation, residual value, power, PUE, maintenance, rack/network, operations labor and practical capacity.
- A lower unit cost does not authorize a higher-risk deployment.
- Human approval remains mandatory for material security, compliance, financial and customer-facing actions.

## Sources

- [langchain-azure](https://github.com/langchain-ai/langchain-azure)
- [Azure Retail Prices API](https://learn.microsoft.com/rest/api/cost-management/retail-prices/azure-retail-prices)
- [Foundry Agent Service FAQ](https://learn.microsoft.com/azure/foundry/agents/faq)
- [Azure Cost Management automation](https://learn.microsoft.com/azure/cost-management-billing/automate/automation-overview)
- [Microsoft Sentinel pricing](https://azure.microsoft.com/pricing/details/microsoft-sentinel/)
