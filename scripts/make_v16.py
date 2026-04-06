#!/usr/bin/env python3
"""
make_v16.py — generates ameyodori_v16.html from ameyodori_v12.html
with the light/dark road system.
"""
import re, sys

SRC  = r"C:\Users\kikai\OneDrive\Desktop\ameyodori_v12.html"
DEST = r"C:\Users\kikai\OneDrive\Desktop\ameyodori_v16.html"

with open(SRC, encoding="utf-8") as f:
    src = f.read()

# ── 1. TILE_DARK constant ────────────────────────────────────────────────────
src = src.replace(
    "const TILE_HIDDEN = 11;",
    "const TILE_HIDDEN = 11;\nconst TILE_DARK = 13;"
)

# ── 2. Floor texture — brighter ──────────────────────────────────────────────
src = src.replace(
    "  // floor — dark, subtle grid\n"
    "  g.clear(); g.fillStyle(0x141428); g.fillRect(0,0,TILE,TILE);\n"
    "  g.fillStyle(0x1a1a30, 0.4); g.fillRect(0,0,TILE,1); g.fillRect(0,0,1,TILE);\n"
    "  g.generateTexture('floor', TILE, TILE);",
    "  // floor — bright blue-purple\n"
    "  g.clear(); g.fillStyle(0x222244); g.fillRect(0,0,TILE,TILE);\n"
    "  g.fillStyle(0x2a2a4e, 0.6); g.fillRect(0,0,TILE,1); g.fillRect(0,0,1,TILE);\n"
    "  g.generateTexture('floor', TILE, TILE);\n\n"
    "  // dark_road — very dark red-purple with red corner dots\n"
    "  g.clear(); g.fillStyle(0x0a0412); g.fillRect(0,0,TILE,TILE);\n"
    "  g.fillStyle(0x3a0808); g.fillRect(0,0,2,2); g.fillRect(TILE-2,0,2,2);\n"
    "  g.fillRect(0,TILE-2,2,2); g.fillRect(TILE-2,TILE-2,2,2);\n"
    "  g.generateTexture('dark_road', TILE, TILE);"
)

# ── 3. buildStage tile loop — add TILE_DARK rendering after TILE_HIDDEN block ─
# find the TILE_HIDDEN block end and insert after it
HIDDEN_BLOCK = (
    "      } else if (t === TILE_HIDDEN) {\n"
    "        scene.add.image(x, y, 'floor').setDepth(0);\n"
    "        const hw = walls.create(x, y, 'hidden_wall').setSize(TILE, TILE).setDepth(2).refreshBody();\n"
    "        hw.isHidden = true; hw.revealed = false;\n"
    "        hw.tileR = r; hw.tileC = c;\n"
    "        hiddenPassages.push(hw);\n"
    "      }\n"
    "    }\n"
    "  }\n"
    "\n"
    "  // Link switches to doors"
)
HIDDEN_BLOCK_NEW = (
    "      } else if (t === TILE_HIDDEN) {\n"
    "        scene.add.image(x, y, 'floor').setDepth(0);\n"
    "        const hw = walls.create(x, y, 'hidden_wall').setSize(TILE, TILE).setDepth(2).refreshBody();\n"
    "        hw.isHidden = true; hw.revealed = false;\n"
    "        hw.tileR = r; hw.tileC = c;\n"
    "        hiddenPassages.push(hw);\n"
    "      } else if (t === TILE_DARK) {\n"
    "        scene.add.image(x, y, 'dark_road').setDepth(0);\n"
    "      }\n"
    "    }\n"
    "  }\n"
    "\n"
    "  // Link switches to doors"
)
src = src.replace(HIDDEN_BLOCK, HIDDEN_BLOCK_NEW)

# ── 4. tryMoveSister — block TILE_DARK unless matchActive ───────────────────
src = src.replace(
    "  if (t === TILE_WALL || t === TILE_SHOP || t === TILE_DOOR || t === TILE_HIDDEN || t === TILE_MIRROR) return;",
    "  if (t === TILE_WALL || t === TILE_SHOP || t === TILE_DOOR || t === TILE_HIDDEN || t === TILE_MIRROR) return;\n"
    "  if (t === TILE_DARK && !matchActive) return;"
)

