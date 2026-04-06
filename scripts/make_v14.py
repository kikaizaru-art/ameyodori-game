import shutil, re, sys

src = r"C:\Users\kikai\OneDrive\Desktop\ameyodori_v12.html"
dst = r"C:\Users\kikai\OneDrive\Desktop\ameyodori_v14.html"

shutil.copy2(src, dst)
print(f"Copied {src} -> {dst}")

with open(dst, 'r', encoding='utf-8') as f:
    code = f.read()

original = code

# ----------------------------------------------------------------
# Change 1: Add TILE_DARK constant after TILE_HIDDEN
# ----------------------------------------------------------------
old1 = "const TILE_HIDDEN = 11;"
new1 = "const TILE_HIDDEN = 11;\nconst TILE_DARK = 13;"
assert old1 in code, "Change 1: TILE_HIDDEN not found"
code = code.replace(old1, new1, 1)
print("Change 1 done: TILE_DARK constant added")

# ----------------------------------------------------------------
# Change 2: Add dark_road texture after floor texture
# ----------------------------------------------------------------
old2 = "  g.generateTexture('floor', TILE, TILE);"
new2 = (
    "  g.generateTexture('floor', TILE, TILE);\n"
    "\n"
    "  // dark_road — deep crimson-black, requires match to cross\n"
    "  g.clear(); g.fillStyle(0x0a0412); g.fillRect(0,0,TILE,TILE);\n"
    "  g.fillStyle(0x120618, 0.5); g.fillRect(1,1,TILE-2,TILE-2);\n"
    "  g.fillStyle(0x330011, 0.25); g.fillCircle(4,4,2); g.fillCircle(TILE-4,4,2);\n"
    "  g.fillCircle(4,TILE-4,2); g.fillCircle(TILE-4,TILE-4,2);\n"
    "  g.generateTexture('dark_road', TILE, TILE);"
)
assert old2 in code, "Change 2: floor generateTexture not found"
code = code.replace(old2, new2, 1)
print("Change 2 done: dark_road texture added")

# ----------------------------------------------------------------
# Change 3: Add TILE_DARK rendering in buildStage
# ----------------------------------------------------------------
old3 = (
    "      } else if (t === TILE_HIDDEN) {\n"
    "        scene.add.image(x, y, 'floor').setDepth(0);\n"
    "        const hw = walls.create(x, y, 'hidden_wall').setSize(TILE, TILE).setDepth(2).refreshBody();\n"
    "        hw.isHidden = true; hw.revealed = false;\n"
    "        hw.tileR = r; hw.tileC = c;\n"
    "        hiddenPassages.push(hw);\n"
    "      }"
)
new3 = (
    "      } else if (t === TILE_HIDDEN) {\n"
    "        scene.add.image(x, y, 'floor').setDepth(0);\n"
    "        const hw = walls.create(x, y, 'hidden_wall').setSize(TILE, TILE).setDepth(2).refreshBody();\n"
    "        hw.isHidden = true; hw.revealed = false;\n"
    "        hw.tileR = r; hw.tileC = c;\n"
    "        hiddenPassages.push(hw);\n"
    "      } else if (t === TILE_DARK) {\n"
    "        scene.add.image(x, y, 'dark_road').setDepth(0);\n"
    "      }"
)
assert old3 in code, "Change 3: TILE_HIDDEN block not found"
code = code.replace(old3, new3, 1)
print("Change 3 done: TILE_DARK rendering added to buildStage")

# ----------------------------------------------------------------
# Change 4: Block dark tiles in tryMoveSister unless match active
# ----------------------------------------------------------------
old4 = (
    "  if (t === TILE_WALL || t === TILE_SHOP || t === TILE_DOOR || t === TILE_HIDDEN || t === TILE_MIRROR) return;\n"
    "  sisterMoving = true;"
)
new4 = (
    "  if (t === TILE_WALL || t === TILE_SHOP || t === TILE_DOOR || t === TILE_HIDDEN || t === TILE_MIRROR) return;\n"
    "  if (t === TILE_DARK && !matchActive) return;\n"
    "  sisterMoving = true;"
)
assert old4 in code, "Change 4: wall check line in tryMoveSister not found"
code = code.replace(old4, new4, 1)
print("Change 4 done: TILE_DARK block in tryMoveSister added")

