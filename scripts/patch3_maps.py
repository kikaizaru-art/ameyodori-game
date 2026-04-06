"""
patch3: Replace map templates with light/dark versions.
        'D' = TILE_DARK corridors (enemy paths), '.' = TILE_FLOOR (player paths).
        Remove streetlight/breaklight placement code from all 3 stages.
        Update template mappings to include 'd': TILE_DARK.
"""
PATH = r'C:\Users\kikai\OneDrive\Desktop\ameyodori_v13.html'
with open(PATH, encoding='utf-8') as f:
    code = f.read()

# ====================================================
# STAGE 1 template + mapping + remove streetlight code
# ====================================================
OLD_S1 = (
    '  const t = [\n'
    '    "###########GGG###########",\n'
    '    "#...........#...........#",\n'
    '    "#.###.####.###.####.###.#",\n'
    '    "#.........................#",\n'
    '    "#.###.#.#########.#.###.#",\n'
    '    "#.....#.....#.....#.....#",\n'
    '    "####.####.#.#.#.####.####",\n'
    '    "#........#.#.#.#........#",\n'
    '    "#.####.#.#...#.#.####.#.#",\n'
    '    "#.........#.#.#.........#",\n'
    '    "####.####.#.#.#.####.####",\n'
    '    "#.....#.....#.....#.....#",\n'
    '    "#.###.#.#########.#.###.#",\n'
    '    "#.........................#",\n'
    '    "#.###.####.###.####.###.#",\n'
    '    "#...........#...........#",\n'
    '    "#.............P.........#",\n'
    '    "#########################",\n'
    '  ];\n'
    "  const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'G': TILE_GOAL, 'P': TILE_FLOOR };"
)
NEW_S1 = (
    '  const t = [\n'
    '    "###########GGG###########",\n'
    '    "#ddddddddddd#ddddddddddd#",\n'
    '    "#d###d####d###d####d###d#",\n'
    '    "#d.......d...d.......d..#",\n'
    '    "#d###.#.#########.#.###d#",\n'
    '    "#.....#ddddd#ddddd#.....#",\n'
    '    "####d####d#.#.#d####d####",\n'
    '    "#.......#.#.#.#.........#",\n'
    '    "#d####.#.#ddd#.#.####d#.#",\n'
    '    "#.........#.#.#.........#",\n'
    '    "####d####d#.#.#d####d####",\n'
    '    "#.....#ddddd#ddddd#.....#",\n'
    '    "#.###.#.#########.#.###.#",\n'
    '    "#.........................#",\n'
    '    "#.###.####.###.####.###.#",\n'
    '    "#...........#...........#",\n'
    '    "#.............P.........#",\n'
    '    "#########################",\n'
    '  ];\n'
    "  const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'd': TILE_DARK, 'G': TILE_GOAL, 'P': TILE_FLOOR };"
)
assert OLD_S1 in code, "Stage1 template not found"
code = code.replace(OLD_S1, NEW_S1, 1)

# Remove Stage 1 streetlight placement block
OLD_S1_SL = (
    "  // Streetlights at intersections\n"
    "  const slPositions = [\n"
    "    [Math.floor(ROWS*0.25), Math.floor(COLS*0.25)],\n"
    "    [Math.floor(ROWS*0.25), Math.floor(COLS*0.75)],\n"
    "    [Math.floor(ROWS*0.5), midC],\n"
    "    [Math.floor(ROWS*0.75), Math.floor(COLS*0.25)],\n"
    "    [Math.floor(ROWS*0.75), Math.floor(COLS*0.75)],\n"
    "  ];\n"
    "  slPositions.forEach(([r,c]) => { if (map[r] && map[r][c] === TILE_FLOOR) map[r][c] = TILE_STREETLIGHT; });\n"
    "  // Mirror\n"
    "  if (map[midR] && map[midR][3] === TILE_FLOOR) map[midR][3] = TILE_MIRROR;\n"
    "  // Match\n"
    "  if (map[3] && map[3][midC+2] === TILE_FLOOR) map[3][midC+2] = TILE_MATCH;"
)
NEW_S1_SL = (
    "  // Mirror — on a floor tile near left edge\n"
    "  if (map[midR] && map[midR][3] !== TILE_WALL) map[midR][3] = TILE_MIRROR;\n"
    "  // Match — near a dark/light border so player learns the mechanic\n"
    "  if (map[3] && map[3][midC+2] !== TILE_WALL) map[3][midC+2] = TILE_MATCH;"
)
assert OLD_S1_SL in code, "Stage1 streetlight placement block not found"
code = code.replace(OLD_S1_SL, NEW_S1_SL, 1)

