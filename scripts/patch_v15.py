#!/usr/bin/env python3
"""
patch_v15.py — Generates ameyodori_v15.html from ameyodori_v12.html
Light/dark road mechanic + enemy spawn delay
"""

import sys

INPUT  = 'ameyodori_v12.html'
OUTPUT = 'ameyodori_v15.html'

with open(INPUT, 'r', encoding='utf-8') as f:
    src = f.read()

original_len = len(src)
applied = []

# ── helpers ──────────────────────────────────────────────────────────────
def replace_first(text, find, repl, label):
    idx = text.find(find)
    if idx == -1:
        print(f'  [WARN] {label}: pattern NOT found')
        return text, False
    result = text[:idx] + repl + text[idx + len(find):]
    print(f'  [OK]   {label}')
    return result, True

def replace_all(text, find, repl, label):
    count = text.count(find)
    if count == 0:
        print(f'  [WARN] {label}: pattern NOT found')
        return text, False
    result = text.replace(find, repl)
    print(f'  [OK]   {label} ({count} replacements)')
    return result, True

# ── R1: TILE_DARK constant ────────────────────────────────────────────────
src, ok = replace_first(
    src,
    'const TILE_HIDDEN = 11;',
    'const TILE_HIDDEN = 11;\nconst TILE_DARK = 13;',
    'R1: TILE_DARK constant'
)

# ── R2: dark_road texture ─────────────────────────────────────────────────
dark_road_texture = """g.generateTexture('floor', TILE, TILE);

  // dark road (enemy territory - much darker, reddish tint)
  g.clear(); g.fillStyle(0x080210); g.fillRect(0,0,TILE,TILE);
  g.fillStyle(0x100418); g.fillRect(1,1,TILE-2,TILE-2);
  g.fillStyle(0x2a0011, 0.3); g.fillCircle(4,4,2); g.fillCircle(TILE-4,4,2); g.fillCircle(4,TILE-4,2); g.fillCircle(TILE-4,TILE-4,2);
  g.generateTexture('dark_road', TILE, TILE);"""

src, ok = replace_first(
    src,
    "g.generateTexture('floor', TILE, TILE);",
    dark_road_texture,
    'R2: dark_road texture'
)

# ── R3: TILE_DARK rendering ───────────────────────────────────────────────
# Actual indentation in v12 uses 6-space indent inside for loop
find_r3 = "      if (t === TILE_FLOOR) {\n        scene.add.image(x, y, 'floor').setDepth(0);"
repl_r3 = ("      if (t === TILE_FLOOR) {\n"
           "        scene.add.image(x, y, 'floor').setDepth(0);\n"
           "      } else if (t === TILE_DARK) {\n"
           "        scene.add.image(x, y, 'dark_road').setDepth(0);")

src, ok = replace_first(src, find_r3, repl_r3, 'R3: TILE_DARK rendering')
if not ok:
    # Try with different whitespace (4-space)
    find_r3b = "    if (t === TILE_FLOOR) {\n      scene.add.image(x, y, 'floor').setDepth(0);"
    repl_r3b = ("    if (t === TILE_FLOOR) {\n"
                "      scene.add.image(x, y, 'floor').setDepth(0);\n"
                "    } else if (t === TILE_DARK) {\n"
                "      scene.add.image(x, y, 'dark_road').setDepth(0);")
    src, ok = replace_first(src, find_r3b, repl_r3b, 'R3: TILE_DARK rendering (4-space fallback)')

# ── R4: Block dark tiles in tryMoveSister ────────────────────────────────
find_r4 = "  if (t === TILE_WALL || t === TILE_SHOP || t === TILE_DOOR || t === TILE_HIDDEN || t === TILE_MIRROR) return;"
repl_r4 = ("  if (t === TILE_WALL || t === TILE_SHOP || t === TILE_DOOR || t === TILE_HIDDEN || t === TILE_MIRROR) return;\n"
           "  if (t === TILE_DARK && !matchActive) return;")
src, ok = replace_first(src, find_r4, repl_r4, 'R4: Block dark tiles in tryMoveSister')

# ── R5: Stage 1 mapping — add 'd' ────────────────────────────────────────
find_r5 = "const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'G': TILE_GOAL, 'P': TILE_FLOOR };"
repl_r5 = "const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'd': TILE_DARK, 'G': TILE_GOAL, 'P': TILE_FLOOR };"
src, ok = replace_first(src, find_r5, repl_r5, 'R5: Stage 1 mapping')

# ── R6: Stage 2 & 3 mappings — add 'd' (replace all) ────────────────────
find_r6 = "const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'G': TILE_GOAL };"
repl_r6 = "const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'd': TILE_DARK, 'G': TILE_GOAL };"
src, ok = replace_all(src, find_r6, repl_r6, 'R6: Stage 2+3 mappings')

