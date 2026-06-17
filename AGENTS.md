
## SkillSpector Security Protocol
Before adding or modifying any agent skill, run a SkillSpector scan to ensure no high-severity vulnerabilities are introduced.
```bash
skillspector scan --format terminal --no-llm .agents/skills/<skill-name>
```
Refer to `audits/do-deal-relay/summary.md` for the latest audit findings and remediation guidelines.
