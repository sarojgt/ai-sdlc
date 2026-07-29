# GitHub Copilot model catalog

Use the `Model ID` value directly in the HLD workflow. Availability depends on
the Copilot plan, client, organization policy, and model lifecycle. The tiers
below are internal routing guidance, not official pricing or a guarantee that a
model is free.

For automation, the equivalent machine-readable catalog is
[`copilot-model-catalog.json`](copilot-model-catalog.json).

## Recommended demo models

| Tier | Generator | Reviewer | Why |
|---|---|---|---|
| Economical | `claude-haiku-4.5` | `gemini-3.5-flash` | Lower-cost candidate for small HLDs and routine review |
| Economical | `gpt-5-mini` | `mai-code-1-flash` | Alternative low-cost demo pairing |
| Balanced | `gpt-5.6-terra` | `claude-sonnet-4.6` | More capable design and review pairing |
| Advanced | `gpt-5.6-sol` | `claude-opus-4.8` | Complex or large architecture work |
| Automatic | `auto` | Use a different explicit model | Let Copilot choose the available generator model |

## Full model list

| Model ID | Provider | Routing tier | Auto selection | Demo candidate |
|---|---|---:|:---:|:---:|
| `auto` | GitHub | economical | yes | yes |
| `gpt-5-mini` | OpenAI | economical | yes | yes |
| `gpt-5.4-mini` | OpenAI | economical | yes | yes |
| `claude-haiku-4.5` | Anthropic | economical | yes | yes |
| `gemini-3.5-flash` | Google | economical | no | yes |
| `mai-code-1-flash` | Microsoft | economical | yes | yes |
| `raptor-mini` | GitHub | economical | yes | yes |
| `gemini-3-flash` | Google | economical | no | yes |
| `gpt-5.4` | OpenAI | balanced | yes | no |
| `gpt-5.6-terra` | OpenAI | balanced | no | no |
| `gpt-5.6-luna` | OpenAI | balanced | no | no |
| `claude-sonnet-4.5` | Anthropic | balanced | no | no |
| `claude-sonnet-4.6` | Anthropic | balanced | yes | no |
| `gemini-2.5-pro` | Google | balanced | no | no |
| `gemini-3.6-flash` | Google | balanced | no | no |
| `gpt-5.3-codex` | OpenAI | advanced | yes | no |
| `gpt-5.5` | OpenAI | advanced | no | no |
| `gpt-5.6-sol` | OpenAI | advanced | no | no |
| `claude-opus-4.5` | Anthropic | advanced | no | no |
| `claude-opus-4.6` | Anthropic | advanced | no | no |
| `claude-opus-4.7` | Anthropic | advanced | no | no |
| `claude-opus-4.8` | Anthropic | advanced | no | no |
| `claude-opus-5` | Anthropic | advanced | no | no |
| `claude-sonnet-5` | Anthropic | advanced | no | no |
| `gemini-3.1-pro` | Google | advanced | no | no |
| `kimi-k2.7-code` | Moonshot | advanced | no | no |
| `grok-4.5` | xAI | advanced | no | no |

## Selection rules

- The generator and reviewer must use different model IDs.
- Use economical models for small/demo initiatives.
- Use balanced models when the impact assessment identifies multiple services,
  integrations, or meaningful data/security concerns.
- Use advanced models for large, cross-domain, high-risk, or ambiguous work.
- `auto` is suitable for generation, but use an explicit different reviewer
  model to preserve independent review.
- If a model is unavailable, choose another model from the same tier or use
  `auto` where supported.

Source: [GitHub supported AI models](https://docs.github.com/en/copilot/reference/ai-models/supported-models). Verify current availability before use.
