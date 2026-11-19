# Token-efficient debugging prompt

Investigate only the failing command/test and directly related files.
Do not reread the whole repository. First reproduce the issue, capture the exact error,
identify the smallest root cause, make the smallest safe change, and rerun the failing test.
Do not redesign unrelated components. Return: root cause, changed files, exact test result,
and any remaining risk. Use Sonnet; escalate only after two focused failed attempts.
