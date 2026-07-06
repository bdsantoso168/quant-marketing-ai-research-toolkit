# Task 4: AI Agent from the AlphaGenome Paper (Paper2Agent)

## Deliverable

output/mr_prompt_response.json (full agent response) and output/rs11174281/ (VCF, batch scores CSV, metadata CSV, alphagenome report JSON, and 7 regulatory landscape plots) for the Mendelian randomization prompt on rs11174281, run via AlphaGenome's remote MCP server after a documented pivot from a failed local build.

## Objective

Build an AI agent from the AlphaGenome research paper using the Paper2Agent framework, then run a given Mendelian randomization prompt through the agent and save the output.

## Final approach

Local build (Paper2Agent.sh against the AlphaGenome repo) was attempted first and progressed through steps 1 to 6 successfully, but failed three separate times at step 7 (extract tools from tutorials) under three different conditions: missing envsubst, silent overnight death, and a live hang with sleep prevention confirmed active. Three isolated variables pointing at the same failure step ruled out environment quirks as the cause and indicated a structural issue at that step, likely a large intermediate payload (200KB plus step3_output.json) feeding a nested Claude call that never returned.

Switched to Paper2Agent's hosted remote MCP server for AlphaGenome instead of continuing to patch the local build. This is a documented deviation, not a shortcut taken early. It was earned after real diagnostic effort on the local path.

## Tooling

- Framework: https://github.com/jmiao24/Paper2Agent
- Target paper and repo: https://github.com/google-deepmind/alphagenome
- Remote MCP endpoint used: https://Paper2Agent-alphagenome-mcp.hf.space/mcp
- Execution environment: Claude Code CLI, local terminal
- Auth: Anthropic API key for the claude CLI, no AlphaGenome API key needed once on the remote MCP path since the hosted server handles that

## Environment

- macOS, Apple Silicon
- System bash: 3.2 (Apple ships the last GPLv2 version, no declare -A support)
- Python: 3.13.1
- Claude Code CLI at ~/.local/bin/claude, symlinked from the Claude Desktop bundled binary

## Blockers hit and fixes applied, in order

### 1. claude CLI not on PATH
Symlinked the Claude Desktop bundled binary into ~/.local/bin/claude, avoided npm install -g since it required sudo.

### 2. fastmcp not installed
Installed with pip install --user fastmcp, symlinked into local bin.

### 3. Retired model reference
Paper2Agent hardcodes claude-sonnet-4-20250514 across 6 script files. Returns a 404 against current keys. Patched all 6 to claude-sonnet-4-6, same cost and quality tier intent as the original.

### 4. Bash 3.2 incompatibility
macOS ships bash 3.2, the orchestrator and one sub script use declare -A which needs bash 4 plus. Patched both to avoid associative arrays.

### 5. Unquoted paths break on directories with spaces
Project path included spaces. Sub script invocations broke on word splitting. Symlinked the Paper2Agent directory to a space free path rather than patching every unquoted reference individually.

### 6. envsubst not installed
Not shipped on macOS by default, used in 4 scripts. Wrote a minimal drop in replacement scoped only to the specific substitution patterns Paper2Agent actually uses.

### 7. Step 7 (tool extraction) failed three times at the same checkpoint
- Attempt 1: blocked by the missing envsubst above
- Attempt 2: died silently overnight with no error logged, confirmed via absence of the 05_step3_done marker, not agent narration. Root cause suspected machine sleep interrupting the background shell.
- Attempt 3: hung again with caffeinate active and sleep confirmed prevented, ruling out sleep as the cause. Same file (step3_output.json, 200KB plus) stayed static for over 50 minutes with no progress.

Decision: abandoned the local build at this step and moved to the remote MCP path rather than a fourth attempt.

### 8. Auth failure after switching to remote MCP
claude CLI returned 401 even with a freshly rotated API key. Root cause: default (non bare) mode reads OAuth and keychain credentials in addition to ANTHROPIC_API_KEY, and this machine's Claude Desktop had an active OAuth session that interfered. Fixed by adding --bare to force strict env variable only auth.

### 9. --bare strips MCP config loading
--bare disables project scoped MCP discovery from ~/.claude.json. Fixed by passing an explicit --mcp-config pointing to a standalone JSON file with the alphagenome server definition, combined with --strict-mcp-config.

### 10. Recurring empty environment across shell sessions
ANTHROPIC_API_KEY and PATH reset every time a new terminal tab or shell was opened, since /tmp/task4_secrets.env was never sourced automatically. This caused multiple silent failures (empty output files, "Not logged in" errors) that looked like new bugs but were actually the same root cause repeating. Fixed by chaining source and export directly before every claude invocation in a single command, and by adding an automatic source line to ~/.zshrc going forward.

## Resume behavior observed

The local pipeline tracks step completion via markers and skips cleanly on rerun. Steps 1 through 6 skipped correctly on every relaunch after a failure, meaning each fix only cost a rerun from the failure point forward, not from step 1.

## MCP connection verification

Before running the research prompt, tool availability was confirmed with actual evidence, not assumed from a health check. A forced short delay before the first real turn let the async MCP handshake complete, after which claude mcp list showed alphagenome as connected and a tool listing call returned 18 alphagenome tools covering variant scoring, in silico mutagenesis analysis, DNA sequence prediction, and visualization across chromatin accessibility, contact maps, gene expression, histone marks, splicing, and transcription factor binding.

