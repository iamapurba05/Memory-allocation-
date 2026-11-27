# MemAlloc — Dynamic Memory Allocation Simulator

Operating Systems capstone, project 6. A local web application comparing First Fit, Best Fit and Worst Fit on identical workloads. It simulates contiguous memory; it does not allocate actual operating system RAM.

## Run locally (Windows)

1. Extract the project ZIP. Open the `MemAlloc` folder in VS Code.
2. Open Terminal > New Terminal (PowerShell).
3. Run `python --version` (Python 3.10 or later). If the `python` command is unavailable, try `py --version`.
4. Run `python app.py` (or `py app.py`).
5. Open http://127.0.0.1:8501 in Edge or Chrome.
6. Stop the server with Ctrl+C. Alternatively, double-click `start.bat` to start the server, then open the URL manually.

No pip packages, database or internet connection are required. If port 8501 is occupied, stop the other service or change the port in `app.py` and the browser URL.

## Features

- First Fit, Best Fit and Worst Fit, each starting with a fresh copy of the original blocks.
- Dynamic splitting: remaining space can be reused by later processes.
- Optional fixed-partition comparison to demonstrate internal fragmentation.
- Visual memory blocks, per-process allocation trace (before/after and inspected blocks), failed-allocation reasons.
- Comparison table and utilization chart, largest free hole, allocation success, block checks and fragmentation metrics.
- CSV export and sample workloads; validation in both the UI and backend.

## Structure

```text
MemAlloc/
  app.py                 Local HTTP server and API
  algorithms.py          Allocation logic and metrics
  static/
    index.html           Interface
    style.css            Design and responsive layout
    script.js            Input, API calls, graphs, CSV
  tests/
    test_algorithms.py   Automated tests
    test_api.py          HTTP integration tests
  docs/
    project-report.md    Report draft (complete student fields and evidence)
    viva-guide.md        Demo and oral examination guide
    test-results.txt     Actual automated test log
    verification.md      Verification scope and manual checklist
  start.bat              Windows launcher
  .gitignore
```

## Test

From the project directory, run `python -m unittest discover -s tests -v`. The API tests use a temporary local server and an available port. You do not need to start the app first.

## Example

Blocks: `100, 500, 200, 300, 600` KB. Processes: `212, 417, 112, 426` KB.

| Algorithm | Allocation (block IDs, dash = failure) | Allocated | Used KB | Free KB |
|---|---|---:|---:|---:|
| First Fit | 2, 5, 2, — | 3/4 | 741 | 959 |
| Best Fit | 4, 2, 3, 5 | 4/4 | 1167 | 533 |
| Worst Fit | 5, 2, 5, — | 3/4 | 741 | 959 |

Best Fit wins on allocation count for this input, not for every possible workload.

## Model and metrics

Original blocks represent distinct free holes, separated by occupied regions; their remainders cannot be merged. Requests arrive in listed order. There is no process release, compaction, alignment or metadata overhead. Ties choose the earliest block. In dynamic mode each successful allocation splits its hole exactly, hence modeled internal fragmentation is zero. In fixed mode one process occupies the entire selected partition and unused capacity becomes internal waste.

- Useful utilization = allocated process memory / original capacity × 100.
- Success rate = allocated processes / requested processes × 100.
- External fragmentation index (dynamic only) = (1 − largest free hole / total free memory) × 100, defined as 0 if no free space remains. This is a distribution index, not a measure of permanently wasted memory.
- An external-fragmentation failure occurs when total free memory is sufficient but no single hole fits a request.
- Block checks count inspections in the allocation search, not wall-clock runtime. All three algorithms are O(P×B) worst-case time, for P requests and B blocks.
- Capacity = allocated useful memory + free memory + internal waste.

## Submission

Read the report draft and viva guide. Run and understand the app, independently check results, personalize it and capture real screenshots from your own browser. Follow your institution's AI-assistance disclosure rules. Commit your genuine changes and test results as you work. No GitHub repository has been created for you; publish your own repository and add its URL to the report.
