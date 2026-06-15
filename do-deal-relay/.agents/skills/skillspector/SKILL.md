---
name: skillspector
description: Scan repository skills for security vulnerabilities and risks using SkillSpector.
license: Apache-2.0
compatibility: Requires Python 3.10+, 'skillspector' CLI installed.
permissions:
  - shell
  - file_read
  - file_write
---

# SkillSpector

Use this skill to perform security analysis on AI agent skills within the repository.

## Overview

SkillSpector is a security scanner for AI agent skills. It identifies malicious patterns, insecure code execution, data exfiltration, and principle of least privilege violations.

## Quick Start

```bash
# Scan a specific skill
skillspector scan --format terminal --no-llm .agents/skills/my-skill

# Scan with LLM analysis (requires NVIDIA_INFERENCE_KEY or OPENAI_API_KEY)
skillspector scan --format terminal .agents/skills/my-skill
```

## When to use this skill

- Before installing or using a new skill from an external source.
- After modifying a skill's manifest (SKILL.md) or its executable scripts.
- As part of a security audit or quality gate in the CI/CD pipeline.

## Actions

- **scan**: Run SkillSpector on a skill directory.
  - `skillspector scan --format [terminal|json|markdown|sarif] [skill_path]`
- **audit-repo**: Scan all skills in the repository.
  - `for d in .agents/skills/*/; do skillspector scan --format terminal --no-llm "$d"; done`

## Remediation

- **CRITICAL/HIGH**: Do not use the skill. Review and fix findings (e.g., remove `exec()`, sanitize inputs, declare permissions).
- **MEDIUM**: Use with caution. Review findings and verify they are intended behaviors.
- **LOW**: Generally safe. Address minor issues like over-declared permissions.

## References

See [SkillSpector GitHub](https://github.com/NVIDIA/SkillSpector) for more information on rule IDs and risk scoring.
