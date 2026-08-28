from __future__ import annotations

from typing import Any

from .models import CloudUnitCost, EconomicsResult, ModelUsage, OnPremTco, ValueModel


def _cloud(config: dict[str, Any]) -> CloudUnitCost:
    model = config["model"]
    return CloudUnitCost(
        model=ModelUsage(**model),
        compute_usd=config.get("compute_usd", 0),
        retrieval_usd=config.get("retrieval_usd", 0),
        observability_usd=config.get("observability_usd", 0),
        storage_usd=config.get("storage_usd", 0),
        network_usd=config.get("network_usd", 0),
        tool_usd=config.get("tool_usd", 0),
        monthly_fixed_usd=config.get("monthly_fixed_usd", 0),
    )


def _decision(roi: float, monthly_net: float, risk_reduction: float, policy: dict[str, Any]) -> tuple[str, tuple[str, ...]]:
    reasons: list[str] = []
    if monthly_net < policy.get("minimum_monthly_net_value", 0):
        reasons.append("monthly net value is below policy")
    if roi < policy.get("minimum_roi", 0):
        reasons.append("ROI is below policy")
    if risk_reduction < policy.get("minimum_risk_reduction", 0):
        reasons.append("risk reduction is below policy")
    if reasons:
        return "BLOCK", tuple(reasons)
    return "PROMOTE", ("economic and risk policies satisfied",)


def evaluate_scenario(config: dict[str, Any], deployment: str) -> EconomicsResult:
    value = ValueModel(**config["value"])
    upfront = float(config.get("upfront_change_cost", 0))
    if deployment == "azure":
        cloud = _cloud(config["azure"])
        monthly_cost = cloud.total * value.volume_per_month + cloud.monthly_fixed_usd
        unit_cost = monthly_cost / value.volume_per_month
        assumptions = config["azure"]
    elif deployment == "on_prem":
        tco_config = {k: v for k, v in config["on_prem"].items() if k != "allocation_floor_fraction"}
        tco = OnPremTco(**tco_config)
        allocation_floor = tco.monthly_cost * float(config["on_prem"].get("allocation_floor_fraction", 1))
        monthly_cost = max(tco.unit_cost * value.volume_per_month, allocation_floor)
        unit_cost = monthly_cost / value.volume_per_month
        assumptions = config["on_prem"] | {"calculated_monthly_tco": tco.monthly_cost, "allocated_monthly_floor": allocation_floor}
    else:
        raise ValueError("deployment must be 'azure' or 'on_prem'")

    monthly_net_before_risk = value.monthly_revenue + value.monthly_labor_value - monthly_cost
    monthly_net = monthly_net_before_risk + value.monthly_risk_value
    operating_roi = monthly_net_before_risk / monthly_cost if monthly_cost else float("inf")
    risk_adjusted_roi = monthly_net / monthly_cost if monthly_cost else float("inf")
    payback = upfront / monthly_net if upfront and monthly_net > 0 else (0.0 if not upfront else None)
    margin = (value.monthly_revenue - monthly_cost) / value.monthly_revenue if value.monthly_revenue else None
    risk_delta = value.baseline_failure_probability - value.controlled_failure_probability
    decision, reasons = _decision(operating_roi, monthly_net_before_risk, risk_delta, config.get("release_policy", {}))
    return EconomicsResult(
        scenario=config["name"], deployment=deployment, unit_cost=unit_cost,
        monthly_cost=monthly_cost, monthly_revenue=value.monthly_revenue,
        monthly_labor_value=value.monthly_labor_value, monthly_risk_value=value.monthly_risk_value,
        monthly_net_value_before_risk=monthly_net_before_risk, monthly_net_value=monthly_net,
        operating_roi=operating_roi, risk_adjusted_roi=risk_adjusted_roi,
        payback_months=payback, gross_margin=margin,
        release_decision=decision, decision_reasons=reasons, assumptions=assumptions,
    )
