"""Measure end-to-end latency of ResearchMind's real pipeline calls."""

import statistics
from argparse import ArgumentParser

from pipeline import run_research_pipeline


DEFAULT_QUERIES = [
    "Recent advances in solid-state batteries",
    "How are cities adapting to extreme heat?",
    "The current state of quantum error correction",
    "Benefits and risks of precision agriculture",
    "How remote work is changing urban economies",
]


def main() -> None:
    parser = ArgumentParser(description="Benchmark ResearchMind pipeline latency.")
    parser.add_argument(
        "queries",
        nargs="*",
        help="Optional research topics. Supply 5-10 for a representative run.",
    )
    args = parser.parse_args()
    queries = args.queries or DEFAULT_QUERIES

    if not 5 <= len(queries) <= 10:
        parser.error("Provide between 5 and 10 queries.")

    timings = []
    for number, query in enumerate(queries, start=1):
        print(f"\n{'#' * 72}\nRun {number}/{len(queries)}: {query}\n{'#' * 72}")
        try:
            result = run_research_pipeline(query)
            elapsed = result["pipeline_elapsed_seconds"]
            timings.append(elapsed)
            print(f"Run {number} completed in {elapsed:.2f}s")
        except Exception as error:
            print(f"Run {number} failed: {error}")

    if not timings:
        raise SystemExit("No benchmark runs completed successfully.")

    average = statistics.mean(timings)
    print("\nBenchmark summary")
    print(f"Successful runs: {len(timings)}/{len(queries)}")
    print(f"Average: {average:.2f}s")
    print(f"Range: {min(timings):.2f}s - {max(timings):.2f}s")
    print(f"Report-ready: API/LLM pipeline calls averaged {average:.1f}s (range {min(timings):.1f}-{max(timings):.1f}s; n={len(timings)}).")


if __name__ == "__main__":
    main()
