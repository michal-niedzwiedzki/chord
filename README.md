# chord

A command-line tool for Linux that plays named musical chords instantly.
Useful for quickly checking how a chord sounds without opening a DAW or reading sheet music.

## Requirements

```bash
sudo apt install python3 python3-mido fluidsynth fluid-soundfont-gm
```

## Installation

Build and install the Debian package:

```bash
make deb
sudo dpkg -i ../chord_0.1.0-1_all.deb
```

Or install directly without packaging:

```bash
make install   # copies src/chord to /usr/local/bin/chord
make install-local   # per-user install to ~/.local/bin/chord (no sudo)
```

---

## Basic usage

```bash
chord CHORD [CHORD ...] [OPTIONS]
```

Play a single chord:

```bash
chord Cmaj7
```

Output:
```
Cmaj7         C E G B                   whole             @ 144 BPM
```

Play a progression:

```bash
chord Dm G7 Cmaj7
```

Output:
```
Dm            D F A                     whole             @ 144 BPM
G7            G B D F                   whole             @ 144 BPM
Cmaj7         C E G B                   whole             @ 144 BPM
```

Each chord is played in sequence inside a single MIDI file — transitions are seamless and respect the tempo exactly.

---

## Chord notation

### Root notes

Any of `A B C D E F G`, with optional sharps (`#`) or flats (`b`):

```
C   D   E   F   G   A   B
C#  D#     F#  G#  A#
Db  Eb  Fb  Gb  Ab  Bb
```

### Qualities

Append a quality suffix directly after the root:

| Suffix | Name | Intervals |
|--------|------|-----------|
| *(none)* | Major | 1 3 5 |
| `m` / `min` | Minor | 1 ♭3 5 |
| `maj7` / `M7` | Major 7th | 1 3 5 7 |
| `7` | Dominant 7th | 1 3 5 ♭7 |
| `m7` / `min7` | Minor 7th | 1 ♭3 5 ♭7 |
| `maj9` / `M9` | Major 9th | 1 3 5 7 9 |
| `9` | Dominant 9th | 1 3 5 ♭7 9 |
| `m9` / `min9` | Minor 9th | 1 ♭3 5 ♭7 9 |
| `maj11` | Major 11th | 1 3 5 7 9 11 |
| `11` | Dominant 11th | 1 3 5 ♭7 9 11 |
| `m11` / `min11` | Minor 11th | 1 ♭3 5 ♭7 9 11 |
| `maj13` | Major 13th | 1 3 5 7 9 11 13 |
| `13` | Dominant 13th | 1 3 5 ♭7 9 11 13 |
| `m13` / `min13` | Minor 13th | 1 ♭3 5 ♭7 9 11 13 |
| `dim` | Diminished | 1 ♭3 ♭5 |
| `dim7` | Diminished 7th | 1 ♭3 ♭5 ♭♭7 |
| `m7b5` | Half-diminished | 1 ♭3 ♭5 ♭7 |
| `aug` | Augmented | 1 3 ♯5 |
| `aug7` | Augmented 7th | 1 3 ♯5 ♭7 |
| `sus2` | Suspended 2nd | 1 2 5 |
| `sus4` | Suspended 4th | 1 4 5 |
| `6` | Major 6th | 1 3 5 6 |
| `5` | Power chord | 1 5 |
| `add9` | Add 9 | 1 3 5 9 |
| `add11` | Add 11 | 1 3 5 11 |
| `mMaj7` | Minor-major 7th | 1 ♭3 5 7 |
| `7b5` | Dominant 7 flat 5 | 1 3 ♭5 ♭7 |
| `7#5` | Dominant 7 sharp 5 | 1 3 ♯5 ♭7 |
| `7b9` | Dominant 7 flat 9 | 1 3 5 ♭7 ♭9 |
| `7#9` | Dominant 7 sharp 9 (Hendrix) | 1 3 5 ♭7 ♯9 |
| `7#11` | Dominant 7 sharp 11 (Lydian dom.) | 1 3 5 ♭7 ♯11 |
| `9#11` | Dominant 9 sharp 11 | 1 3 5 ♭7 9 ♯11 |

Run `chord --list-chords` to see all supported qualities with their exact semitone intervals.

### Slash notation

**Bass note** — a different note in the bass:

```bash
chord C/G      # C major with G in the bass
chord Dm7/F    # D minor 7 with F in the bass
```

**Added degree** — append a chord tone by scale degree number:

```bash
chord Dm7/9    # D minor 7 with added 9th (= Dm9)
chord C7/13    # C dominant 7 with added 13th
```

**Altered tension** — sharp or flat a specific degree:

```bash
chord C7/#9    # C dominant 7 sharp 9 — the Hendrix chord
chord C7/b9    # C dominant 7 flat 9
chord C7/#11   # C dominant 7 sharp 11 — Lydian dominant
```

---

## Durations

Append `:N` to any chord token to set its duration. Uses standard note-value denominators:

