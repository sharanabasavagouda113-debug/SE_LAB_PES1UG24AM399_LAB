# Lab 7: Irrigation Scheduler Fuzz Testing

**Student:** sharanabasava
**SRN:** PES1UG24AM399

The assignment uses the instructor's `lab7/irrigation_scheduler.py` starter.
The handout's `processor.py` names are generic; retain these module filenames.

## Run

Use Python 3.10 or later with the supplied dependencies:

```text
python -m pip install -r requirements.txt
python irrigation_scheduler.py
python -m pytest test_irrigation_scheduler.py -q
```

## Results

- Original implementation, same tests: 29 failed, 2 passed.
- Fixed implementation: 31 passed.
- Six Hypothesis properties, up to 300 examples per property.
- 24 parameterized invalid-input checks and one regression test.

Invalid inputs return `None`. Moisture readings are interpreted as percentages
from 0 to 100; areas and rainfall must be finite and nonnegative. Decimal moisture
values are supported. These validation rules are implemented in the application.

`evidence/` contains genuine subprocess logs, formatted output captures in a
Windows PowerShell-style view, dependency information and a copy of the unmodified
starter. Evidence text files and screenshots have user-specific local paths redacted; test outputs are retained. The failure
summary screenshot and minimized-counterexample screenshot are explicitly marked
as excerpts; the complete failure log is included.

## Sources

- Starter: https://github.com/SETAPESU26/L6_L7_37_irrigation_scheduler/tree/main/lab7
- GitHub profile: https://github.com/sharanabasavagouda113-debug

The final files are prepared locally for review and submission.




