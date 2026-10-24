# Proposal: a "cosmetic extension" class for X4: Foundations

**Status:** suggestion from a mod author for discussion with Egosoft. This is not an Egosoft document. It describes allowlist **v1**; the normative rules are `classify()` in `tools/classify_extension.py`, and this page explains them.

## The problem

Every unsigned extension marks a save as "modified", and the mark stays even after the extension is removed. This mod changes one character's voice. It consists of a diff on six entries in `libraries/sound_library.xml` and 2,324 `.ogg` files. Its saves get exactly the same mark as an economy overhaul or a cheat menu.

Egosoft has acknowledged the difficulty. A community compilation of developer Q&A from 2019 quotes a developer as saying that working out what a mod changes, and whether that affects achievements or gameplay, is "by definition very tricky", and that they wanted to look at solutions without a timescale ([source](https://forums.overclockers.co.uk/threads/x4-foundations.18791409/page-23)). This page is meant as one concrete solution.

## What the mark protects (threat model)

Single-player gameplay is out of scope: what players change in their own single-player game harms nobody else. The mark matters for three things:

1. **Support triage.** Egosoft needs to know whether a bug report comes from a modded game.
2. **Online integrity.** Ventures, and any future online feature or leaderboard, must not be fed by an altered simulation.
3. **Achievements.** Community reports say they still unlock in modified games; listed for completeness.

The proposal follows from that. A file class counts as **cosmetic** if files of that class cannot change the simulation state that ends up in a save or in an online feature. A cosmetic mod can still crash the game, so it must stay **visible** to support. It just should not mark the save.

## Proposed mechanism

### 1. Classify where the game detects unsigned content

We do not know the engine's internals. What we saw: when the game read this mod's unsigned `sound_library.xml` diff, the log showed a signature warning (`docs/phase0-findings.md`, "What was proven in the running game").

- **If the signature check runs per file**, that is the natural place. For every unsigned file, look up its class from path and file type (rules below). An allowlisted file adds the extension to a list of cosmetic extensions. Any other file sets "modified", exactly as today.
- **If the check runs per extension**, apply the same rule to the extension's complete file list, meaning loose files plus catalog index entries, when it is loaded. That is what `tools/classify_extension.py` does.
- `content.xml` is unsigned in every extension and has to be exempt as metadata.

### 2. What is saved and shown

| | Gameplay extension | Cosmetic extension |
|---|---|---|
| Save marked "modified" | yes, permanently (unchanged) | no |
| Listed in save metadata and debug/crash logs | yes | yes, for support |
| Listing persists after removal | yes | no: cosmetic content leaves nothing in the simulation state, so the next save made without it no longer lists it |
| Online features (Ventures) | blocked | Egosoft's decision, see open questions |

An optional small "cosmetic mods active" note in the save/load menu would keep it transparent for players.

### 3. Optional guarantee in `content.xml`

This is a hypothetical attribute that does not exist today:

```xml
<content id="ws_3824406333" name="Boso Ta - new VOICE Will (DE)" version="102" save="0" cosmetic="1">
```

An extension that declares `cosmetic="1"` would have only allowlisted files loaded. Anything else would be skipped and logged. This protects players. Suppose an update accidentally adds a gameplay file. Without the guarantee, every save of every subscriber is marked modified, permanently and silently. With it, the file is not loaded and the author finds the reason in the log. Extensions without the attribute are still classified automatically, so existing cosmetic mods benefit without any change.

### 4. Allowlist v1 (deny by default)

Paths are compared the way Windows resolves them: case-insensitive, `\` equals `/`, and trailing dots and spaces are stripped from each component. Paths with `..`, drive letters, absolute paths or characters Windows forbids are never cosmetic.

| Class | Files | Status | Reason |
|---|---|---|---|
| metadata | `content.xml` in the extension root | core | describes the extension |
| documentation | `*.txt`, `*.pdf`, `*.md` in the extension root | core | believed not to be read by the engine (assumption) |
| audio | `*.ogg`, `*.wav` anywhere; diffs on `libraries/sound_library.xml` | core | verified for this mod in X4 9.00: sample redirect, `is3d`, `noocclusion`. Audio data has no known path back into the simulation; see the open question on speech duration |
| text | `t/*.xml` (directly in `t/`) | **candidate, Egosoft decides** | presentation in most cases, but scripts and the UI read text pages as data |
| texture | `*.dds` outside `ui/` and `assets/fx/` | **candidate, Egosoft decides** | transparent or very bright textures can reveal objects; effect textures (dust, nebula) and UI icons are left out |
| code | everything under `ui/`, `*.lua` anywhere | not cosmetic | Lua can change game state; the Protected UI Mode already treats it separately |
| everything else | `md/`, `aiscripts/`, `maps/`, `index/`, other `libraries/` files, macros and components under `assets/`, models (`.xmf`, which carry collision and connection geometry), shaders, `.gz`, `.mp3`, `.mkv`, `.cur`, unknown types | not cosmetic | gameplay, or not assessable from outside |

Further candidates only Egosoft can assess: `libraries/material_library.xml` and other presentation-only libraries, compressed textures, `.mp3`, `.mkv` (video), `.cur` (cursors).

### 5. Abuse cases considered

- **Disguised file names.** Classification uses path and type together. As far as modders know, a script has to be an `.xml` file in a script folder to be loaded as a script, and that is never allowlisted. A file named `.ogg` should only ever reach the audio decoder; Egosoft can confirm this for its loaders.
- **Windows path tricks.** `md/x.xml.`, `MD\X.XML` and `md/x.xml ` all resolve to `md/x.xml` and are classified as such.
- **Catalogs.** Entries in `.cat` indexes are classified like loose files. A line that does not parse, a missing `.dat`, a `.dat` whose size does not match the index, or a `.dat` without a `.cat` all make the extension non-cosmetic (fail closed).
- **`sound_library.xml` used for advantage.** A diff can make distant sounds audible or remove occlusion. That is an information advantage in single-player, which is out of scope. It does not change the simulation, so online features are not affected.
- **Speech duration.** Re-spoken lines can be longer or shorter than the originals (this mod's German variant). If scripts wait for a line to finish, dialogue timing shifts by seconds. Not verified; see open questions.

### 6. Worked example: this mod

```
> python -I tools/classify_extension.py dist/ws_3824406333

=== dist/ws_3824406333 ===
  audio              1
  metadata           1
verdict: would qualify under the proposed allowlist v1 - not an Egosoft statement
```

`dist/` only holds the XML (the diff and `content.xml`). The folder the Workshop installs, `extensions/ws_3824406333/`, also holds the `.ogg` files, packed into a catalog by the Workshop tool. Run the tool on that folder for the complete picture; the `.ogg` files count as audio as well.

### 7. Rollout suggestion

1. Engine: automatic classification and the cosmetic list, without a new attribute. Every existing audio-only mod benefits immediately.
2. Publish the allowlist in the modding documentation.
3. Add the `cosmetic="1"` guarantee.
4. Decide the candidate classes (text, textures) separately.

The change is backward compatible. Saves that are already modified stay modified, and nothing changes for gameplay extensions.

### 8. Open questions for Egosoft

- Does the signature check run per file or per extension, and where is "modified" set?
- Do mission or AI scripts wait for speech to finish, so that audio length changes timing?
- Which libraries besides `sound_library.xml` are presentation-only?
- Are text pages used by scripts in ways that change the simulation?
- Should cosmetic extensions be allowed with Ventures and future online features?

## Reference implementation

```
python -I tools/classify_extension.py <extension folder> [<extension folder> ...]
```

- `-I` runs Python in isolated mode.
- The arguments are one or more extension folders.
- Exit code 0: every folder would qualify. Exit code 1: at least one would not, or would qualify only with candidate classes. Exit code 2: wrong call, or not an extension folder.
- Only the Python standard library is used.
- Tests: `python -I -m unittest discover -s tests` (`discover` searches the folder given with `-s` for tests).

## Sources

- Developer statement, 2019, as quoted in a community Q&A compilation: [overclockers.co.uk](https://forums.overclockers.co.uk/threads/x4-foundations.18791409/page-23)
- Achievements in modified games, community reports 2018–2023: [Steam 1](https://steamcommunity.com/app/392160/discussions/0/1744479698795164051/), [Steam 2](https://steamcommunity.com/app/392160/discussions/0/1743353164090539301/), [Steam 3](https://steamcommunity.com/app/392160/discussions/0/3164335241614123876/)
- Mark stays after removing mods, community report: [Steam](https://steamcommunity.com/app/392160/discussions/0/3276939184050387907)
- Protected UI Mode, community reports: [Steam](https://steamcommunity.com/app/392160/discussions/0/4626981956824860847)
- Engine behaviour of this mod: `docs/phase0-findings.md`