| Suffix | Name | Beats |
|--------|------|-------|
| `:1` | Whole note | 4 |
| `:2` | Half note | 2 |
| `:4` | Quarter note | 1 |
| `:8` | Eighth note | 0.5 |
| `:16` | Sixteenth note | 0.25 |

Add `.` for dotted values: `:2.` = dotted half (3 beats), `:4.` = dotted quarter (1.5 beats).

Without a suffix, the chord uses the global default (whole note unless overridden with `--duration`).

```bash
chord Dm:2 G7:4 G7:4 Cmaj7:1    # half, quarter, quarter, whole
chord Dm:2. G7:4 Cmaj7:2         # dotted half, quarter, half
chord Dm G7 Cmaj7 --duration 4   # all quarters
```

---

## Rests

Use `-` as the chord name to insert silence. The same duration syntax applies:

```bash
chord Dm:2 -:2 G7:4 -:4 Cmaj7:1   # half rest, quarter rest
chord - G7 Cmaj7                    # whole-note rest before progression
```

---

## Tempo

### Italian markings

Pass `--tempo MARKING` or use the marking directly as a flag:

```bash
chord Dm G7 Cmaj7 --tempo andante
chord Dm G7 Cmaj7 --allegro
```

| Flag | BPM |
|------|-----|
| `--larghissimo` | 20 |
| `--grave` | 35 |
| `--largo` | 50 |
| `--larghetto` | 63 |
| `--adagio` | 72 |
| `--andante` | 92 |
| `--andantino` | 96 |
| `--moderato` | 114 |
| `--allegretto` | 120 |
| `--allegro` | 144 *(default)* |
| `--vivace` | 172 |
| `--presto` | 192 |
| `--prestissimo` | 208 |

### Explicit BPM

```bash
chord Dm G7 Cmaj7 --bpm 120
```

---

## All options

```
chord [CHORD[:DUR] ...] [OPTIONS]

  -d, --duration N[.]     Default note duration for chords without a suffix
                          (default: 1 = whole note)
  -r, --repeat N          Repeat each chord N times (default: 1)
  -g, --gain G            FluidSynth master gain, float (default: 0.8)
  -v, --velocity V        MIDI note velocity 1-127 (default: 100)
      --bpm N             Tempo in BPM
      --tempo MARKING     Italian tempo marking
      --allegro           Shorthand for --tempo allegro (and so on for all markings)
      --list-chords       Print all supported chord qualities and exit
```

### Volume and dynamics

`--gain` controls FluidSynth's master output level. `--velocity` sets how hard each note is struck (MIDI velocity). The defaults are tuned to be clean for 4–5 note chords. Raise `--gain` if the output is too quiet; lower it if you hear distortion on dense voicings.

```bash
chord Cmaj7 --gain 1.2            # louder
chord Cmaj7 -g 0.5 -v 80          # quieter, less attack
```

### Repeat

```bash
chord Dm7/9 --allegro --repeat 4  # play the chord 4 times
chord Dm:2 G7:2 --repeat 2        # each chord repeated twice before moving to the next
```

---

## Examples

### Quick chord lookup

```bash
chord F#m7b5          # what notes are in this chord?
```
```
F#m7b5        F# A C E                  whole             @ 144 BPM
```

### ii–V–I progression

```bash
chord Dm7/9 G7 Cmaj7 Am7 --andante
```

### Hendrix chord

```bash
chord E7/#9 --allegro
```

### iii–VI–ii–V–I in D major

```bash
chord F#m7 B7 Em7 A7 Dmaj7 --andante
```

### Autumn Leaves (G minor) — Nat King Cole

The standard changes, two half notes per chord:

```bash
chord Cm7:2 F7:2 Bbmaj7:2 Ebmaj7:2 Am7b5:2 D7:2 Gm7:2 Gm7:2 \
      Am7b5:2 D7:2 Gm7:2 Cm7:2 F7:2 Bbmaj7:2 Ebmaj7:2 Am7b5:2 D7:2 Gm7:1 \
      --andante
```

The progression follows two ii–V–I cycles: first resolving to Bb major (Cm7–F7–Bbmaj7), then to G minor (Am7b5–D7–Gm7). The final Gm7 is held as a whole note.

### With rests

```bash
chord Dm:2 -:2 G7:2 -:2 Cmaj7:1 --andante
```

---

## How it works

1. Each chord name is parsed into a list of MIDI note numbers (root in octave 4, bass notes in octave 3).
2. All chords are written into a single type-0 MIDI file with correct tempo and timing — no process-launch gaps between chords.
3. FluidSynth renders the MIDI file to audio using the `FluidR3_GM` soundfont and plays it back.
4. The temporary MIDI file is deleted immediately after playback.

Rests are represented as MIDI marker meta-messages, which advance the playback clock silently without triggering any notes.

---

## Building

Development requirements (Debian):

```bash
sudo apt install make dpkg-dev debhelper
```

```bash
make deb      # build .deb package  →  ../chord_0.1.0-1_all.deb
make test     # run the chord parser test suite
make install  # install to /usr/local/bin (no packaging)
make install-local  # install to ~/.local/bin (no sudo)
make clean    # remove build artifacts
```
