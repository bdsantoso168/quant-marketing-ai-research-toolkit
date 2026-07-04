# Task 4: AI Agent from the AlphaGenome Paper (Paper2Agent)

## Objective

Build an AI agent from the AlphaGenome research paper using the Paper2Agent framework, then run a given Mendelian randomization prompt through the agent and save the output.

## Tooling

- Framework: https://github.com/jmiao24/Paper2Agent
- Target paper/repo: https://github.com/google-deepmind/alphagenome
- Execution environment: Claude Code, local build (not the remote hosted MCP option)
- Models: Anthropic API key for the nested Paper2Agent build calls, AlphaGenome API key for the model itself

## Why local build over remote MCP

Paper2Agent ships a pre hosted remote MCP server for AlphaGenome (`https://Paper2Agent alphagenome mcp.hf.space`), which would have skipped the build step entirely. Chose the local build instead because the task asks to "create an AI agent from the paper," which reads as testing the build and operate cycle, not just querying an existing agent. This also produces a reproducible setup trail, which matters more for this evaluation than speed.

## Environment

- macOS, Apple Silicon
- System bash: 3.2 (Apple ships the last GPLv2 version, does not support `declare -A`)
- Python: 3.13.1, both Paper2Agent and AlphaGenome require >= 3.10, no conflict
- Claude Code CLI, run from a local working directory (not a Cowork project)

## Blockers hit and fixes applied

All fixes below are documented deviations from Paper2Agent as shipped, not silent workarounds.

### 1. `claude` CLI not on PATH
Symlinked the Claude Desktop app's bundled binary into `~/.local/bin/claude`. Avoided `npm install -g` since it required sudo.

### 2. `fastmcp` not installed
Installed with `pip install --user fastmcp`, symlinked into `~/.local/bin/fastmcp`.

### 3. Retired model reference (root blocker for the build itself)
Paper2Agent hardcodes `claude-sonnet-4-20250514` across 6 script files (`scripts/05_run_step{1,2,3,4,5,6}_*.sh`). This model is retired and returns a 404 against current API keys. Patched all 6 occurrences to `claude-sonnet-4-6`, matching the original cost and quality tier intent. Verified with a direct auth test before proceeding (`AUTH_OK`, billed against the project's Anthropic API key).

Risk flagged: this substitution was not spot checked against every downstream step at the time of the swap, only verified for auth and model resolution. If any of the 6 patched scripts behave differently than a clean 404 later in the run, that is a signal the substitution is not fully compatible, not a new unrelated bug, and should be traced back here first.

### 4. Bash 3.2 incompatibility
The orchestrator script and `05_run_step5_generate_coverage.sh` use `declare -A` associative arrays, which require bash 4+. macOS ships bash 3.2. Patched both scripts to avoid associative arrays. Verified with a syntax check before rerunning.

### 5. Unquoted paths break on directories with spaces
The working project path included spaces (`NYU - Junior Research Scientist Role`). Paper2Agent invokes sub scripts with unquoted `$SCRIPT_DIR/scripts/...sh` references throughout, which break on word splitting. Rather than patch every unquoted reference individually (fragile, easy to miss one), symlinked the Paper2Agent directory to a space free path and ran from there.

### 6. `envsubst` not installed
`envsubst` (GNU gettext) is used in 4 scripts and is not installed on macOS by default. Wrote a minimal drop in replacement scoped only to the specific substitution patterns Paper2Agent actually uses, not general `envsubst` semantics (no attempt to handle nested braces or unset variable edge cases beyond what the scripts call for). This is the highest risk patch of the six since it is the least mechanical fix and the one most likely to silently misbehave on an edge case not yet observed.

## Resume behavior observed

The pipeline tracks step completion and skips cleanly on rerun. After each of the fixes above, steps 1 through 4 (setup, clone, prepare directories, add context MCP server) reported `SKIPPED (already done)` and did not re execute. This meant each fix only cost a rerun from the point of failure forward, not from step 1.

## Step timings

| Step | Description | Duration | Status |
|------|-------------|----------|--------|
| 1 | Setup project environment | under 1 min | Completed |
| 2 | Clone GitHub repository | under 1 min | Completed |
| 3 | Prepare working directories | under 1 min | Completed |
| 4 | Add context MCP server | under 1 min | Completed |
| 5 | Setup Python environment and scan tutorials | approx. 9 min (20:36 to 20:45) | Completed |
| 6 | Execute tutorial notebooks | pending | In progress |
| 7 to 11 | remaining pipeline steps | pending | Not started |

Total cost (`total_cost_usd` from build log): pending, to be filled once the run completes.

## Agent run

The following Mendelian randomization prompt will be run through the completed agent once the build finishes:

> I'm doing Mendelian randomization with rs11174281 as an instrument for lifetime cannabis use (LCU), identified in a within family GWAS. Please use AlphaGenome to look up the variant's chromosome, position, and alleles (build GRCh38 if possible), run variant effect prediction for both alleles across all available modalities, rank tissues by predicted RNA seq effect magnitude with a focus on brain tissues, identify the gene(s) with the largest expression changes and report direction for the risk allele, check for regulatory element overlap in brain tissues, save plots of the regulatory landscape, and summarize the likely gene and mechanism.

Output location: `output/`
Plot location: `output/plots/` (to be confirmed once generated)

## Status

Build in progress at time of writing (step 6 of 11). This README will be updated with final timings, cost, agent output summary, and plot references once the run completes.
