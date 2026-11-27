# Demo and viva guide

## Five-minute live demo
1. State the problem: choosing contiguous free memory for incoming processes. Clarify the app is a simulation, not actual RAM allocation.
2. Run the default sample. Show First Fit and open P1's trace: B1 is too small, B2 fits; 500 − 212 = 288 KB remains.
3. Switch to Best Fit and Worst Fit. Explain why Best Fit places P1 in B4 and Worst Fit places it in B5. Show comparison results (3/4, 4/4, 3/4).
4. Select External fragmentation example: 300 KB total free, largest hole 100 KB, request 150 KB cannot be satisfied. Explain external index 66.67%.
5. Set blocks to 100 and processes to 40,60; switch to fixed mode and run. Explain 60 KB internal waste and why P2 cannot use it. Return to dynamic mode to show both fit.
6. Try invalid input `0, 200`. Demonstrate validation. Reset sample and export CSV.
7. Show algorithms.py and tests, run `python -m unittest discover -s tests -v`, and show your actual repository.

## Likely questions and answers
- What is memory allocation? Assigning memory to processes so they can execute.
- First Fit? First hole in the search order large enough to satisfy a request.
- Best Fit? Smallest suitable hole; aims to minimize leftover space from the immediate allocation.
- Worst Fit? Largest suitable hole; aims to leave a larger remainder.
- What is internal fragmentation? Unusable space within an allocated partition. Fixed mode makes this visible.
- External fragmentation? Free holes are separated; a contiguous request can fail even with enough total free memory.
- Why zero internal fragmentation in dynamic mode? Exact-size splitting is assumed, with no rounding or metadata overhead.
- Which algorithm is best? Depends on workload and metric. Best Fit wins for the default example on allocation count.
- Why copy the blocks? To avoid one algorithm modifying another's input, enabling fair comparison.
- Complexity? Worst-case O(P × B); First Fit can stop early, Best/Worst Fit inspect all blocks in this implementation.
- Why measure block checks? Reproducible search effort without hardware-dependent timings. It is not elapsed execution time.
- What is the external index? 100 × (1 − largest free hole / total free memory), a free-space dispersion indicator, not a count of permanently wasted memory.
- What happens with equally suitable blocks? Earliest block wins, providing deterministic output.
- Why no database? All data is supplied for a local run; CSV provides export without persistent storage requirements.
- What is the backend? Python computes results and provides them through a local HTTP POST endpoint. JavaScript displays the JSON.
- Can this modify actual RAM? No. Input sizes are simulated abstract holes.
- How could you improve it? Add process release, adjacent hole coalescing, compaction, and workload benchmarking.

## Live modification practice
Change the default input in `static/index.html`, update `reset` in `static/script.js` to match, and rerun. Change one test case and predict its expected result before running. Try a custom workload where First Fit outperforms another method. Be able to point to the first-fit break, best-fit min and worst-fit max in `algorithms.py`.
