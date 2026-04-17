# Extras: ECC Performance Experiments

This folder contains experimental versions of the ECC implementation used for learning and benchmarking.

## Files

- `info_red_threads.py`: Thread-based experiment.
- `info_red_numba.py`: Numba JIT experiment.
- `time_calc.py`: External benchmark runner (runs each script as a separate process).

## Results We Got

Using `time_calc.py` with warmup and repeated runs, we got the following summary:

```text
=== Summary ===
information_redudancy.py: mean=1.594907s, median=1.534829s, n=14
info_red_threads.py: mean=2.303568s, median=2.162522s, n=14
info_red_numba.py: mean=4.844882s, median=4.656397s, n=14
Fastest (mean): information_redudancy.py (1.594907s)
```

## Why These Results Happened

1. **The benchmark measures full process time**
   - `time_calc.py` uses `subprocess.run(...)`, so timing includes Python startup, imports, script execution, and process shutdown.
   - This is not just the ECC kernel time.

2. **Numba has high fixed overhead in this setup**
   - Numba import and JIT compilation add startup cost.
   - For very small data (`72` bits codeword), that fixed cost can dominate total runtime.

3. **Threading does not strongly help for small CPU-bound work**
   - The workload is tiny, and Python thread management overhead can offset potential gains.
   - Small differences between baseline and threads are expected and can vary run to run.

4. **Input was normalized (`np.ones`)**
   - All scripts used the same bit pattern, which is good for fair comparison.

## Takeaway

For this exact benchmark style (external process timing + very small payload), plain Python/NumPy can be as fast as or faster than the experimental Numba/thread versions.

These scripts are kept as **study/experiment artifacts**, not the primary implementation.

The README and `time_calc.py` were written by AI, while the 3 other information redundancy scripts were done by the author, as it was done for study. Those tests were only made to anwer personal curiosity.