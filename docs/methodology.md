# Methodology and evidence requirements

## Per-workflow evidence

Every production run should emit a signed receipt containing workflow/version, tenant partition, deployment, model/deployment name, input/output tokens, tool calls, retrieval operations, compute duration, observability bytes, human-review time, outcome, revenue unit, policy decision and source price-snapshot identifiers.

## Cloud cost

Use actual invoice exports when available. Retail meters are a reproducible fallback. Never blend reservation, savings-plan, spot and pay-as-you-go rates without recording the term and utilization assumptions.

## On-premises cost

Capacity must be the lower of technical throughput and reliability-adjusted throughput. Include redundancy, idle headroom, planned maintenance and failure replacement. Allocate shared platform labor consistently across workflows.

## Risk

Expected loss is `event probability × impact`. Probability reduction must come from controlled pilots, historic incidents, validation datasets or an explicitly labeled expert estimate. Show risk value separately from booked revenue and captured labor.

## ROI quality levels

1. **Modeled** — explicit assumptions only.
2. **Observed** — trace-derived usage and cycle time.
3. **Financially reconciled** — invoice and contract revenue matched.
4. **Causally validated** — controlled comparison supports the claimed delta.

Release materials must display the current quality level.

