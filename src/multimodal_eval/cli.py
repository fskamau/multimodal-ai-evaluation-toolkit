from __future__ import annotations

import argparse
import json

from .evaluator import evaluate_response


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a structured AI evaluation.")
    parser.add_argument("--id", required=True, dest="evaluation_id")
    parser.add_argument("--task-type", default="text")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--response", required=True)
    parser.add_argument(
        "--scores",
        required=True,
        help='JSON object, e.g. '{"factuality":4,"instruction_following":5}'',
    )
    args = parser.parse_args()

    result = evaluate_response(
        evaluation_id=args.evaluation_id,
        task_type=args.task_type,
        prompt=args.prompt,
        response=args.response,
        scores=json.loads(args.scores),
    )
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