# ── 5a. Stage 1 template — add dark roads, keep complete light path ───────────
OLD_S1_TEMPLATE = '''\
  const t = [
    "###########GGG###########",
    "#...........#...........#",
    "#.###.####.###.####.###.#",
    "#.........................#",
    "#.###.#.#########.#.###.#",
    "#.....#.....#.....#.....#",
    "####.####.#.#.#.####.####",
    "#........#.#.#.#........#",
    "#.####.#.#...#.#.####.#.#",
    "#.........#.#.#.........#",
    "####.####.#.#.#.####.####",
    "#.....#.....#.....#.....#",
    "#.###.#.#########.#.###.#",
    "#.........................#",
    "#.###.####.###.####.###.#",
    "#...........#...........#",
    "#.............P.........#",
    "#########################",
  ];
  const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'G': TILE_GOAL, 'P': TILE_FLOOR };'''

NEW_S1_TEMPLATE = '''\
  const t = [
    "###########GGG###########",
    "#...........#...........#",
    "#.###.####.###.####.###.#",
    "#....ddddd........ddddd.#",
    "#.###.#.#########.#.###.#",
    "#.....#.....#.....#.....#",
    "####.####.#.#.#.####.####",
    "#....ddd.#.#.#.#.ddd....#",
    "#.####.#.#...#.#.####.#.#",
    "#.........#.#.#.........#",
    "####.####.#.#.#.####.####",
    "#.....#.....#.....#.....#",
    "#.###.#.#########.#.###.#",
    "#....ddddd........ddddd.#",
    "#.###.####.###.####.###.#",
    "#...........#...........#",
    "#...............P.......#",
    "#########################",
  ];
  const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'G': TILE_GOAL, 'P': TILE_FLOOR, 'd': TILE_DARK };'''

src = src.replace(OLD_S1_TEMPLATE, NEW_S1_TEMPLATE)

# ── 5b. Stage 2 template ──────────────────────────────────────────────────────
OLD_S2_TEMPLATE = '''\
  const t = [
    "###########GGG###########",
    "#.......#.......#.......#",
    "#.#####.#.#####.#.#####.#",
    "#.#...#...#...#...#...#.#",
    "#.#.#.#####.#.#####.#.#.#",
    "#...#.......#.......#...#",
    "###.###.#########.###.###",
    "#.......#.......#.......#",
    "#.###.###.#.#.###.###.#.#",
    "#.#.......#.#.......#.#.#",
    "#.#.#####.#.#.#####.#.#.#",
    "#...#.......#.......#...#",
    "###.###.#########.###.###",
    "#.......#.......#.......#",
    "#.#####.#.#####.#.#####.#",
    "#.#...#...#...#...#...#.#",
    "#.........................#",
    "#########################",
  ];
  const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'G': TILE_GOAL };'''

NEW_S2_TEMPLATE = '''\
  const t = [
    "###########GGG###########",
    "#.......#.......#.......#",
    "#.#####.#.#####.#.#####.#",
    "#.#.d.#...#.d.#...#.d.#.#",
    "#.#.#.#####.#.#####.#.#.#",
    "#...#.......#.......#...#",
    "###.###.#########.###.###",
    "#.ddddd.#.......#.ddddd.#",
    "#.###.###.#.#.###.###.#.#",
    "#.#.......#.#.......#.#.#",
    "#.#.#####.#.#.#####.#.#.#",
    "#...#.ddd.#.#.ddd.#...#.#",
    "###.###.#########.###.###",
    "#.......#.......#.......#",
    "#.#####.#.#####.#.#####.#",
    "#.#...#...#...#...#...#.#",
    "#.........................#",
    "#########################",
  ];
  const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'G': TILE_GOAL, 'd': TILE_DARK };'''

src = src.replace(OLD_S2_TEMPLATE, NEW_S2_TEMPLATE)

# ── 5c. Stage 3 template ──────────────────────────────────────────────────────
OLD_S3_TEMPLATE = '''\
  const t = [
    "###########GGG###########",
    "#...#.........#.........#",
    "#.#.#.#####.#.#.#####.#.#",
    "#.#...#...#.#...#...#.#.#",
    "#.#####.#.#.#####.#.###.#",
    "#.......#.........#.....#",
    "#.###.#####.#.#####.###.#",
    "#.#.........#.........#.#",
    "#.#.###.#########.###.#.#",
    "#.#.#.......#.......#.#.#",
    "#.#.#.#####.#.#####.#.#.#",
    "#...#.......#.......#...#",
    "#.###.###.#####.###.###.#",
    "#.........#...#.........#",
    "#.#####.###.#.###.#####.#",
    "#.#...........#...#.....#",
    "#.........................#",
    "#########################",
  ];
  const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'G': TILE_GOAL };'''