# ====================================================
# STAGE 2 template + mapping + remove streetlight code
# ====================================================
OLD_S2 = (
    '  const t = [\n'
    '    "###########GGG###########",\n'
    '    "#.......#.......#.......#",\n'
    '    "#.#####.#.#####.#.#####.#",\n'
    '    "#.#...#...#...#...#...#.#",\n'
    '    "#.#.#.#####.#.#####.#.#.#",\n'
    '    "#...#.......#.......#...#",\n'
    '    "###.###.#########.###.###",\n'
    '    "#.......#.......#.......#",\n'
    '    "#.###.###.#.#.###.###.#.#",\n'
    '    "#.#.......#.#.......#.#.#",\n'
    '    "#.#.#####.#.#.#####.#.#.#",\n'
    '    "#...#.......#.......#...#",\n'
    '    "###.###.#########.###.###",\n'
    '    "#.......#.......#.......#",\n'
    '    "#.#####.#.#####.#.#####.#",\n'
    '    "#.#...#...#...#...#...#.#",\n'
    '    "#.........................#",\n'
    '    "#########################",\n'
    '  ];\n'
    "  const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'G': TILE_GOAL };"
)
NEW_S2 = (
    '  const t = [\n'
    '    "###########GGG###########",\n'
    '    "#ddddddd#ddddddd#ddddddd#",\n'
    '    "#d#####d#d#####d#d#####d#",\n'
    '    "#d#...#ddd#...#ddd#...#d#",\n'
    '    "#d#d#d#####d#d#####d#d#d#",\n'
    '    "#...#ddddddd#ddddddd#...#",\n'
    '    "###d###d#########d###d###",\n'
    '    "#.......#ddddddd#.......#",\n'
    '    "#d###d###.#.#.###d###d#d#",\n'
    '    "#d#.......#.#.......#.#d#",\n'
    '    "#d#.#####.#.#.#####.#.#d#",\n'
    '    "#...#.......#.......#...#",\n'
    '    "###d###d#########d###d###",\n'
    '    "#.......#ddddddd#.......#",\n'
    '    "#.#####.#.#####.#.#####.#",\n'
    '    "#.#...#...#...#...#...#.#",\n'
    '    "#.........................#",\n'
    '    "#########################",\n'
    '  ];\n'
    "  const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'd': TILE_DARK, 'G': TILE_GOAL };"
)
assert OLD_S2 in code, "Stage2 template not found"
code = code.replace(OLD_S2, NEW_S2, 1)

# Remove Stage 2 streetlight/breaklight placement
OLD_S2_SL = (
    "  const midC = Math.floor(COLS / 2);\n"
    "  const midR = Math.floor(ROWS / 2);\n"
    "  // Streetlights (fewer)\n"
    "  [[Math.floor(ROWS*0.3), midC], [Math.floor(ROWS*0.6), Math.floor(COLS*0.25)], [Math.floor(ROWS*0.6), Math.floor(COLS*0.75)]].forEach(([r,c]) => {\n"
    "    if (map[r] && map[r][c] === TILE_FLOOR) map[r][c] = TILE_STREETLIGHT;\n"
    "  });\n"
    "  // Breakable streetlight\n"
    "  if (map[2] && map[2][midC] === TILE_FLOOR) map[2][midC] = TILE_BREAKLIGHT;\n"
    "  // Mirror\n"
    "  if (map[midR] && map[midR][midC] === TILE_FLOOR) map[midR][midC] = TILE_MIRROR;\n"
    "  // Match\n"
    "  if (map[ROWS-4] && map[ROWS-4][3] === TILE_FLOOR) map[ROWS-4][3] = TILE_MATCH;"
)
NEW_S2_SL = (
    "  const midC = Math.floor(COLS / 2);\n"
    "  const midR = Math.floor(ROWS / 2);\n"
    "  // Mirror — center\n"
    "  if (map[midR] && map[midR][midC] !== TILE_WALL) map[midR][midC] = TILE_MIRROR;\n"
    "  // Match — lower left, near a dark section\n"
    "  if (map[ROWS-4] && map[ROWS-4][3] !== TILE_WALL) map[ROWS-4][3] = TILE_MATCH;"
)
assert OLD_S2_SL in code, "Stage2 streetlight placement block not found"
code = code.replace(OLD_S2_SL, NEW_S2_SL, 1)

