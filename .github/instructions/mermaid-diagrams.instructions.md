---
applyTo: "**/*.md"
---

# Mermaid diagram instructions

Use Mermaid for diagrams embedded in Markdown. Treat the Mermaid source as a
reviewable architecture artifact, not as an image-only output.

## Authoring

1. Choose the smallest diagram type that explains the decision: `flowchart`,
   `sequenceDiagram`, `classDiagram`, `stateDiagram-v2`, or `erDiagram`.
2. Start every fenced block with the exact diagram declaration on its first
   non-empty line.
3. Use stable, readable node identifiers and quote labels containing spaces,
   punctuation, slashes, parentheses, colons, or comparison operators.
4. Keep one concern per diagram. Prefer several small diagrams over one dense
   diagram, and embed only diagrams that help a human make or review a design
   decision.
5. Use portable Mermaid syntax. Do not use HTML such as `<br>` in labels,
   JavaScript, external images, or renderer-specific CSS.
6. Keep diagrams deterministic: no timestamps, generated IDs, random styling,
   or provider-specific instructions.

## Validation

- Preserve diagrams inside ` ```mermaid ` fences so GitHub can render them.
- Run the repository HLD validator after editing an HLD.
- Use the Mermaid parser or Mermaid CLI (`mmdc`) when available; parser
  validation is the required syntax check, while browser rendering is a
  separate visual check.
- If a local preview is needed, extract the block to a temporary `.mmd` file
  and preview it with the editor or render it with `mmdc`. Do not commit
  temporary extracted files unless the repository explicitly requires them.
- Do not call VS Code-only commands such as `mermaidChart.preview` from a
  shell or GitHub Actions job. They are optional interactive editor features,
  not repository automation APIs.

## HLD-specific rules

- Include a diagram only when it clarifies boundaries, flow, deployment,
  data, or an important decision.
- Name the view in the surrounding Markdown heading or caption, for example
  `Request flow` or `Deployment view`.
- Do not duplicate the same architecture in multiple diagrams. If another
  view is needed, change the perspective rather than redrawing the same flow.
- Keep business and architecture claims traceable to the requirement and
  assembled context. Mark unknown facts as context gaps instead of inventing
  nodes or integrations.

This guidance follows Mermaid's documented syntax and CLI behavior:
https://mermaid.js.org/syntax/
https://mermaid.js.org/config/mermaidCLI
https://github.com/mermaid-js/mermaid-cli