NEW_S3_TEMPLATE = '''\
  const t = [
    "###########GGG###########",
    "#...#.........#.........#",
    "#.#.#.#####.#.#.#####.#.#",
    "#.#.d.#.d.#.#.d.#.d.#.#.#",
    "#.#####.#.#.#####.#.###.#",
    "#.ddddd.#.........#.ddd.#",
    "#.###.#####.#.#####.###.#",
    "#.#.........#.........#.#",
    "#.#.###.#########.###.#.#",
    "#.#.#.ddddd.#.ddddd.#.#.#",
    "#.#.#.#####.#.#####.#.#.#",
    "#...#.......#.......#...#",
    "#.###.###.#####.###.###.#",
    "#.ddddddd.#.d.#.ddddddd.#",
    "#.#####.###.#.###.#####.#",
    "#.#...........#...#.....#",
    "#.........................#",
    "#########################",
  ];
  const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'G': TILE_GOAL, 'd': TILE_DARK };'''

src = src.replace(OLD_S3_TEMPLATE, NEW_S3_TEMPLATE)

# ── 6. Remove streetlight code ────────────────────────────────────────────────

# 6a. Remove TILE_STREETLIGHT placements from generate functions
#     (replace with TILE_FLOOR via not placing them; remove the slPositions/forEach blocks)

# Stage 1: remove streetlight placement block
src = src.replace(
    "  // Streetlights at intersections\n"
    "  const slPositions = [\n"
    "    [Math.floor(ROWS*0.25), Math.floor(COLS*0.25)],\n"
    "    [Math.floor(ROWS*0.25), Math.floor(COLS*0.75)],\n"
    "    [Math.floor(ROWS*0.5), midC],\n"
    "    [Math.floor(ROWS*0.75), Math.floor(COLS*0.25)],\n"
    "    [Math.floor(ROWS*0.75), Math.floor(COLS*0.75)],\n"
    "  ];\n"
    "  slPositions.forEach(([r,c]) => { if (map[r] && map[r][c] === TILE_FLOOR) map[r][c] = TILE_STREETLIGHT; });",
    "  // (streetlights removed in v16)"
)

# Stage 2: remove streetlight placement block
src = src.replace(
    "  // Streetlights (fewer)\n"
    "  [[Math.floor(ROWS*0.3), midC], [Math.floor(ROWS*0.6), Math.floor(COLS*0.25)], [Math.floor(ROWS*0.6), Math.floor(COLS*0.75)]].forEach(([r,c]) => {\n"
    "    if (map[r] && map[r][c] === TILE_FLOOR) map[r][c] = TILE_STREETLIGHT;\n"
    "  });",
    "  // (streetlights removed in v16)"
)
# Stage 2: remove TILE_BREAKLIGHT placement
src = src.replace(
    "  // Breakable streetlight\n"
    "  if (map[2] && map[2][midC] === TILE_FLOOR) map[2][midC] = TILE_BREAKLIGHT;",
    "  // (breaklight removed in v16)"
)

# Stage 3: remove permanent streetlights block
src = src.replace(
    "  // Permanent streetlights (2)\n"
    "  [[Math.floor(ROWS*0.35), Math.floor(COLS*0.2)], [Math.floor(ROWS*0.65), Math.floor(COLS*0.8)]].forEach(([r,c]) => {\n"
    "    if (map[r] && map[r][c] === TILE_FLOOR) map[r][c] = TILE_STREETLIGHT;\n"
    "  });",
    "  // (streetlights removed in v16)"
)
# Stage 3: remove breakable streetlights block
src = src.replace(
    "  // Breakable streetlights (3)\n"
    "  [[Math.floor(ROWS*0.2), midC], [midR, Math.floor(COLS*0.3)], [Math.floor(ROWS*0.75), midC]].forEach(([r,c]) => {\n"
    "    if (map[r] && map[r][c] === TILE_FLOOR) map[r][c] = TILE_BREAKLIGHT;\n"
    "  });",
    "  // (breaklights removed in v16)"
)

