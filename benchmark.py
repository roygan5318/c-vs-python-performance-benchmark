#!/usr/bin/env python3

import argparse
import csv
import random
import shutil
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
C_SOURCE = ROOT / "insertion_sort.c"
C_PROGRAM = ROOT / "insertion_sort_c"
PYTHON_PROGRAM = ROOT / "insertion_sort.py"


def compile_c() -> str:
    compiler = shutil.which("cc") or shutil.which("clang") or shutil.which("gcc")
    if compiler is None:
        raise SystemExit("No C compiler was found (tried cc, clang, and gcc).")
    subprocess.run(
        [compiler, "-std=c11", "-O2", "-Wall", "-Wextra", str(C_SOURCE), "-o", str(C_PROGRAM)],
        check=True,
    )
    return compiler


def run_program(command: list[str], data_file: Path) -> tuple[float, int]:
    completed = subprocess.run(
        [*command, str(data_file)],
        check=True,
        capture_output=True,
        text=True,
    )
    seconds, checksum = completed.stdout.strip().split()
    return float(seconds), int(checksum)


def make_chart(rows: list[dict[str, float]], destination: Path) -> None:
    width, height = 900, 520
    left, right, top, bottom = 90, 40, 55, 80
    plot_w = width - left - right
    plot_h = height - top - bottom
    max_time = max(row["python_median_seconds"] for row in rows) * 1.10
    max_size = max(row["size"] for row in rows)

    def x(size: float) -> float:
        return left + (size / max_size) * plot_w

    def y(seconds: float) -> float:
        return top + plot_h - (seconds / max_time) * plot_h

    c_points = " ".join(f'{x(row["size"]):.1f},{y(row["c_median_seconds"]):.1f}' for row in rows)
    py_points = " ".join(f'{x(row["size"]):.1f},{y(row["python_median_seconds"]):.1f}' for row in rows)
    grid = []
    for step in range(6):
        value = max_time * step / 5
        py = y(value)
        grid.append(f'<line x1="{left}" y1="{py:.1f}" x2="{width-right}" y2="{py:.1f}" stroke="#dbe3ea"/>')
        grid.append(f'<text x="{left-12}" y="{py+5:.1f}" text-anchor="end">{value:.3f}</text>')
    labels = []
    for row in rows:
        px = x(row["size"])
        labels.append(f'<text x="{px:.1f}" y="{height-bottom+28}" text-anchor="middle">{int(row["size"]):,}</text>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/>
<style>text{{font-family:system-ui,sans-serif;fill:#263238;font-size:14px}} .title{{font-size:22px;font-weight:700}}</style>
<text class="title" x="{width/2}" y="30" text-anchor="middle">Insertion Sort: C vs. Python</text>
{''.join(grid)}
<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#455a64"/>
<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#455a64"/>
{''.join(labels)}
<text x="{width/2}" y="{height-20}" text-anchor="middle">Array size</text>
<text x="20" y="{height/2}" text-anchor="middle" transform="rotate(-90 20 {height/2})">Median time (seconds)</text>
<polyline points="{c_points}" fill="none" stroke="#1565c0" stroke-width="4"/>
<polyline points="{py_points}" fill="none" stroke="#ef6c00" stroke-width="4"/>
<circle cx="{width-235}" cy="55" r="6" fill="#1565c0"/><text x="{width-220}" y="60">C (-O2)</text>
<circle cx="{width-135}" cy="55" r="6" fill="#ef6c00"/><text x="{width-120}" y="60">Python</text>
</svg>'''
    destination.write_text(svg)


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark insertion sort in C and Python.")
    parser.add_argument("--sizes", nargs="+", type=int, default=[1000, 2000, 4000, 8000])
    parser.add_argument("--repetitions", type=int, default=10)
    parser.add_argument("--seed", type=int, default=211)
    args = parser.parse_args()

    compiler = compile_c()
    rows = []
    rng = random.Random(args.seed)

    with tempfile.TemporaryDirectory(prefix="c-vs-python-") as temporary_directory:
        temporary_path = Path(temporary_directory)
        for size in args.sizes:
            data_file = temporary_path / f"data_{size}.txt"
            values = [rng.randint(-1_000_000, 1_000_000) for _ in range(size)]
            data_file.write_text("\n".join(map(str, values)))

            c_times = []
            python_times = []
            expected_checksum = sum(values)
            for repetition in range(args.repetitions):
                # Alternate the order to reduce systematic bias from always running one language first.
                commands = [
                    ("c", [str(C_PROGRAM)]),
                    ("python", [sys.executable, str(PYTHON_PROGRAM)]),
                ]
                if repetition % 2:
                    commands.reverse()

                for language, command in commands:
                    seconds, checksum = run_program(command, data_file)
                    if checksum != expected_checksum:
                        raise RuntimeError(f"Checksum mismatch for {language}, n={size}")
                    (c_times if language == "c" else python_times).append(seconds)

            c_median = statistics.median(c_times)
            python_median = statistics.median(python_times)
            rows.append(
                {
                    "size": size,
                    "c_median_seconds": c_median,
                    "python_median_seconds": python_median,
                    "python_over_c": python_median / c_median,
                }
            )
            print(f"n={size:>6,}: C={c_median:.6f}s Python={python_median:.6f}s ratio={python_median/c_median:.1f}x")

    csv_path = ROOT / "results.csv"
    with csv_path.open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    results_path = ROOT / "RESULTS.md"
    table = [
        "# Benchmark Results",
        "",
        f"Each value is the median of {args.repetitions} runs. C was compiled with `{Path(compiler).name} -O2`.",
        "Only the insertion-sort operation was timed.",
        "",
        "| Array size | C median (seconds) | Python median (seconds) | Python/C ratio |",
        "|---:|---:|---:|---:|",
    ]
    table.extend(
        f'| {int(row["size"]):,} | {row["c_median_seconds"]:.6f} | {row["python_median_seconds"]:.6f} | {row["python_over_c"]:.1f}× |'
        for row in rows
    )
    table.extend(
        [
            "",
            "![Runtime graph](results.svg)",
            "",
            "## Interpretation",
            "",
            "Both implementations use the same O(n²) insertion-sort algorithm, so their runtimes grow similarly as the input gets larger. "
            "The absolute times differ because optimized C is compiled to native machine code, while CPython performs additional interpreter, dynamic-type, and object-handling work.",
        ]
    )
    results_path.write_text("\n".join(table) + "\n")
    make_chart(rows, ROOT / "results.svg")


if __name__ == "__main__":
    main()
