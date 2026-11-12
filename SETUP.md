# GitHub profile dashboard setup

This pack is for GitHub user `munnamihir`. Create or use public repository
`munnamihir/munnamihir`, then add the files from this package to that repo's
DEFAULT BRANCH, preserving directory paths.

Directory tree:

- `README.md`
- `assets/*.svg` and `assets/language-telemetry.json`
- `scripts/refresh_telemetry.py`
- `.github/workflows/refresh-telemetry.yml`

## Initialize the live language donut

1. In GitHub, go to your new profile repo > Actions > "Refresh profile telemetry".
2. Click "Run workflow" and select the default branch.
3. Allow it to commit the generated SVG and language-telemetry.json.
4. If it cannot push, open Settings > Actions > General > Workflow permissions,
   select "Read and write permissions", and retry. This setting can be restricted
   by an organization; do not broaden permissions unnecessarily.
5. After the first successful run, the chart will update weekly on Mondays.

The workflow is free on standard public GitHub repositories subject to GitHub's
normal Actions policies. It only reads publicly visible repository language
statistics and writes a chart/JSON snapshot to the profile repo.

## Supported interactivity

- Native GitHub Markdown `<details>` expand/collapse sections.
- Clickable repository and navigation links.
- Mermaid flow diagram (rendered by GitHub).
- Dynamic GitHub badges from shields.io.
- The auto-updated SVG language chart.

GitHub profile READMEs do not permit arbitrary JavaScript, iframes, or embedded
interactive web apps, so do not expect JavaScript hover effects, a real terminal,
or user-controlled donut slices to work inside a GitHub README.

## Chart data

Focus categories (curated 11-project set):
Security/privacy: 4; reliability/safety: 3; AI/automation: 2; platforms/tools: 2.

Delivery modes: product/tooling: 5; validation/research: 3; protocols/platforms: 3.

The language chart uses GitHub's language API source-byte counts across these 11
public repos. It is *not* a ranking of skills or total engineering work.