# 6b. Remove streetlight texture generation
src = src.replace(
    "\n  // streetlight\n"
    "  g.clear(); g.fillStyle(0x1a1a2e); g.fillRect(0,0,TILE,TILE);\n"
    "  g.fillStyle(0x555566); g.fillRect(14,8,4,20);\n"
    "  g.fillStyle(0xffdd88); g.fillRect(10,4,12,6);\n"
    "  g.generateTexture('streetlight', TILE, TILE);\n\n"
    "  // breakable streetlight (reddish tint, crack mark)\n"
    "  g.clear(); g.fillStyle(0x1a1a2e); g.fillRect(0,0,TILE,TILE);\n"
    "  g.fillStyle(0x665544); g.fillRect(14,8,4,20);\n"
    "  g.fillStyle(0xffcc66); g.fillRect(10,4,12,6);\n"
    "  g.fillStyle(0xcc4422); g.fillRect(10,2,2,2);\n"
    "  g.generateTexture('breaklight', TILE, TILE);\n\n"
    "  // dead breakable streetlight\n"
    "  g.clear(); g.fillStyle(0x1a1a2e); g.fillRect(0,0,TILE,TILE);\n"
    "  g.fillStyle(0x333333); g.fillRect(14,8,4,20);\n"
    "  g.fillStyle(0x444444); g.fillRect(10,4,12,6);\n"
    "  g.generateTexture('breaklight_dead', TILE, TILE);",
    ""
)

# 6c. Remove streetglow texture
src = src.replace(
    "\n  // streetglow (dimmer)\n"
    "  g.clear();\n"
    "  for (let i = 32; i > 0; i--) {\n"
    "    g.fillStyle(0xffddaa, (1-i/32)*0.18);\n"
    "    g.fillCircle(80,80,(i/32)*80);\n"
    "  }\n"
    "  g.generateTexture('streetglow', 160, 160);",
    ""
)

# 6d. Remove streetlightGlows array init and cleanup in buildStage
src = src.replace(
    "  streetlights = [];\n"
    "  streetlightGlows.forEach(g => g.destroy());\n"
    "  streetlightGlows = [];\n"
    "  lightZones = [];",
    "  streetlights = [];\n"
    "  lightZones = [];"
)

# 6e. Remove TILE_STREETLIGHT rendering block in buildStage tile loop
src = src.replace(
    "      } else if (t === TILE_STREETLIGHT) {\n"
    "        scene.add.image(x, y, 'floor').setDepth(0);\n"
    "        scene.add.image(x, y, 'streetlight').setDepth(2);\n"
    "        streetlights.push({ x, y });\n"
    "        const gl = scene.add.image(x, y - 4, 'streetglow').setAlpha(0.45).setBlendMode(Phaser.BlendModes.ADD).setDepth(5);\n"
    "        streetlightGlows.push(gl);\n"
    "        lightZones.push({ x, y, radius: activeConfig.STREETLIGHT_RADIUS, baseAlpha: 0.45, glow: gl });\n"
    "      } else if (t === TILE_BREAKLIGHT) {\n"
    "        scene.add.image(x, y, 'floor').setDepth(0);\n"
    "        const blSprite = scene.add.image(x, y, 'breaklight').setDepth(2);\n"
    "        const blGlow = scene.add.image(x, y - 4, 'streetglow').setAlpha(0.4).setBlendMode(Phaser.BlendModes.ADD).setDepth(5);\n"
    "        const lz = { x, y, radius: activeConfig.STREETLIGHT_RADIUS, baseAlpha: 0.4, glow: blGlow, isBreakable: true };\n"
    "        lightZones.push(lz);\n"
    "        breakLights.push({\n"
    "          sprite: blSprite, glow: blGlow, x, y,\n"
    "          timer: 0, lifetime: activeConfig.BREAKLIGHT_LIFETIME, dead: false, lightZone: lz,\n"
    "        });",
    "      } else if (t === TILE_STREETLIGHT) {\n"
    "        // streetlights removed in v16 — treat as floor\n"
    "        scene.add.image(x, y, 'floor').setDepth(0);\n"
    "      } else if (t === TILE_BREAKLIGHT) {\n"
    "        // breaklights removed in v16 — treat as floor\n"
    "        scene.add.image(x, y, 'floor').setDepth(0);"
)

