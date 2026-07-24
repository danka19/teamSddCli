---
name: teamssd-test-driven-development
description: Use when implementing a code feature or bug fix before writing production code, unless the human explicitly waives tests.
---

# Test-Driven Development

Write one focused local test, run it and confirm it fails for the expected
missing behavior. Implement the smallest change, run the test to green, then
refactor while keeping relevant checks green.

Tests must exercise real behavior; mock only unavoidable boundaries. A test
that never failed is not RED evidence. When the human explicitly waives tests,
record the exception and residual regression risk rather than claiming TDD.

Never download dependencies to satisfy the cycle.