# ----------------------------------------------------------------
# Change 5: Update Stage 1 mapping and template rows 1-3 to use 'd'
# ----------------------------------------------------------------
# Update the mapping object for Stage 1
old5_mapping = "  const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'G': TILE_GOAL, 'P': TILE_FLOOR };"
new5_mapping = "  const mapping = { '#': TILE_WALL, '.': TILE_FLOOR, 'G': TILE_GOAL, 'P': TILE_FLOOR, 'd': TILE_DARK };"
assert old5_mapping in code, "Change 5a: Stage 1 mapping not found"
code = code.replace(old5_mapping, new5_mapping, 1)
print("Change 5a done: Stage 1 mapping updated with 'd'")

# Update rows 1-3 of Stage 1 template to use 'd' (dark zone near goal)
old5_template = (
    '    "#...........#...........#",\n'
    '    "#.###.####.###.####.###.#",\n'
    '    "#.........................#",'
)
new5_template = (
    '    "#ddddddddddd#ddddddddddd#",\n'
    '    "#d###d####d###d####d###d#",\n'
    '    "#ddddddddddddddddddddddd#",'
)
assert old5_template in code, "Change 5b: Stage 1 template rows 1-3 not found"
code = code.replace(old5_template, new5_template, 1)
print("Change 5b done: Stage 1 rows 1-3 changed to dark zone")

# ----------------------------------------------------------------
# Change 6: Enemy spawn delay
# ----------------------------------------------------------------
# 6a: Add global variable near other let declarations
old6a = "let sisterMoving = false;"
new6a = "let sisterMoving = false;\nlet enemySpawnDelay = 0;"
assert old6a in code, "Change 6a: sisterMoving declaration not found"
code = code.replace(old6a, new6a, 1)
print("Change 6a done: enemySpawnDelay global added")

# 6b: Set delay in buildStage after sisterMoving = false
old6b = "  sisterMoving = false; sisterMoveQueue = null; sisterTrail = []; brotherMoving = false;"
new6b = "  sisterMoving = false; sisterMoveQueue = null; sisterTrail = []; brotherMoving = false;\n  enemySpawnDelay = Date.now() + 3000;"
assert old6b in code, "Change 6b: sisterMoving=false line in buildStage not found"
code = code.replace(old6b, new6b, 1)
print("Change 6b done: enemySpawnDelay set in buildStage")

# 6c: Early return + restore alpha at start of enemy forEach in update
old6c = "  enemies.forEach(enemy => {\n    let chaseX = sister.x, chaseY = sister.y;"
new6c = (
    "  if (Date.now() < enemySpawnDelay) { enemies.forEach(e => e.sprite.setAlpha(0)); return; }\n"
    "  enemies.forEach(e => { if (e.sprite.alpha < 0.1) e.sprite.setAlpha(0.85); });\n"
    "  enemies.forEach(enemy => {\n"
    "    let chaseX = sister.x, chaseY = sister.y;"
)
assert old6c in code, "Change 6c: enemies.forEach start not found"
code = code.replace(old6c, new6c, 1)
print("Change 6c done: enemy spawn delay early-return added")

# ----------------------------------------------------------------
# Sanity check: brace balance
# ----------------------------------------------------------------
opens = code.count('{')
closes = code.count('}')
print(f"\nBrace check: {{ = {opens}, }} = {closes}, diff = {opens - closes}")
if opens != closes:
    print("WARNING: brace mismatch! Check the file.")
else:
    print("Brace count OK")

with open(dst, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\nDone! ameyodori_v14.html written ({len(code)} chars)")
print(f"Changes from v12: {len(code) - len(original):+d} chars")
