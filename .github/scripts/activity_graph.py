name: Activity Graph

on:
  schedule:
    - cron: "17 18 * * *"  # daily 01:17 WIB
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - "scripts/activity_graph.py"
      - ".github/workflows/activity-graph.yml"

permissions:
  contents: write

concurrency:
  group: activity-graph
  cancel-in-progress: true

jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Render activity graph SVG
        env:
          GH_TOKEN: ${{ github.token }}
          GH_LOGIN: mulhamna
          OUT: activity-graph.svg
        run: python scripts/activity_graph.py

      - name: Skip commit if unchanged
        id: diff
        run: |
          if git diff --quiet -- activity-graph.svg; then
            echo "changed=false" >> "$GITHUB_OUTPUT"
          else
            echo "changed=true" >> "$GITHUB_OUTPUT"
          fi

      - name: Commit and push SVG
        if: steps.diff.outputs.changed == 'true'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add activity-graph.svg
          git commit -m "chore: update activity graph"
          git push
