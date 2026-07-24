---
name: teamssd-systematic-debugging
description: Use when a bug, failing check, unexpected output, hang, or inconsistent behavior must be diagnosed before fixing.
---

# Systematic Debugging

Reproduce the symptom locally, capture the exact failure and trace data flow to
the earliest incorrect state. Form one falsifiable hypothesis, run the
narrowest local experiment, and change one variable at a time.

Do not patch symptoms before identifying the cause. For code fixes use
`teamssd-test-driven-development` unless the human explicitly waives tests.
Verify the original symptom after the change and report remaining uncertainty.

Do not use web search or external diagnostics.
