# SkillSpector Security Audit Report

**Date:** 2026-06-15
**Tool:** SkillSpector v2.1.4 (Static Analysis Mode)
**Target:** `do-deal-relay` Agent Skills

## Executive Summary

A security audit of the AI agent skills in this repository was performed using SkillSpector. The audit identified significant security risks in skills containing executable scripts, particularly those handling external APIs or generating new skills.

| Skill | Risk Score | Severity | Recommendation |
|-------|------------|----------|----------------|
| `jules-usage` | 100/100 | CRITICAL | DO NOT INSTALL |
| `skill-creator` | 100/100 | CRITICAL | DO NOT INSTALL |
| `goap-agent` | 26/100 | MEDIUM | CAUTION |
| `skill-evaluator` | 13/100 | LOW | SAFE |

## Detailed Findings

### 1. jules-usage (CRITICAL)
- **Rule ID: LP3**: Missing permissions declaration in `SKILL.md`.
- **Rule ID: TM1**: Tool parameter abuse in `references/commands.md`.
- **Rule ID: E1**: External transmission of data in `scripts/jules_api_request.sh`.
- **Rule ID: AST3/AST4**: Use of `__import__` and `subprocess` in `scripts/test.py`.

### 2. skill-creator (CRITICAL)
- **Rule ID: RA1**: Self-modification patterns (e.g., in `scripts/aggregate_benchmark.py`).
- **Rule ID: OH1**: Unvalidated output injection in `references/workflows.md`.
- **Rule ID: MP3**: Memory manipulation instructions in `reference/guide.md`.

### 3. goap-agent (MEDIUM)
- **Rule ID: EA2**: Autonomous decision making without human-in-the-loop confirmation.
- **Rule ID: LP3**: Missing permissions declaration.

### 4. skill-evaluator (LOW)
- **Rule ID: LP3**: Missing permissions declaration (Minor).

## Integration

SkillSpector has been integrated into the repository:
1. **Skill Definition**: Added to `.agents/skills/skillspector`.
2. **Jules Integration**: Linked to `.jules/skills/skillspector`.
3. **Reports**: Detailed logs available in `reports/skillspector/`.
4. **Sentinel**: Findings recorded in `.jules/sentinel.md`.

## Remediation Plan

1. **Permission Lockdown**: Add explicit `permissions` field to all `SKILL.md` files.
2. **Safe Code Execution**: Replace `shell=True` with list-based arguments in all Python scripts using `subprocess`.
3. **Input Validation**: Sanitize all tool parameters and model-generated content.
4. **Confirmation Gates**: Implement human confirmation for destructive actions in `skill-creator` and `goap-agent`.
