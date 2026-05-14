# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/)
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.2.1] - 2026-05-14

### Bug fixes

- rename 'standard' to 'methodology' throughout prompts
- add marketplace.json for plugin discovery
- use explicit github source in marketplace.json
- add required type and title fields to userConfig
- remove version/date from prompt — use git tags and prompt snapshots
- single methodology-snapshot.md instead of two separate files
- separate snapshot files — two for plugin, one for paste
- use relative source './' in marketplace.json instead of github self-ref
- replace userConfig with project-local custom.md override
- correct Ghost domain in article links
- restructure repo to match documented plugin layout
- rename n to runs, add seconds to timestamp (v1.9.1) (#37)
- remove entity IDs from input schema (#47)
- resolve CI failures for ruff, mypy, and markdownlint
- correct schema $id URLs to match actual repo paths
- Step 5 source scorer — batch size 2, top 15 sources, snippet field allowed
- rename config file from .dorc to .diorc
- robust JSON parsing for Haiku trailing text + brevity instruction
- run ruff format on all source files for CI compliance
- add Table of Contents to README.md for standards compliance
- config priority order and MCP setup instructions
- correct MCP setup to use claude mcp add CLI, not settings.json
- scope MCP tool descriptions to research workflows only
- include compiled prompts in plugin directory for skill access
- mandatory dio_search usage when MCP tools are available
- make compile-prompts.py executable (EXE001)
- renderer iteration 1 — broken links, missing audit, raw JSON in group reports
- use topic title in card headings so query confidence has context
- explicit HTML anchors for TOC links (cross-renderer compatible)
- remove redundant meta count table at top of run index
- CI pip-licenses reads from .pip-licenses-allowlist (single source of truth)
- pin lxml>=6.1.0 (CVE-2026-41066) + CodeQL URL assertion (#131)
- run index drops all per-item cards for CLI-format input (#156)
- render CLI-format searches, answers, and confidence (#157 round 1)
- pipeline reports now emit title for run-level index headings
- run ruff/mypy/pytest/audit on host so local matches CI (#160)
- attach CLI stderr log handler so pre-pipeline errors surface (#154)
- disposition every raw search result, validate invariant (#163)
- walk up parent dirs looking for .env (#155)
- pass boolean to ci-security reusable workflow inputs (#203)
- specify language and container-tag in publish-release caller (#206)
- use URL source format in marketplace.json and add version to plugin.json (#216)
- use explicit secret passing for cross-org reusable workflow

### CI

- retrigger after PR body fix for issue linkage
- enforce mypy across src and tests; fix 101 pre-existing test errors
- adopt standard-actions v1.5 reusable workflows (#197)

### Chores

- bump version to 1.2.0 for plugin cache update
- bump to v1.3.0 — custom.md override, userConfig removed
- bump marketplace.json version to 1.5.0
- release v1.6.0 — candidate evidence, pre-fact-check gate (#17)
- release v1.7.0 — source reading list, resources factored out (#21)
- release v1.8.0 — fact-check scorecard, rerun diff (#26)
- release v1.9.0 — n-run default, synthesis, HHMM timestamps (#35)
- release v1.9.1 (#38)
- recompile prompts after PR #95 merge, upgrade pypdf to fix vulns
- restrict Python to 3.14 only, drop 3.12/3.13 CI matrix (#121)
- retrigger CI with updated PR body
- delete ci-push.yml; collapse three-tier CI to two-tier
- migrate standard-actions refs from @develop to @v1.3
- upgrade standard-actions from @v1.3 to @v1.4
- bootstrap st-config.toml for cache-first docker workflow
- seed standard-tooling.toml
- remove legacy st-config.toml (#185)
- add memory management policy (#187)
- strip config sections from repository-standards.md (#188)
- upgrade standard-tooling to v1.4.13 (#189)
- upgrade to standard-actions v1.5 and enable config enforcement (#192)
- remove standard-tooling as a Python dev dependency (#194)
- decommission st-validate-local remnants (#199)
- remove legacy scripts/dev/ validation scripts (#200) (#201)
- fleet-wide config and workflow cleanup (#202)
- shorten issue template header comments to fit yamllint line-length (#204)
- migrate to reusable publish/docs workflows (#205)
- adopt CI/CD workflow naming convention (#383) (#207)

### Documentation

- README — make standalone prompt generic to any AI interface
- README — replace Two Modes with Three Input Types
- README — add links to the two blog posts explaining the methodology
- rewrite install/update instructions with verified commands
- workflow architecture design document (#43)
- add Input Parser as AI sub-agent 0 (#44)
- define research input JSON schema (#45)
- remove config.id from input schema, add output rendering design (#46)
- mark researcher_profile as experimental placeholder (#48)
- define standard sub-agent preamble for input handling (#49)
- remove dedicated Input Parser sub-agent from workflow (#50)
- add product name decision — Diogenes (dio) (#56) (#57)
- add MCP server and dio CLI sections to README
- restructure README with configuration section and key requirements
- fix search provider documentation consistency
- genericize MCP setup step 2 to not reference Serper specifically
- bootstrap docs/specs/ + tech-debt register for PAAD integration
- pushback review of tech-debt-register (PAAD /paad:pushback)
- downgrade standards-and-conventions refs, bump standard-tooling to v1.4

### Features

- v1.0.0 — initial public release
- Rule 6 — required sections are minimum, not maximum
- unify claim and query prompts into single research.md
- add axiom support — declared facts assumed true during research
- add standalone prompt and HTML output mode
- add revisit triggers as mandatory assessment section
- v1.1.0 — remove citation chain analysis, renumber to 11 steps
- add userConfig for custom output format override
- replace claim/query modes with unified 'run' command
- save prompt snapshot in run directory for version traceability
- prompt snapshot in output format — works for all interfaces
- save both prompt and output format snapshots in run directory
- v1.4.0 — implement extract and check commands
- v1.5.0 — fact-check command, confirm=no batch mode, sane defaults
- add 0% and 100% to probability scale for deterministic claims
- add candidate evidence support for claims (#9) (#16)
- add source reading list artifact (#11) (#20)
- add fact-check scorecard to claim runs (#8) (#24)
- generate difference report automatically on rerun (#5) (#25)
- default to n=3 independent runs with synthesis (#32) (#34)
- add Python project infrastructure (#51)
- standard tooling infrastructure setup (#52) (#53)
- rename package to diogenes, register dio CLI entry point (#62)
- CLI argparse skeleton with run/rerun/fact-check subcommands (#63)
- Anthropic API client for sub-agent prompt calls (#64)
- schema validator with input file parsing (#65)
- input-clarifier sub-agent prompt (#66)
- run command + commands package (#67)
- config loader with multi-source API key resolution
- extract common guidelines and prepend to all sub-agent calls
- add hypothesis generator sub-agent and pipeline orchestration
- single source of truth for JSON schemas, injected into prompts
- add search designer sub-agent (Step 3) with schema and pipeline
- add search executor sub-agent (Step 4) with web search tool
- add token usage tracking and fix web search allowed_callers
- redesign Step 4 — Python search execution + LLM result selection
- add cost estimation, Serper.dev provider, and search config
- batched relevance scoring for Step 4 — 93% token reduction
- add source scorer sub-agent (Step 5) with page fetching
- complete pipeline — Steps 6-11 implementation
- switch scoring steps (4b, 5) to Haiku for cost optimization
- enable prompt caching for common guidelines block
- MCP server exposing search and page fetch tools
- move prompts into package and add compile-prompts script
- add schemas for usage, archive, and step output collection
- rewrite SKILL.md Step 5 to use compiled sub-agent prompts with JSON output
- extracted claims output as JSON with schema
- dio render — JSON-to-markdown renderer with CLI and MCP tool
- renderer iteration 2 — rich item index with summary tables
- renderer iteration 3 — run-level index mirrors R0044 card format
- run index — TOC, axiom-first order, separate sections, no zero counts
- restructure per-item index — Summary section, Results rename, TOC
- sub-page titles include topic — '{id} — {topic} — {artifact}'
- universal table of contents on all rendered pages
- denormalize reading list entries so renderer needs no joins
- evidence extraction with verbatim validator (#94)
- pipeline events observability with three-layer capture (#101)
- content cache + dio_validate_packets MCP tool (#102)
- add model identifier and execution path to run outputs (#109)
- constrained JSON decoding via Anthropic structured outputs (#107)
- state-machine-driven pipeline orchestration (#110)
- parallel execution for evidence extraction via parallelize_thread (#89)
- process-parallelism for fetches + complete step name alignment (#124)
- add --cov-fail-under=100 enforcement + 352 unit tests across 11 modules (#131)
- record PID in pipeline-state.json for crash correlation (#123)
- replace prompt-snapshot.md with version metadata in pipeline-state.json (#127)
- exponential-backoff retry for transient API and network failures (#77)
- classify dio_search failures so the agent can offer web_search fallback (#88)
- expose pipeline tuning parameters via .diorc [pipeline] section (#76)
- replace print() with progress logger
- add dio resume for interrupted research runs
- plugin path usage.json schema compliance (minimum slice)
- adopt git worktree convention for parallel AI agent development
- add dio resume --from-step for step-level rerun (#162)
- migrate to diogenes-project/diogenes (#211)

### Refactoring

- rationalize step/file/prompt naming convention (#117)
- run vs rerun, per-instance clarification, remove multi-run (#93)
- narrow self-audit to analytical ROBIS domains only
- migrate to host-level-tool model
- align PR and issue templates with standard-tooling (#208)

### Reverts

- restore Sonnet for all steps — Haiku scoring produced wrong verdicts

### Styling

- Summary section as inline bold-label paragraphs
- apply ruff format to #157 round-1 files (#157)
- fix D403 docstring capitalization + SLF001 sentinel attr (#154)
- apply ruff format to pipeline.py and test_pipeline.py (#163)

### Testing

- add step dispatch + pipeline handler tests, raise coverage to 76% (#131)
- add group-level rendering tests + item type fields, raise coverage to 80% (#131)
- enrich renderer fixtures (robis_audit, verdict_summary, evidence_quality), 81% total (#131)
- close coverage gaps across all modules, reach 98% (#131)
- close branch partials in state_machine, pipeline, commands/run (#131)
- add rich-CLI fixture + helper unit tests, all statements covered (#131)
- add minimal/dict-gaps/assessment-variant fixtures, reach 99% (#131)
- add search/sources/self-audit variant fixtures (#131)
- edge-case fixtures for no-synthesis/no-audit/minimal items (#131)
- add empty-items and item-no-id tests (#131)
- group reading list + robis branches + empty group (#131)
- report-no-bluf + assessment-no-confidence + bare-source branches (#131)
- empty plugin verification + no-synthesis item fixtures (#131)
- defensive guard tests + reading-list unusual priority (#131)
- reach 100% coverage — pragma: no branch on 9 defensive guards (#131)
- fix ruff D205/PT018 in new #157 round-1 test classes
- add defensive-branch coverage for #157 round-1 schema helpers (#157)

### Tune

- Step 5 source scorer batch size to 1 for reliability

### Types

- annotate ambiguous dict literal caught by mypy src+tests (#157)

### Wip

- checkpoint before Step 4 batched relevance scoring redesign