# ====================================================
# STAGE 3 template + mapping + remove streetlight code
# ====================================================
OLD_S3 = (
    '  const t = [\n'
    '    "###########GGG###########",\n'
    '    "#...#.........#.........#",\n'
    '    "#.#.#.#####.#.#.#####.#.#",\n'
    '    "#.#...#...#.#...#...#.#.#",\n'
    '    "#.#####.#.#.#####.#.###.#",\n'
    '    "#.......#.........#.....#",\n'
    '    "#.###.#####.#.#####.###.#",\n'
    '    "#.#.........#.........#.#",\n'
    '    "#.#.###.#########.###.#.#",\n'
    '    "#.#.#.......#.......#.#.#",\n'
    '    "#.#.#.#####.#.#####.#.#.#",\n'
    '    "#...#.......#.......#...#",\n'
    '    "#.###.###.#####.###.###.#",\n'
    '    "#.........#...#.........#",\n'
    '    "#.#####.###.#.###.#####.#",\n'
    '    "#.#...........#...#.....#",\n'
    '    "#.........................#",\n'
    '    "#########################",\n'
    '  ];\n'
    "  const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'G': TILE_GOAL };"
)
NEW_S3 = (
    '  const t = [\n'
    '    "###########GGG###########",\n'
    '    "#ddd#ddddddddd#ddddddddd#",\n'
    '    "#d#d#d#####d#d#d#####d#d#",\n'
    '    "#d#ddd#...#d#ddd#...#d#d#",\n'
    '    "#d#####d#d#d#####d#d###d#",\n'
    '    "#ddddddd#ddddddddd#ddddd#",\n'
    '    "#d###d#####d#d#####d###d#",\n'
    '    "#d#.........#.........#d#",\n'
    '    "#d#d###d#########d###d#d#",\n'
    '    "#d#d#.......#.......#d#d#",\n'
    '    "#d#d#d#####.#.#####d#d#d#",\n'
    '    "#...#.......#.......#...#",\n'
    '    "#.###.###.#####.###.###.#",\n'
    '    "#.........#...#.........#",\n'
    '    "#.#####.###.#.###.#####.#",\n'
    '    "#.#...........#...#.....#",\n'
    '    "#.........................#",\n'
    '    "#########################",\n'
    '  ];\n'
    "  const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'd': TILE_DARK, 'G': TILE_GOAL };"
)
assert OLD_S3 in code, "Stage3 template not found"
code = code.replace(OLD_S3, NEW_S3, 1)

# Remove Stage 3 streetlight/breaklight placement
OLD_S3_SL = (
    "  const midC = Math.floor(COLS / 2);\n"
    "  const midR = Math.floor(ROWS / 2);\n"
    "  // Permanent streetlights (2)\n"
    "  [[Math.floor(ROWS*0.35), Math.floor(COLS*0.2)], [Math.floor(ROWS*0.65), Math.floor(COLS*0.8)]].forEach(([r,c]) => {\n"
    "    if (map[r] && map[r][c] === TILE_FLOOR) map[r][c] = TILE_STREETLIGHT;\n"
    "  });\n"
    "  // Breakable streetlights (3)\n"
    "  [[Math.floor(ROWS*0.2), midC], [midR, Math.floor(COLS*0.3)], [Math.floor(ROWS*0.75), midC]].forEach(([r,c]) => {\n"
    "    if (map[r] && map[r][c] === TILE_FLOOR) map[r][c] = TILE_BREAKLIGHT;\n"
    "  });\n"
    "  // Mirrors (2)\n"
    "  if (map[3] && map[3][3] === TILE_FLOOR) map[3][3] = TILE_MIRROR;\n"
    "  if (map[ROWS-4] && map[ROWS-4][COLS-4] === TILE_FLOOR) map[ROWS-4][COLS-4] = TILE_MIRROR;"
)
NEW_S3_SL = (
    "  const midC = Math.floor(COLS / 2);\n"
    "  const midR = Math.floor(ROWS / 2);\n"
    "  // Mirrors (2)\n"
    "  if (map[3] && map[3][3] !== TILE_WALL) map[3][3] = TILE_MIRROR;\n"
    "  if (map[ROWS-4] && map[ROWS-4][COLS-4] !== TILE_WALL) map[ROWS-4][COLS-4] = TILE_MIRROR;"
)
assert OLD_S3_SL in code, "Stage3 streetlight placement block not found"
code = code.replace(OLD_S3_SL, NEW_S3_SL, 1)

# Stage 3 match items — allow on non-wall tiles
OLD_MATCH3 = (
    "  // Matches (2)\n"
    "  if (map[2] && map[2][2] === TILE_FLOOR) map[2][2] = TILE_MATCH;\n"
    "  if (map[ROWS-3] && map[ROWS-3][COLS-3] === TILE_FLOOR) map[ROWS-3][COLS-3] = TILE_MATCH;"
)
NEW_MATCH3 = (
    "  // Matches (2)\n"
    "  if (map[2] && map[2][2] !== TILE_WALL) map[2][2] = TILE_MATCH;\n"
    "  if (map[ROWS-3] && map[ROWS-3][COLS-3] !== TILE_WALL) map[ROWS-3][COLS-3] = TILE_MATCH;"
)
assert OLD_MATCH3 in code, "Stage3 match items block not found"
code = code.replace(OLD_MATCH3, NEW_MATCH3, 1)

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(code)
print("patch3 OK — map templates updated with light/dark tiles, streetlight placement removed")
