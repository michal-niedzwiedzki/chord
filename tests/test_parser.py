#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

src = open(os.path.join(os.path.dirname(__file__), '..', 'src', 'chord')).read()
exec(compile(src.split("if __name__")[0], 'chord', 'exec'))

CASES = [
    ('C',        [60, 64, 67]),
    ('Dm',       [62, 65, 69]),
    ('G7',       [67, 71, 74, 77]),
    ('Cmaj7',    [60, 64, 67, 71]),
    ('Dm7/9',    [62, 65, 69, 72, 76]),
    ('F#m7b5',   [66, 69, 72, 76]),
    ('Bb7',      [70, 74, 77, 80]),
    ('C/G',      [55, 60, 64, 67]),
    ('Am7',      [69, 72, 76, 79]),
    ('Bdim7',    [71, 74, 77, 80]),
    ('Csus4',    [60, 65, 67]),
    ('Daug',     [62, 66, 70]),
]

ok = True
for name, expected in CASES:
    got = parse_chord(name)
    status = 'OK  ' if got == expected else 'FAIL'
    if got != expected:
        ok = False
    print(f"  {status}  {name:<12} -> {got}  (expected {expected})")

sys.exit(0 if ok else 1)