# ── R7: Stage 1 template — add dark zone rows ────────────────────────────
# Row 1 (after goal row): "#...........#...........#"
src, ok = replace_first(
    src,
    '"#...........#...........#",',
    '"#ddddddddddd#ddddddddddd#",',
    'R7a: Stage1 row1 dark'
)

# Row 2: "#.###.####.###.####.###.#"
src, ok = replace_first(
    src,
    '"#.###.####.###.####.###.#",',
    '"#d###d####d###d####d###d#",',
    'R7b: Stage1 row2 dark'
)

# Row 3 (first occurrence of "#.........................#"
# There are two occurrences — we want the first (near goal)
src, ok = replace_first(
    src,
    '"#.........................#",',
    '"#ddddddddddddddddddddddddd#",',
    'R7c: Stage1 row3 dark (1st occurrence)'
)

# ── R8a: enemySpawnDelay variable declaration ────────────────────────────
src, ok = replace_first(
    src,
    'let sisterMoving = false;',
    'let sisterMoving = false;\nlet enemySpawnDelay = 0;',
    'R8a: enemySpawnDelay declaration'
)

# ── R8b: enemySpawnDelay reset in stage init ────────────────────────────
find_r8b = "  sisterMoving = false; sisterMoveQueue = null; sisterTrail = []; brotherMoving = false;"
repl_r8b = ("  sisterMoving = false; sisterMoveQueue = null; sisterTrail = []; brotherMoving = false;\n"
            "  enemySpawnDelay = Date.now() + 3000;\n"
            "  enemies.forEach(e => { e.sprite.setAlpha(0); e.sprite.setVisible(false); });")
src, ok = replace_first(src, find_r8b, repl_r8b, 'R8b: enemySpawnDelay reset + hide enemies')

# ── R9: Enemy spawn delay check at top of enemies.forEach callback ───────
find_r9 = "  enemies.forEach(enemy => {\n    let chaseX = sister.x, chaseY = sister.y;"
repl_r9 = ("  enemies.forEach(enemy => {\n"
           "    // Enemy spawn delay\n"
           "    if (Date.now() < enemySpawnDelay) { enemy.sprite.setAlpha(0); enemy.sprite.setVisible(false); return; }\n"
           "    if (!enemy.sprite.visible) { enemy.sprite.setVisible(true); enemy.sprite.setAlpha(0.85); }\n"
           "    let chaseX = sister.x, chaseY = sister.y;")
src, ok = replace_first(src, find_r9, repl_r9, 'R9: enemySpawnDelay check in update loop')

# ── R10: Enemy positions — move to bottom of map ─────────────────────────
# Stage 1: y: 2 * TILE  →  y: (ROWS-2) * TILE
src, ok = replace_first(
    src,
    'enemies: [{ x: midC * TILE, y: 2 * TILE }],',
    'enemies: [{ x: midC * TILE, y: (ROWS-2) * TILE }],',
    'R10a: Stage1 enemy y to bottom'
)

# Stage 2: two enemies at y: 3 * TILE
src, ok = replace_first(
    src,
    '      { x: 3 * TILE, y: 3 * TILE },\n      { x: (COLS - 4) * TILE, y: 3 * TILE },',
    '      { x: 3 * TILE, y: (ROWS-2) * TILE },\n      { x: (COLS - 4) * TILE, y: (ROWS-2) * TILE },',
    'R10b: Stage2 enemies y to bottom'
)

# Stage 3: enemies
src, ok = replace_first(
    src,
    '      { x: 3 * TILE, y: 2 * TILE },\n      { x: (COLS - 4) * TILE, y: Math.floor(ROWS*0.4) * TILE },',
    '      { x: 3 * TILE, y: (ROWS-2) * TILE },\n      { x: (COLS - 4) * TILE, y: (ROWS-2) * TILE },',
    'R10c: Stage3 enemies y to bottom'
)

# ── Write output ──────────────────────────────────────────────────────────
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(src)

print()
print(f'Written: {OUTPUT}  ({len(src)} chars, was {original_len})')

# ── Verification ──────────────────────────────────────────────────────────
print()
print('=== Verification ===')
checks = [
    ('TILE_DARK',       5),
    ('dark_road',       2),
    ('enemySpawnDelay', 3),
]
all_ok = True
for term, minimum in checks:
    count = src.count(term)
    status = 'OK' if count >= minimum else 'FAIL'
    if status == 'FAIL':
        all_ok = False
    print(f'  [{status}] "{term}": found {count} times (need >= {minimum})')

# Check for duplicate const declarations
import re
consts = re.findall(r'const TILE_DARK\b', src)
if len(consts) > 1:
    print(f'  [FAIL] Duplicate "const TILE_DARK" found ({len(consts)} times)')
    all_ok = False
else:
    print(f'  [OK]   No duplicate const TILE_DARK ({len(consts)} declaration)')

print()
print('Result:', 'ALL CHECKS PASSED' if all_ok else 'SOME CHECKS FAILED')
