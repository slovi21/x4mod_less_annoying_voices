# How the Boso Ta voice mod works

This page is for people who play X4 and want to know what the mod does to their game, without any programming background.

## The problem

Boso Ta is the Boron scientist who lives in a water tank at your headquarters and talks to you a lot. His voice is very high and squeaky. The game offers no way to change a single character's voice; the only control is one volume slider for all speech.

## How the game plays a voice line

Picture a library.

- Every sentence a character can say is stored as a small sound file. Boso Ta has 2,324 of them in German and 1,750 in English.
- A catalogue tells the game, for every character, which shelf holds their files, how loud to play them, and whether the sound should come from a particular direction in the room.
- When Boso Ta is supposed to speak, the game looks him up in the catalogue, walks to his shelf, takes the right file and plays it.

## What the mod changes

The mod does not alter a single original file. It does two things.

1. **It adds a shelf of its own.** On that shelf are copies of Boso Ta's sentences that went through a sound processing program. The voice was lowered by one octave without slowing it down, given a slightly alien colour, and tuned so that it stays easy to understand in the noise of a space station. Every sentence is exactly as long as before, so his mouth movements and the flow of dialogue still match.
2. **It pins a note into the catalogue.** The note says: "Take Boso Ta's sentences from the mod's shelf, not from the original one." It also says that his conversations should no longer be played as coming from a point in the room. Before that change he got quieter and muffled as soon as you turned your back to him or he was behind the glass of his tank.

That is all. Every other character, every sound effect and the music stay as they are. One other character, the Boron faction representative, is voiced by the same actor and uses the same shelf, so he gets the new voice as well.

## Why this is not a simple download in the repository

The processed sound files are copies of Egosoft's recordings. That is why they are not stored in the public project. The project contains the recipe instead: a small program fetches the originals from your own copy of the game, processes them, and puts them on the mod's shelf. That takes about ten minutes on your own PC. If someone hands you the finished mod as a package, you need none of this; the files are already inside.

## What "modified" means

Egosoft seals its own game files with a kind of signature. As soon as the game loads a file without that seal, and the mod's note is such a file, it switches to "modified" mode. This is what is known about the consequences.

- Any save you make while modified stays marked as modified, even if you remove the mod later.
- The online Ventures feature is not available in modified saves.
- Steam achievements keep working. Egosoft does not say so officially, but players have reported it consistently for years, most recently in early 2026. The only exceptions are the two achievements tied to Ventures, and those can reportedly not be earned by anyone any more, with or without mods.

This is true for every mod, including everything from the Steam Workshop. No mod can carry Egosoft's seal, and the game cannot tell a voice mod from a cheat. If an unmarked save matters to you, keep one that never had mods. How the game could tell cosmetic mods apart is described in `docs/proposals/COSMETIC_EXTENSIONS.md`.

## Removing the mod

Delete the mod's folder from the game's `extensions` folder. The game no longer finds the note and goes back to the original shelf. Your saves keep working, but they keep the "modified" mark.

## In short

| Question | Answer |
|---|---|
| What changes? | Where the game fetches Boso Ta's voice from, and how it is placed in the room. |
| Are original files touched? | No. |
| Other characters? | Only the Boron representative, who shares the voice actor. |
| What do I need? | To build it yourself: Python and ffmpeg. As a packaged download: nothing. |
| Does the game count as modified? | Yes, like with any mod, and saves keep the mark. No Ventures. Steam achievements keep working (player reports up to 2026). |
| Undo? | Delete the folder. |
