---
name: progress-bars
description: Any long-running process (loops over files/events, batch jobs, downloads, renders, scans) must report progress with a useful progress bar — tqdm in Python, or rate/ETA logging where a TTY bar is unavailable (CI, logs). Use whenever writing or reviewing a tool that takes more than a few seconds.
---

# progress-bars

Any tool or script that can run longer than a few seconds must show its
progress. Silent long processes are indistinguishable from hung ones, waste
debugging time, and hide throughput regressions.

## What "useful" means

A good progress bar shows all of:
- **Fraction done** (n/total and %) when the total is knowable — count it up
  front (files, events, rows) rather than falling back to a spinner.
- **Rate** (items/s, MB/s) so throughput regressions are visible.
- **ETA**, derived from the rate.
- **A label** saying *what* is progressing (`"histogramming Events"`, not
  bare `it`).

For unknown totals, still show a counter + rate, not a bare spinner.

## Python: `tqdm`

Default choice. Wrap the iterable; don't hand-roll `print(i)` loops.

```python
from tqdm import tqdm

for path in tqdm(paths, desc="processing files", unit="file"):
    process(path)

# Unknown total / manual updates (e.g. bytes downloaded):
with tqdm(desc="downloading", unit="B", unit_scale=True, total=size) as bar:
    for chunk in stream:
        out.write(chunk)
        bar.update(len(chunk))
```

- Nested loops: `tqdm(..., leave=False)` on inner bars.
- `uproot.iterate` chunks: wrap with a manual bar updated by
  `chunk_size`, or compute `num_entries` first for a real total.
- Keep bars on **stderr** (tqdm's default) so stdout stays parseable.

## Non-TTY contexts (CI, batch logs, `docker run` without `-t`)

Interactive bars turn into garbage in logs. Detect it and degrade to
periodic line output:

```python
import sys
bar = tqdm(paths, desc="processing", disable=None,  # auto-off when not a TTY
           mininterval=5)
```

`disable=None` auto-disables on non-TTYs; when disabled, emit a heartbeat
line every N items or seconds (`logging.info("processed %d/%d (%.0f/s)")`).
CI logs should show steady, timestamped progress — never minutes of silence.

## Shell scripts

- Prefer tools' built-in progress (`rsync --info=progress2`, `curl -#`,
  `pv` in pipes: `pv big.dat | process`).
- For loops, print `"[$i/$total] $item"` per iteration.

## Rules

- Any loop that may exceed ~5 seconds gets a bar or heartbeat. No exceptions
  for "quick" scripts — they grow.
- Never let a bar corrupt machine-readable output: bars to stderr, data to
  stdout.
- Long multi-stage jobs: one labeled bar per stage, not one mystery bar for
  the whole job.
- Add the dependency properly (`tqdm` in `requirements.txt`/the Docker
  image), don't vendor or conditionally import-and-skip.
