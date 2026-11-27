# Operating Systems Capstone Report
## Project 6 — Dynamic Memory Allocation Simulator (MemAlloc)

Student(s): [fill in]  
Roll number(s): [fill in]  
Section / group: [fill in]  
Faculty: [fill in]  
GitHub URL: [add after publishing]  

## 1. Problem statement and objective
Contiguous memory allocation requires selecting a free region large enough to hold each process. Different placement strategies leave different free-hole patterns, which may prevent future allocations despite sufficient total free space. This project compares First Fit, Best Fit and Worst Fit with identical input workloads and visualizes their effects on allocation success, useful memory utilization and fragmentation.

## 2. OS concepts and tools
Contiguous allocation, dynamic partitions, fixed partitions, internal and external fragmentation, memory utilization. Tools: Python standard library, HTML, CSS, JavaScript, browser, VS Code and Git. The app runs on localhost and simulates sizes in KB rather than changing actual RAM.

## 3. Architecture
Browser input → local Python HTTP API → independent algorithm runs → JSON results → allocation trace, memory bars, comparison table and chart. Each algorithm receives a fresh copy of the original free holes. The optional fixed mode demonstrates internal waste.

## 4. Algorithm / pseudocode
```
remaining = copy(original_blocks)
for process in arrival_order:
    scan remaining blocks for those at least process.size
    First Fit: choose first suitable block (stop scanning)
    Best Fit: choose smallest suitable block
    Worst Fit: choose largest suitable block
    if none exists: mark allocation failed
    otherwise: record block and subtract process size
    in fixed mode: record remainder as internal waste; set free space to zero
    record before/after state
calculate metrics and compare algorithms
```
All methods use O(P × B) worst-case allocation time; storing a full trace uses O(P × B) space. Equal-size candidates are resolved by choosing the earliest block. No block merging or release is modeled.

## 5. Metrics
Useful utilization = allocated useful KB / total original KB × 100. Allocation success = allocated requests / total requests × 100. Internal waste = unused capacity within occupied fixed partitions; zero in the ideal dynamic model. External index = 100 × (1 − largest free hole / total free KB), or zero if no free KB. It is a comparative index rather than an absolute number of wasted bytes. A failed request due to external fragmentation has enough total free KB, but no individual hole large enough. Block inspections provide a reproducible measure of search effort.

## 6. Test cases
| Test | Blocks | Processes | Expected result |
|---|---|---|---|
| Normal | 100,500,200,300,600 | 212,417,112,426 | First/Best/Worst allocate 3/4/3 |
| Exact fit | 100,200 | 100,200 | All allocated; zero free |
| Reuse | 100 | 40,60 | Dynamic: both allocated |
| External fragmentation | 100,100,100 | 150 | Failure despite 300 KB free; index 66.67% |
| Insufficient memory | 100,200 | 400 | Failure: total free insufficient |
| Internal fragmentation | 100 | 40,60 | Fixed: P1 allocated, 60 KB internal waste, P2 fails |
| Invalid | 0,200 | 100 | Validation error |
| Invalid | 100 | abc | Validation error |
| Boundary | 1,1000000 | 1,1000000 | Both allocated |

See `test-results.txt` for actual automated tests. Verify the browser cases locally and attach real screenshots before submission.

## 7. Standard workload results
| Algorithm | P1 | P2 | P3 | P4 | Used KB | Free KB | Success |
|---|---|---|---|---|---:|---:|---:|
| First Fit | B2 | B5 | B2 | Failed | 741 | 959 | 75% |
| Best Fit | B4 | B2 | B3 | B5 | 1167 | 533 | 100% |
| Worst Fit | B5 | B2 | B5 | Failed | 741 | 959 | 75% |
Best Fit allocates every request on this workload. First Fit may inspect fewer blocks because it stops as soon as a suitable hole is located. No algorithm is universally best.

## 8. Actual output evidence (student to complete)
Insert screenshots from your own local run: standard workload, Best Fit, expanded trace, fragmentation example, fixed comparison, invalid-input error and terminal test result. Add your GitHub URL and genuine commit history. Do not submit placeholders as evidence.

## 9. Limitations and future scope
The simulator uses abstract integer sizes and distinct initial holes, assumes no alignment or metadata costs and does not model real virtual memory, concurrent processes or process release. Future enhancements: deallocation/coalescing, compaction, workload generation and repeated performance benchmarking.

## 10. Conclusion
The simulator illustrates how placement decisions influence remaining holes and the success of later requests. Identical workloads permit fair comparison, while the trace makes each allocation decision explainable. The fixed-partition mode contrasts internal waste with external fragmentation in dynamic allocation.

## 11. Contribution / AI assistance (complete accurately)
Describe each member's actual contribution, modifications, tests and any AI assistance in accordance with institutional policy.
