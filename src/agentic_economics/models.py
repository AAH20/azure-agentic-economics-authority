from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ModelUsage:
    input_tokens: int
    output_tokens: int
    input_usd_per_million: float
    output_usd_per_million: float

    @property
    def cost(self) -> float:
        return (
            self.input_tokens * self.input_usd_per_million
            + self.output_tokens * self.output_usd_per_million
        ) / 1_000_000


@dataclass(frozen=True)
class CloudUnitCost:
    model: ModelUsage
    compute_usd: float
    retrieval_usd: float
    observability_usd: float
    storage_usd: float
    network_usd: float
    tool_usd: float
    monthly_fixed_usd: float = 0

    @property
    def total(self) -> float:
        return self.model.cost + self.compute_usd + self.retrieval_usd + self.observability_usd + self.storage_usd + self.network_usd + self.tool_usd


@dataclass(frozen=True)
class OnPremTco:
    hardware_capex: float
    residual_value: float
    useful_life_months: int
    monthly_maintenance: float
    monthly_rack_network: float
    monthly_ops_labor: float
    average_kw: float
    pue: float
    energy_usd_per_kwh: float
    monthly_capacity_units: int

    @property
    def monthly_cost(self) -> float:
        depreciation = (self.hardware_capex - self.residual_value) / self.useful_life_months
        power = self.average_kw * self.pue * 730 * self.energy_usd_per_kwh
        return depreciation + power + self.monthly_maintenance + self.monthly_rack_network + self.monthly_ops_labor

    @property
    def unit_cost(self) -> float:
        return self.monthly_cost / self.monthly_capacity_units


@dataclass(frozen=True)
class ValueModel:
    volume_per_month: int
    revenue_per_completed_unit: float
    baseline_minutes: float
    agent_minutes: float
    loaded_labor_usd_per_hour: float
    labor_capture_rate: float
    baseline_failure_probability: float
    controlled_failure_probability: float
    impact_usd_per_failure: float

    @property
    def monthly_revenue(self) -> float:
        return self.volume_per_month * self.revenue_per_completed_unit

    @property
    def monthly_labor_value(self) -> float:
        saved_hours = max(0.0, self.baseline_minutes - self.agent_minutes) / 60
        return self.volume_per_month * saved_hours * self.loaded_labor_usd_per_hour * self.labor_capture_rate

    @property
    def monthly_risk_value(self) -> float:
        probability_delta = max(0.0, self.baseline_failure_probability - self.controlled_failure_probability)
        return self.volume_per_month * probability_delta * self.impact_usd_per_failure


@dataclass(frozen=True)
class EconomicsResult:
    scenario: str
    deployment: str
    unit_cost: float
    monthly_cost: float
    monthly_revenue: float
    monthly_labor_value: float
    monthly_risk_value: float
    monthly_net_value_before_risk: float
    monthly_net_value: float
    operating_roi: float
    risk_adjusted_roi: float
    payback_months: float | None
    gross_margin: float | None
    release_decision: str
    decision_reasons: tuple[str, ...]
    assumptions: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
