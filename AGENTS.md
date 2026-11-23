# AI Agent Guidelines

This project follows the AI/LLM-Assisted Contributions Policy outlined in `README.rst`.

## LLM Policy

When contributing to this repository, AI agents (and the humans using them) must adhere to the following:

1. **Responsibility**: The human developer is responsible for all contributions. All LLM-generated code must be reviewed and understood by the developer before submission.
2. **PR Disclosure**: Any pull request containing LLM-generated content must explicitly disclose this in the PR description.
3. **Commit Attribution**: Every commit containing LLM-generated content must include an `Assisted-by` (recommended) or `Co-authored-by` commit trailer in the commit message.

### Commit Message Format

Follow the project's requirement for an `Assisted-by` or `Co-authored-by` trailer. A recommended format is:

`Assisted-by: <AGENT_NAME> with <MODEL_VERSION>[, TOOL1, TOOL2, ...]`

Example: `Assisted-by: OpenCode 2.3.0 with gemma4:31b`
