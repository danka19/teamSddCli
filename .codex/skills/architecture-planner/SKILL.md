---
name: architecture-planner
description: Plan or revise project architecture from current docs, implementation evidence, audit findings, and human decisions. Use when the user asks for architecture planning, module boundaries, data model choices, integration design, deployment shape, security boundaries, ADR-like decisions, or a technical plan before implementation.
---

# Architecture Planner

Use this skill before implementation when architecture decisions can affect product behavior, data contracts, persistence, security, integrations, deployment, or long-term maintainability.

## Workflow

1. Read the required project docs from `AGENTS.md`.
2. Search existing code, tests, and docs for related concepts.
3. Identify raw facts, accepted human decisions, open decisions, constraints, and risks.
4. Propose the smallest architecture that supports the next validated workflow.
5. Separate accepted decisions from options and unresolved questions.
6. Update durable docs when the plan changes architecture, setup, operations, security, roadmap status, or data contracts.

## Output Shape

Include:

- decision summary;
- module/service/data boundaries;
- tradeoffs;
- rejected options;
- verification strategy;
- documentation updates;
- open human decisions.