# 6f. Remove streetlight flicker code in update
src = src.replace(
    "  // Streetlight flicker (permanent streetlights only)\n"
    "  streetlightGlows.forEach((gl, i) => {\n"
    "    const slZone = lightZones.find(z => z.glow === gl);\n"
    "    if (!slZone) return;\n"
    "    let minLD = 9999;\n"
    "    enemies.forEach(e => {\n"
    "      if (streetlights[i]) {\n"
    "        const ld = Phaser.Math.Distance.Between(streetlights[i].x, streetlights[i].y, e.x, e.y);\n"
    "        if (ld < minLD) minLD = ld;\n"
    "      }\n"
    "    });\n"
    "    const flickerMod = currentStage >= 2 ? (Math.random() * 0.12) : 0;\n"
    "    if (minLD < 140) gl.setAlpha(0.08 + Math.random() * 0.18 - flickerMod);\n"
    "    else if (minLD < 240) gl.setAlpha(slZone.baseAlpha * (0.5 + Math.random() * 0.4) - flickerMod);\n"
    "    else gl.setAlpha(slZone.baseAlpha + Math.sin(time / 500 + i) * 0.05 - flickerMod);\n"
    "  });",
    "  // (streetlight flicker removed in v16)"
)

# 6g. Remove breaklight update loop
src = src.replace(
    "  // --- BREAKABLE STREETLIGHTS ---\n"
    "  breakLights.forEach(bl => {\n"
    "    if (bl.dead) return;\n"
    "    bl.timer += dt;\n"
    "    const remaining = bl.lifetime - bl.timer;\n"
    "    if (remaining <= 0) {\n"
    "      bl.dead = true;\n"
    "      bl.sprite.setTexture('breaklight_dead');\n"
    "      bl.glow.setAlpha(0);\n"
    "      bl.lightZone.radius = 0;\n"
    "    } else if (remaining < activeConfig.BREAKLIGHT_WARN_TIME) {\n"
    "      const flickerRate = 1 - (remaining / activeConfig.BREAKLIGHT_WARN_TIME);\n"
    "      bl.glow.setAlpha(Math.random() < (0.3 + flickerRate * 0.5) ? 0.02 : 0.2);\n"
    "      bl.lightZone.radius = activeConfig.STREETLIGHT_RADIUS * (remaining / activeConfig.BREAKLIGHT_WARN_TIME);\n"
    "    }\n"
    "  });",
    "  // (breaklight update removed in v16)"
)

# 6h. Remove breakLights = [] from buildStage clear section
src = src.replace(
    "  breakLights = [];\n  switchSprites = [];",
    "  switchSprites = [];"
)

# 6i. Remove breakLights declaration from GAME STATE
src = src.replace(
    "let breakLights = [];\n",
    ""
)

# 6j. Remove streetlightGlows declaration from GAME STATE
src = src.replace(
    "let streetlightGlows = [], lightZones = [];\n",
    "let lightZones = [];\n"
)

# ── 7. Enemy spawn delay ───────────────────────────────────────────────────────

# Add global variable after matchLightZone declaration
src = src.replace(
    "let matchLightZone = null;\n",
    "let matchLightZone = null;\nlet enemySpawnDelay = 0;\n"
)

# In buildStage, after sisterTrail reset line, add spawn delay setup
src = src.replace(
    "  sisterMoving = false; sisterMoveQueue = null; sisterTrail = []; brotherMoving = false;",
    "  sisterMoving = false; sisterMoveQueue = null; sisterTrail = []; brotherMoving = false;\n"
    "  // Enemy spawn delay — enemies appear 3s after stage loads\n"
    "  enemySpawnDelay = Date.now() + 3000;\n"
    "  enemies.forEach(e => { e.sprite.setVisible(false); });"
)

# In enemy update forEach, add early-return if spawn delayed
src = src.replace(
    "  enemies.forEach(enemy => {\n"
    "    let chaseX = sister.x, chaseY = sister.y;",
    "  enemies.forEach(enemy => {\n"
    "    // Spawn delay: hide and skip until timer expires\n"
    "    if (Date.now() < enemySpawnDelay) {\n"
    "      enemy.sprite.setVisible(false);\n"
    "      return;\n"
    "    }\n"
    "    enemy.sprite.setVisible(true);\n"
    "    let chaseX = sister.x, chaseY = sister.y;"
)

