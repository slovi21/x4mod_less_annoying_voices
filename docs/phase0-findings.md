# Verified facts about X4 9.00 voice playback

Everything on this page was checked against the game files or observed in the running game on 2026-10-22. Game folder `C:\Steam\steamapps\common\X4 Foundations`, version 9.00 (`version.dat` = 900), interface language 49 = German. Files were pulled from the catalogs with `tools/x4cat_extract.py`; every MD5 matched.

## Catalog format

- `NN.cat` is a text index with one line per file: relative path, size in bytes, modification time, MD5.
- `NN.dat` holds the files back to back in index order without padding, so the offset of entry *i* is the sum of the sizes of entries 0 … *i*−1.
- `01.cat` … `09.cat` are mounted in order; a later catalog overrides an earlier one. DLCs ship `extensions/<dlc>/ext_NN.cat`, whose contents are mounted relative to the extension folder.

## Where Boso Ta's voice is defined

| Fact | Evidence |
|---|---|
| Voice set is page **10201**, titled "Boron NPC 1 / Boron rep / Misc Plot Characters" | Mission scripts speak Boso Ta with `$actor='$BosoTa', $speak=<id>`; the ids 302360401, 302360101 and 30253525 exist as `voice-l044/10201/{comm,comm_broadcast,comm_npc}/<id>.ogg` |
| The page is assigned per actor, not per character macro | `md/x4ep1_mentor_subscription.xml` lines 117 and 876, `md/story_boron.xml` line 2049 and `md/scenario_advanced.xml` line 32 all create the actor with `<page exact="10201"/>`; the NPC macro `character_boron_hq_mentor_macro` has no page |
| The page is stored in the save file | `<component class="npc" macro="character_boron_hq_mentor_macro" … page="10201">` in `save_002.xml.gz`; `md.xsd` offers no action to change it later |
| Only one other speaker uses the set | `extensions/ego_dlc_boron/libraries/characters.xml` line 55 assigns 10201 to `factionrepresentative_boron`; the set has 1,681 plot lines and only 71 generic lines in English (real random sets such as 10202 have 488), so the engine cannot use it for random NPCs |
| Six sound entries, none with effects | `10201_normal`, `10201_normal_npc`, `10201_comm`, `10201_comm_signalleak`, `10201_comm_npc`, `10201_comm_broadcast` in `libraries/sound_library.xml` (`08.cat`, lines 12079–12110); each has only `<sample>` and in some cases `<volume>` |
| No DLC patches these entries | all seven `extensions/ego_dlc_*/ext_03.cat` contain a `sound_library.xml` diff; none mentions `10201_` |
| Audio lives only in the base catalogs | no `voice-l0xx/` paths in any DLC catalog |

Line counts for page 10201, `normal` context: German 2,324, English 1,750. The 574 German-only lines are pilot and crew phrases (ids 10001 and up, "Enemy spotted", "We were hit") that were never recorded in English for this set. Greetings and small talk (2001–2014, 7001–7010, 11201–12118) exist in both languages. File names are the speak ids, not line numbers within the page.

## What the engine exposes in `sound_library.xml`

From `libraries/sound_library.xsd` (`08.cat`). `<effects>` is `xs:all`, so each child appears at most once and order does not matter.

| Element | Attributes | Notes |
|---|---|---|
| `doppler` | `factor` | |
| `fade` | `in`, `out` | seconds |
| `filter` | `mode` = lowpass, bandpass, highpass, notch; `frequency` 0–1; `oneoverq` 0–1.5; `distance` | the game uses lowpass with `frequency` 0.05–0.5 for muffled sounds |
| `reverb` | `room` preset, `roomsize` 1–100 ft, `drymix` 0–100 %, `density` 0–100 % | presets include `padded cell`, `carpeted hallway`, `sewer pipe`, `underwater` |
| `pitch` | `start`, `end`, `steps` | example in the game: `<pitch start="0.8" end="1.0" steps="1"/>` |

There is no equalizer and no tempo-preserving pitch shifter. `pitch` is a resampling factor: 0.5 is one octave down **and** half speed.

Useful `<sound>` attributes: `is3d` (positional playback with distance attenuation), `noocclusion` (skip geometry muffling), `preload`, `repeat`, `tags`.

## What was proven in the running game

| Claim | How it was tested |
|---|---|
| An unsigned extension diff on `sound_library.xml` is applied; failed selectors log "No matching node" | log shows the extension's file being read (signature warning only); replacing `<volume start>` with 0.03 made Boso nearly silent |
| `<effects><pitch>` works on speech and changes speed with it | pitch 0.3–0.35 on the flight-school tutor: "extremely slow and deep" |
| `<sample start>` can point into an extension folder, and the engine takes the path **literally** | tutor entries pointed at `extensions\<mod>\voice\10190\…`; the folder `voice\` held Betty's files, `voice-l049\` held Boso's; the tutor spoke with Betty's voice |
| Positional playback and occlusion can make a dark voice unintelligible | facing Boso: 90 % of Karee's loudness; back turned: 60 % and unintelligible, with bit-identical files; fixed with `is3d="0"` and `noocclusion="true"` |
| Equal measured loudness is not equal perceived loudness in the game | processed files at −22 LUFS like the originals were "far too quiet"; above 1 kHz they carried 11 dB less energy |
| Swapping a mod while the game runs silences the voice | the loaded diff pointed at a folder that had just been deleted; nothing appears in the log |

## Diff syntax that worked

```xml
<replace sel="/soundlibrary/sound[@id='10201_normal']/sample">
  <sample start="extensions\bosota_voice_alien\voice\10201\normal"/>
</replace>
<add sel="/soundlibrary/sound[@id='10201_normal']" type="@noocclusion">true</add>
<replace sel="/soundlibrary/sound[@id='10201_normal']/@is3d">0</replace>
```

Adding an attribute that already exists is an error; `10201_comm_signalleak` already carries `noocclusion="true"`, so it is left out of the add.

## User environment

- User folder: `C:\Users\slovi\OneDrive\Documents\Egosoft\X4\34818113\`. The extension enable table is machine specific, `content-MSI-PRODP20Z.xml`, not `content.xml`.
- `-logfile debuglog.txt` writes to that folder; `-debug all` slows loading noticeably and is only needed for file I/O messages. `-skipintro` skips the intro videos. `-voicelanguage 44|49` switches the voice track independently of the interface language. All strings verified in `X4.exe`.
- Only two voice tracks exist in the game data: `voice-l044` (English) and `voice-l049` (German).
