from __future__ import annotations

import argparse
import statistics
import subprocess
import sys
from pathlib import Path
from time import perf_counter


def run_and_time(script_path: Path) -> dict[str, object]:
	start = perf_counter()
	completed = subprocess.run(
		[sys.executable, str(script_path)],
		capture_output=True,
		text=True,
	)
	elapsed = perf_counter() - start

	return {
		"name": script_path.name,
		"elapsed": elapsed,
		"returncode": completed.returncode,
		"stdout": completed.stdout,
		"stderr": completed.stderr,
	}


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Benchmark ECC scripts")
	parser.add_argument(
		"-n",
		"--runs",
		type=int,
		default=15,
		help="Number of runs per script (default: 15)",
	)
	parser.add_argument(
		"-w",
		"--warmup",
		type=int,
		default=1,
		help="Number of initial runs to discard (default: 1)",
	)
	return parser.parse_args()


def summarize_times(values: list[float]) -> dict[str, float]:
	if len(values) == 1:
		return {
			"mean": values[0],
			"median": values[0],
			"stdev": 0.0,
			"min": values[0],
			"max": values[0],
		}

	return {
		"mean": statistics.mean(values),
		"median": statistics.median(values),
		"stdev": statistics.pstdev(values),
		"min": min(values),
		"max": max(values),
	}


def main() -> None:
	args = parse_args()
	total_runs = args.runs
	warmup_runs = args.warmup

	if total_runs <= 0:
		raise ValueError("--runs must be greater than 0")

	if warmup_runs < 0:
		raise ValueError("--warmup cannot be negative")

	if warmup_runs >= total_runs:
		raise ValueError("--warmup must be less than --runs")

	base_dir = Path(__file__).resolve().parent
	project_root = base_dir.parent
	scripts = [
		project_root / "information_redudancy.py",
		base_dir / "info_red_threads.py",
		base_dir / "info_red_numba.py",
	]

	results: list[dict[str, object]] = []

	print(f"Runs per script: {total_runs}")
	print(f"Warmup runs discarded: {warmup_runs}")

	for script in scripts:
		if not script.exists():
			print(f"File not found: {script}")
			continue

		times: list[float] = []
		failures = 0

		for run_idx in range(total_runs):
			run_result = run_and_time(script)

			if run_result["returncode"] != 0:
				failures += 1
				print(
					f"Failure in {run_result['name']} on run {run_idx + 1}: "
					f"exit={run_result['returncode']}"
				)
				stderr = str(run_result["stderr"]).strip()
				if stderr:
					print(stderr)
				continue

			times.append(float(run_result["elapsed"]))

		if len(times) <= warmup_runs:
			print(f"\n=== {script.name} ===")
			print("Not enough samples after warmup.")
			continue

		valid_times = times[warmup_runs:]
		stats = summarize_times(valid_times)
		entry = {
			"name": script.name,
			"stats": stats,
			"samples": len(valid_times),
			"failures": failures,
		}
		results.append(entry)

		print(f"\n=== {script.name} ===")
		print(f"Valid samples: {entry['samples']}")
		print(f"Failures: {failures}")
		print(f"Mean: {stats['mean']:.6f}s")
		print(f"Median: {stats['median']:.6f}s")
		print(f"Std dev (population): {stats['stdev']:.6f}s")
		print(f"Min: {stats['min']:.6f}s")
		print(f"Max: {stats['max']:.6f}s")

	if results:
		fastest = min(results, key=lambda item: item["stats"]["mean"])
		print("\n=== Summary ===")
		for item in results:
			stats = item["stats"]
			print(
				f"{item['name']}: mean={stats['mean']:.6f}s, "
				f"median={stats['median']:.6f}s, n={item['samples']}"
			)
		print(
			f"Fastest (mean): {fastest['name']} "
			f"({fastest['stats']['mean']:.6f}s)"
		)


if __name__ == "__main__":
	main()