# ── 8. Enemy spawn positions — bottom of screen ────────────────────────────────

# Stage 1 enemies
src = src.replace(
    "    enemies: [{ x: midC * TILE, y: 2 * TILE }],",
    "    enemies: [{ x: midC * TILE, y: (ROWS - 2) * TILE }],"
)

# Stage 2 enemies
src = src.replace(
    "    enemies: [\n"
    "      { x: 3 * TILE, y: 3 * TILE },\n"
    "      { x: (COLS - 4) * TILE, y: 3 * TILE },\n"
    "    ],",
    "    enemies: [\n"
    "      { x: 3 * TILE, y: (ROWS - 2) * TILE },\n"
    "      { x: (COLS - 4) * TILE, y: (ROWS - 2) * TILE },\n"
    "    ],"
)

# Stage 3 enemies
src = src.replace(
    "    enemies: [\n"
    "      { x: 3 * TILE, y: 2 * TILE },\n"
    "      { x: (COLS - 4) * TILE, y: Math.floor(ROWS*0.4) * TILE },\n"
    "    ],",
    "    enemies: [\n"
    "      { x: 3 * TILE, y: (ROWS - 2) * TILE },\n"
    "      { x: (COLS - 4) * TILE, y: (ROWS - 2) * TILE },\n"
    "    ],"
)

# ── 9. Fix tileTexKeys arrays — remove streetlight/breaklight entries ─────────
# In buildStage destroy old standalone map images
src = src.replace(
    "  const tileTexKeys = [\n"
    "    'floor','wall','shop','streetlight','mirror','goal',\n"
    "    'breaklight','breaklight_dead','pushbox',\n"
    "    'switch_off','switch_on','door','match_item',\n"
    "    'hidden_wall','hidden_revealed',\n"
    "  ];",
    "  const tileTexKeys = [\n"
    "    'floor','dark_road','wall','shop','mirror','goal',\n"
    "    'pushbox',\n"
    "    'switch_off','switch_on','door','match_item',\n"
    "    'hidden_wall','hidden_revealed',\n"
    "  ];"
)
# In triggerClear
src = src.replace(
    "  const allTexKeys = [\n"
    "    'floor','wall','shop','streetlight','mirror','goal',\n"
    "    'breaklight','breaklight_dead','pushbox',\n"
    "    'switch_off','switch_on','door','match_item',\n"
    "    'hidden_wall','hidden_revealed',\n"
    "  ];",
    "  const allTexKeys = [\n"
    "    'floor','dark_road','wall','shop','mirror','goal',\n"
    "    'pushbox',\n"
    "    'switch_off','switch_on','door','match_item',\n"
    "    'hidden_wall','hidden_revealed',\n"
    "  ];"
)

# ── write output ──────────────────────────────────────────────────────────────
with open(DEST, "w", encoding="utf-8") as f:
    f.write(src)

print(f"Written: {DEST}")

# ── verify ────────────────────────────────────────────────────────────────────
checks = {
    "TILE_DARK": 6,
    "dark_road": 2,
    "TILE_STREETLIGHT": 0,   # must be 0 in logic (only comments allowed)
    "enemySpawnDelay": 3,
}

import re as _re
for key, minimum in checks.items():
    # For TILE_STREETLIGHT check only non-comment occurrences
    if key == "TILE_STREETLIGHT":
        lines = [l for l in src.splitlines() if key in l and not l.strip().startswith("//")]
        count = len(lines)
        status = "OK" if count == 0 else f"FAIL ({count} non-comment occurrences found)"
    else:
        count = len(_re.findall(re.escape(key), src))
        status = "OK" if count >= minimum else f"FAIL (found {count}, need >= {minimum})"
    print(f"  {key:25s}: {count:3d}  {status}")

# Check for duplicate const declarations
consts = _re.findall(r'\bconst\s+(\w+)\s*=', src)
from collections import Counter
dups = [k for k, v in Counter(consts).items() if v > 1]
if dups:
    print(f"  DUPLICATE consts: {dups}")
else:
    print("  No duplicate const declarations: OK")

# Check stage mappings have 'd'
for stage_n in [1, 2, 3]:
    has_d = f"'d': TILE_DARK" in src
print(f"  'd': TILE_DARK in all mappings: {'OK' if has_d else 'FAIL'}")
