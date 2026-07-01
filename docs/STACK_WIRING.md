# Stack Wiring & Swap Guide — csvkit

<!-- How the runtime components glue together, and EXACTLY what to change to swap -->
<!-- any one of them. The mental model: identify the CONTRACTS between components; -->
<!-- hold a contract on a seam and you can swap freely on either side. -->
<!-- Keep this verified against the live code; cite real files/lines. -->

> **What this is:** how the runtime components connect, and what to change to
> swap any one of them. Complements [`PRD.md`](PRD.md) §4 (Architecture) (high-level);
> this doc is the integration-seam detail.
>
> **As-built, verified against the live code on 2026-07-01.** Re-verify with the
> toolkit in §6 if the code has moved since.

---

## 1. The request chain (who calls whom)

<!-- A small ASCII diagram of the components and the direction of calls. -->
<!-- Show ports/addresses and the one-line role of each box. -->

```
{{COMPONENT_A}}        {{COMPONENT_B}}            {{COMPONENT_C}}          {{COMPONENT_D}}
{{A_ROLE}}             {{B_ROLE}}                 {{C_ROLE}}               {{D_ROLE}}
   ──────────────▶        ──────────────▶            ──────────────▶
```

<!-- Note any second path that touches a key component differently -->
<!-- (e.g. a side request that bypasses the main hub). -->

> **Key fact:** {{ONE_LOAD_BEARING_FACT}} (e.g. which component owns the provider
> config; which component is provider-agnostic).

---

## 2. Swappable components

<!-- THE core table. One row per swappable piece. For each: where it is -->
<!-- configured, how to swap it, and the gotcha that bites you. -->

| Component | Where configured | How to swap | Gotchas |
|---|---|---|---|
| {{LLM_PROVIDER}} | {{WHERE}} (e.g. `{{CONFIG_FILE}}`: `{{ENV_VAR}}`) | {{HOW_TO_SWAP}} | {{GOTCHA}} |
| {{AGENT_HOST}} | {{WHERE}} | {{HOW_TO_SWAP}} | {{GOTCHA}} |
| {{DATASTORE}} | {{WHERE}} | {{HOW_TO_SWAP}} | {{GOTCHA}} |
| {{AUTH}} | {{WHERE}} | {{HOW_TO_SWAP}} | {{GOTCHA}} |
| {{WEB_FRAMEWORK}} | {{WHERE}} | {{HOW_TO_SWAP}} | {{GOTCHA}} |
<!-- | {{COMPONENT}} | {{WHERE}} | {{HOW_TO_SWAP}} | {{GOTCHA}} | -->

---

## 3. The contracts (the only things that must hold)

<!-- List the interfaces that make swaps safe. Anything is swappable as long as -->
<!-- the contract on its seam is preserved. This is the heart of the swap guide. -->

Everything is swappable as long as these interfaces are preserved:

1. **{{CONTRACT_1}}** — {{WHAT_IT_IS}} (between {{SIDE_A}} and {{SIDE_B}}). Any
   implementation honoring it works.
2. **{{CONTRACT_2}}** — {{WHAT_IT_IS}}.
3. **{{CONTRACT_3}}** — {{WHAT_IT_IS}}.

Change a component on one side of a contract, keep the contract, and nothing else moves.

---

## 4. Gotchas (verified)

<!-- CROSS-CUTTING traps that are NOT tied to a single swappable-component row in §2. -->
<!-- These are the things that bite you regardless of which piece you touch: an -->
<!-- artifact that is generated (not hand-edited); two code paths that consume the -->
<!-- same dependency differently (a swap must satisfy BOTH); an ephemeral mount that -->
<!-- re-seeds on every boot. Verify each against the live code before listing it. -->

- **{{GOTCHA}}** — {{WHY_IT_BITES_AND_WHAT_TO_DO}}. <!-- e.g. `{{FILE}}` is generated, not hand-edited -->
- **{{GOTCHA}}** — {{WHY_IT_BITES_AND_WHAT_TO_DO}}. <!-- e.g. two paths touch {{DEP}} differently; a swap must satisfy both -->
- **{{GOTCHA}}** — {{WHY_IT_BITES_AND_WHAT_TO_DO}}.

<!-- If none have surfaced yet, say "None verified yet." Add as the code teaches you. -->

---

## 5. Config knobs, by file

<!-- A by-file index of where the wiring knobs live and whether each file is -->
<!-- tracked or gitignored. Critical for "what do I actually edit". -->

| File | Tracked? | The wiring knobs it holds |
|---|---|---|
| `{{CONFIG_FILE}}` | {{tracked/gitignored}} | {{KNOBS}} |
| `{{CONFIG_FILE}}` | {{tracked/gitignored}} | {{KNOBS}} |

---

## 6. Discovery / verification toolkit (all read-only)

<!-- Copy-pasteable read-only commands to discover the current wiring and -->
<!-- prove each contract holds. Keep these non-mutating. -->

```bash
# The swap knobs (provider / model / datastore / agent bindings):
{{COMMAND_TO_SHOW_BINDINGS}}

# The exact payload/contract crossing the main seam:
{{COMMAND_TO_SHOW_SEAM}}

# Prove a swappable dependency speaks the expected contract:
{{COMMAND_TO_PROBE_DEPENDENCY}}

# Live port / process wiring while running:
{{COMMAND_TO_SHOW_LIVE_PORTS}}
```

The mental model: **the contracts in §3**. Hold the contract on a seam and swap
freely on either side.
