# Texts about the "modified" mark

Two ready-to-paste texts. Both link to `docs/proposals/COSMETIC_EXTENSIONS.md` on `main`, so post them only after that file is merged. The Egosoft forum (phpBB) and Steam Workshop descriptions both use BBCode, so the texts are written in BBCode.

## Egosoft forum post

Where: the X4: Foundations ideas or suggestions board.

**Title:** Suggestion: a "cosmetic extension" class that does not mark saves as modified

```
Hi Egosoft,

I make a small voice mod: it gives Boso Ta a less squeaky voice. It consists of a diff on six entries in libraries/sound_library.xml and 2,324 .ogg files – no scripts, no wares, no AI, no UI. Still, every save made with it is marked "modified" for good, exactly like a save made with a cheat menu.

I know you said years ago that telling cosmetic mods from gameplay mods is tricky. So here is a concrete proposal instead of a complaint:

[list]
[*]Classify unsigned files by path and type with a deny-by-default allowlist (v1: audio files and sound_library.xml diffs; text and textures only as candidates for you to decide; UI/Lua, scripts, libraries, models and shaders excluded).
[*]If every unsigned file of an extension is allowlisted, do not set "modified". List the extension in save metadata and crash logs instead, so support still sees it.
[*]Optionally, a content.xml attribute cosmetic="1" that makes the engine refuse non-allowlisted files from that extension, so an update can never silently mark players' saves.
[/list]

Full write-up with threat model, abuse cases, rollout steps and open questions, plus a small reference classifier (Python, standard library only):
https://github.com/slovi21/x4mod_less_annoying_voices/blob/main/docs/proposals/COSMETIC_EXTENSIONS.md

I would be glad to hear whether something like this is feasible on your side – and which of my assumptions about the engine are wrong.

Thanks for the game, and for keeping it open to mods.
Slovi
```

## Steam Workshop description paragraph

Replaces the current sentence ending in "come on, Egosoft!".

**English (both items):**

```
[b]About the "modified" mark:[/b] Like every mod, this one marks your saves as "modified" – permanently, even after you remove it. That is a bit unfortunate here: the mod only patches six voice entries in libraries/sound_library.xml and adds .ogg files. No scripts, no wares, no AI, no UI – gameplay is untouched. The game currently cannot tell cosmetic mods from gameplay mods; we have written up a concrete suggestion for Egosoft: [url=https://github.com/slovi21/x4mod_less_annoying_voices/blob/main/docs/proposals/COSMETIC_EXTENSIONS.md]cosmetic extension proposal[/url]
```

**German (optional, for the DE item):**

```
[b]Zum Vermerk „modifiziert“:[/b] Wie jede Mod markiert auch diese deine Spielstände als „modifiziert“ – dauerhaft, auch nach dem Entfernen. Hier ist das schade: Die Mod ändert nur sechs Stimmeinträge in libraries/sound_library.xml und bringt .ogg-Dateien mit. Keine Skripte, keine Waren, keine KI, keine Oberfläche – das Gameplay bleibt unberührt. Das Spiel kann kosmetische Mods derzeit nicht von Gameplay-Mods unterscheiden; einen konkreten Vorschlag an Egosoft haben wir hier aufgeschrieben: [url=https://github.com/slovi21/x4mod_less_annoying_voices/blob/main/docs/proposals/COSMETIC_EXTENSIONS.md]Vorschlag „kosmetische Erweiterungen“[/url] (Englisch)
```
