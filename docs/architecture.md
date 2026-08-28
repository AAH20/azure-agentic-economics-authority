# Reference architecture

```mermaid
flowchart LR
  A[LangGraph / Foundry workflow] --> B[Economics trace callback]
  A --> C[Application Insights / OpenTelemetry]
  D[Azure invoice or retail price snapshot] --> E[Cost allocator]
  F[Contracts and workflow revenue] --> G[Value allocator]
  H[Incidents, QA and approvals] --> I[Risk model]
  B --> J[Signed workflow receipt]
  C --> J
  E --> J
  G --> J
  I --> J
  J --> K{Release policy}
  K -->|Promote| L[Azure or on-prem deployment]
  K -->|Block| M[Human remediation / redesign]
```

The architecture separates telemetry collection, financial attribution, risk estimation and release authority. The agent cannot edit its own economics policy or evidence receipt.

