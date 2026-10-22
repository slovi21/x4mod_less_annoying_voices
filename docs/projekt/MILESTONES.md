# Milestones – Boso Ta voice mod for X4: Foundations

Goal: Boso Ta's voice stops being annoying while his dialogue stays intelligible and in sync. Started 2026-10-22 from the research handoff in `docs/X4_Boso_Ta_Voice_Mod_Handoff.md`.

| # | Milestone (outcome) | Acceptance criterion (checkable from outside) | Status |
|---|---|---|---|
| 1 | The engine's effect schema and Boso Ta's sound entries are documented | `docs/phase0-findings.md` names the voice page, the six sound ids and the XSD-backed effect list | **reached** 2026-10-22 |
| 2 | A test extension audibly changes a voice through `<effects>` | game starts without "No matching node"; a speaker is clearly deeper | **reached** 2026-10-22 (flight-school tutor with pitch 0.3: "extremely slow and deep") |
| 3 | Boso Ta is no longer annoying in the German track and stays intelligible | Slovi's verdict at the HQ, facing him, back turned, and during background chatter; parameters frozen in `config/variants.json` | **reached** 2026-10-22 ("that works now"; variant `d12_alien_mid`, +9 dB, 2D playback) |
| 4 | An English variant with its own strength | same test with `-voicelanguage 44` | **reached** 2026-10-22 (half strength, +4 dB; verdict "fits", level corrected by 2 dB) |
| 5 | Both variants are packaged and documented; the validator passes | `python -I tools/validate_mod.py` reports 0 errors; README covers building, installing, removing and distributing | in progress – docs rewritten in English, Workshop upload pending |
| 6 | Audio redirect proven as the delivery mechanism | processed files load through a `<sample>` redirect, lip sync intact | **reached** 2026-10-22 (diagnostic v6, installed variants) |

## Change log

- 2026-10-22 – Plan created by the orchestrator from the handoff. Proposal accepted: German before English, because Slovi plays in German.
- 2026-10-22 – Milestone 2 reworded from "Betty's voice" to "a voice" (wording only): the proof came from the flight-school tutor because that scenario loads in seconds.
- 2026-10-22 – **Goal changed by Slovi:** "deeper and warmer" through engine effects was not enough ("still unpleasantly squeaky"). New goal: "not annoying, intelligible", delivered through processed audio. Milestone 3 reworded, milestone 6 promoted from optional to the main path.
- 2026-10-22 – Milestone 4 reinstated by Slovi after hearing the English original ("the English voice needs at most half the correction").
