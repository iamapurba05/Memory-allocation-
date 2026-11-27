# Verification status

- Automated core algorithm and HTTP integration tests: see `test-results.txt` for the actual execution log.
- JavaScript syntax checked with Node.js during packaging.
- Browser end-to-end check could not be completed in the packaging environment: Chromium blocked localhost navigation (`ERR_BLOCKED_BY_ADMINISTRATOR`). No application screenshots or browser interaction results are claimed. Run the following manual checks on your own laptop and capture authentic evidence.

## Manual browser checklist
- [ ] Open app at http://127.0.0.1:8501; no visible errors.
- [ ] Default First Fit: 3/4 allocated, 959 KB free.
- [ ] Best Fit: 4/4 allocated, 533 KB free.
- [ ] Worst Fit: 3/4 allocated, 959 KB free.
- [ ] Expand a trace row; verify selected block, before/after values.
- [ ] External fragmentation example: 0/1 allocated, 66.67% index.
- [ ] Fixed partition with block 100 and processes 40,60: 1/2 allocated, 60 KB waste.
- [ ] CSV export downloads and contains all three algorithms.
- [ ] Invalid input `0, 200` displays an error; Reset sample restores results.
- [ ] Screenshot your own working app and add it to screenshots/.
- [ ] Verify repository URL and individual contributions in report.
