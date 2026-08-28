from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import evaluate_scenario
from .pricing import fetch_retail_prices


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate agentic workflow unit economics")
    sub = parser.add_subparsers(dest="command", required=True)
    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("scenario", type=Path)
    evaluate.add_argument("--deployment", choices=("azure", "on_prem", "both"), default="both")
    evaluate.add_argument("--output", type=Path)
    prices = sub.add_parser("snapshot-prices")
    prices.add_argument("--filter", required=True)
    prices.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "snapshot-prices":
        result = fetch_retail_prices(args.filter, args.output)
    else:
        config = json.loads(args.scenario.read_text(encoding="utf-8"))
        deployments = ("azure", "on_prem") if args.deployment == "both" else (args.deployment,)
        result = [evaluate_scenario(config, d).as_dict() for d in deployments]
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