## Research prompt run

The Mendelian randomization prompt was run against the connected remote MCP agent:

"I'm doing Mendelian randomization with rs11174281 as an instrument for lifetime cannabis use (LCU), identified in a within family GWAS. Please use AlphaGenome to look up the variant's chromosome, position, and alleles (build GRCh38 if possible), run variant effect prediction for both alleles across all available modalities, rank tissues by predicted RNA seq effect magnitude with a focus on brain tissues, identify the gene(s) with the largest expression changes and report direction for the risk allele, check for regulatory element overlap in brain tissues, save plots of the regulatory landscape, and summarize the likely gene and mechanism."

Output was independently verified by a second agent instance (Cowork) that had not produced the run, cross checking file contents against the report's stated coordinates, gene names, tissue rankings, and plot filenames. All checks passed.

## Output files

| Path | Size |
|---|---|
| output/mr_prompt_response.json | 9.8 KB |
| output/rs11174281/rs11174281.vcf | 97 bytes |
| output/rs11174281/rs11174281_metadata.csv | 868 KB |
| output/rs11174281/rs11174281_batch_scores.csv | 6.4 MB, 25,090 rows |
| output/rs11174281/rs11174281_alphagenome_report.json | 9.4 KB |
| output/rs11174281/rs11174281_chromatin_brain.png | 360 KB, 5668x1407 |
| output/rs11174281/rs11174281_gene_expr_brain.png | 1.4 MB, 6602x6027 |
| output/rs11174281/rs11174281_histone_brain.png | 1.9 MB, 5860x5334 |
| output/rs11174281/rs11174281_splicing_brain.png | 148 KB, 5369x945 |
| output/rs11174281/rs11174281_lrrk2_interval_rna_seq_plot.png | 508 KB, 6419x2268 |
| output/rs11174281/rs11174281_lrrk2_interval_rna_seq_plot_zoomed.png | 620 KB, 6405x2268 |
| output/rs11174281/rs11174281_variant_effects_brain_effects_20260624_085045.png | 4.3 MB, 6602x11508 |

## Scientific findings

Variant identity, GRCh38, confirmed via Ensembl: chr12:39,917,691, REF=C, ALT=T/A, MAF(T)=14.5%, intron variant in SLC2A13, upstream of LRRK2. Risk allele modeled as T.

Effect prediction across all modalities: 25,089 tracks across 11 modalities scored in a 1MB window. Strongest signals: splice junctions (mean absolute quantile score 0.973, nearly all positive, SLC2A13 junction usage up), ATAC (0.821, mostly positive), PROCAP (0.729, mostly negative), histone ChIP (0.626), DNase (0.626, mixed), RNA seq (0.547, gene and tissue dependent).

RNA seq, brain tissues ranked by effect magnitude: dorsolateral prefrontal cortex ranked highest (SLC2A13 up), followed by amygdala, cerebellum, caudate, hypothalamus, anterior cingulate, frontal cortex, temporal lobe, putamen, substantia nigra, nucleus accumbens, whole brain, and glutamatergic neurons. LINC02555 is down in most limbic and striatal regions. SLC2A13 is up in prefrontal, temporal, and reward related regions.

Largest expression changes for the risk allele: LINC02555, a long noncoding RNA, is consistently down across amygdala, caudate, hypothalamus, cingulate, frontal cortex, putamen, substantia nigra, nucleus accumbens, and dorsolateral prefrontal cortex. SLC2A13 is consistently up in dorsolateral prefrontal cortex, temporal lobe, nucleus accumbens, anterior cingulate, and substantia nigra. LRRK2 antisense transcript is down broadly. LRRK2 itself shows mixed and inconsistent direction. KIF21A is up, strongest in cerebellum.

Regulatory element overlap: DNase accessible in cerebellum and frontal cortex, closed in glutamatergic neurons, neuronal stem cells, dorsolateral prefrontal cortex, posterior cingulate, and caudate. Enhancer marks (H3K4me1 and H3K27ac) are increased in hippocampus, substantia nigra, cingulate gyrus, dorsolateral prefrontal cortex, caudate, and temporal lobe, suggesting the variant overlaps a predicted active enhancer in dopaminergic and reward circuitry.

Best guess mechanism: rs11174281 T likely activates an intronic enhancer in the SLC2A13 to LRRK2 corridor, driving SLC2A13 up and LINC02555 down in striatal, prefrontal, and limbic circuits including caudate, putamen, nucleus accumbens, dorsolateral prefrontal cortex, and substantia nigra, the same circuitry underlying reward and executive control over drug use. SLC2A13 is a glucose and myo inositol transporter and may alter phosphoinositide signaling that intersects endocannabinoid and dopamine pathways. Loss of LINC02555 may de repress neuronal programs tied to motivational salience.

Caveats stated in the model output: these findings are in silico predictions, the true GWAS risk allele should be confirmed independently, LINC02555 function is uncharacterized, LRRK2 effects were inconsistent across tissues, and the proposed intronic mechanism needs experimental validation.

## Status

Complete. Output independently verified across two separate agent instances rather than relying on a single self report.
