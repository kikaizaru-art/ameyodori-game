"""
patch4: Movement rules
  - tryMoveSister: block TILE_DARK unless matchActive
  - Enemy AI: repelled from TILE_FLOOR tiles (light roads) instead of lightZones
  - Add tile helper functions (isOnLightTile, isOnDarkTile) to replace isInLight/getLightLevel
"""
PATH = r'C:\Users\kikai\OneDrive\Desktop\ameyodori_v13.html'
with open(PATH, encoding='utf-8') as f:
    code = f.read()

# ---- Replace LIGHT SYSTEM block with tile helpers ----
OLD_LIGHT = (
    "// ============================================\n"
    "// LIGHT SYSTEM\n"
    "// ============================================\n"
    "function isInLight(x, y) {\n"
    "  for (const z of lightZones) {\n"
    "    if (z.radius > 0 && Phaser.Math.Distance.Between(x, y, z.x, z.y) < z.radius) return true;\n"
    "  }\n"
    "  return false;\n"
    "}\n"
    "\n"
    "function getLightLevel(x, y) {\n"
    "  let lv = 0;\n"
    "  for (const z of lightZones) {\n"
    "    if (z.radius > 0) {\n"
    "      lv += Math.max(0, 1 - Phaser.Math.Distance.Between(x, y, z.x, z.y) / z.radius) * 0.6;\n"
    "    }\n"
    "  }\n"
    "  return Math.min(lv, 1);\n"
    "}"
)
NEW_LIGHT = (
    "// ============================================\n"
    "// TILE HELPERS (replace light-zone system)\n"
    "// ============================================\n"
    "function getTileAtPixel(px, py) {\n"
    "  const r = Math.floor(py / TILE);\n"
    "  const c = Math.floor(px / TILE);\n"
    "  if (!currentMap || r < 0 || r >= ROWS || c < 0 || c >= COLS) return TILE_WALL;\n"
    "  return currentMap[r][c];\n"
    "}\n"
    "\n"
    "function isOnLightTile(sprite) {\n"
    "  const t = getTileAtPixel(sprite.x, sprite.y);\n"
    "  return t === TILE_FLOOR || t === TILE_GOAL;\n"
    "}\n"
    "\n"
    "function isOnDarkTile(sprite) {\n"
    "  return getTileAtPixel(sprite.x, sprite.y) === TILE_DARK;\n"
    "}"
)
assert OLD_LIGHT in code, "LIGHT SYSTEM block not found"
code = code.replace(OLD_LIGHT, NEW_LIGHT, 1)

# ---- tryMoveSister: add TILE_DARK block ----
OLD_MOVE = (
    "  if (!currentMap) return;\n"
    "  const t = currentMap[nr][nc];\n"
    "  if (t === TILE_WALL || t === TILE_SHOP || t === TILE_DOOR || t === TILE_HIDDEN || t === TILE_MIRROR) return;"
)
NEW_MOVE = (
    "  if (!currentMap) return;\n"
    "  const t = currentMap[nr][nc];\n"
    "  if (t === TILE_WALL || t === TILE_SHOP || t === TILE_DOOR || t === TILE_HIDDEN || t === TILE_MIRROR) return;\n"
    "  // Dark tiles are impassable unless a match is active\n"
    "  if (t === TILE_DARK && !matchActive) return;"
)
assert OLD_MOVE in code, "tryMoveSister passable check not found"
code = code.replace(OLD_MOVE, NEW_MOVE, 1)

# ---- Enemy AI: replace lightZone-based repel with tile-based repel ----
OLD_REPEL = (
    "    // Light repel (マッチは特別に強い反発力)\n"
    "    const ell = getLightLevel(enemy.x, enemy.y);\n"
    "    if (ell > activeConfig.ENEMY_LIGHT_REPEL_THRESHOLD) {\n"
    "      // 最も近い光源を探す\n"
    "      let nLX = enemy.x, nLY = enemy.y, nLD = 9999;\n"
    "      let nearestIsMatch = false;\n"
    "      for (const z of lightZones) {\n"
    "        if (z.radius <= 0) continue;\n"
    "        const ld = Phaser.Math.Distance.Between(enemy.x, enemy.y, z.x, z.y);\n"
    "        if (ld < nLD) { nLD = ld; nLX = z.x; nLY = z.y; nearestIsMatch = !!z.isMatch; }\n"
    "      }\n"
    "      if (nLD < 9999) {\n"
    "        // マッチの光は通常の3倍の反発力\n"
    "        const multiplier = nearestIsMatch ? (activeConfig.MATCH_REPEL_MULTIPLIER || 3) : 1;\n"
    "        const repelStr = ell * activeConfig.ENEMY_LIGHT_REPEL_STRENGTH * multiplier;\n"
    "        const ax = enemy.x - nLX, ay = enemy.y - nLY, ad = Math.sqrt(ax * ax + ay * ay) || 1;\n"
    "        enemy.x += (ax / ad) * repelStr * dt;\n"
    "        enemy.y += (ay / ad) * repelStr * dt;\n"
    "      }\n"
    "    }"
)
NEW_REPEL = (
    "    // Tile-based repel: enemies are repelled from TILE_FLOOR (light roads)\n"
    "    // Match active = much stronger repulsion (matchActive makes dark tiles also repel)\n"
    "    {\n"
    "      const eR = Math.floor(enemy.y / TILE);\n"
    "      const eC = Math.floor(enemy.x / TILE);\n"
    "      let repelX = 0, repelY = 0;\n"
    "      for (let dr = -2; dr <= 2; dr++) {\n"
    "        for (let dc = -2; dc <= 2; dc++) {\n"
    "          const tr = eR + dr, tc = eC + dc;\n"
    "          if (tr < 0 || tr >= ROWS || tc < 0 || tc >= COLS) continue;\n"
    "          const tt = currentMap ? currentMap[tr][tc] : TILE_WALL;\n"
    "          const isRepellent = (tt === TILE_FLOOR || tt === TILE_GOAL) ||\n"
    "                              (matchActive && tt === TILE_DARK);\n"
    "          if (!isRepellent) continue;\n"
    "          const fx = tc * TILE + TILE / 2, fy = tr * TILE + TILE / 2;\n"
    "          const fd = Phaser.Math.Distance.Between(enemy.x, enemy.y, fx, fy) || 1;\n"
    "          if (fd < TILE * 2.5) {\n"
    "            const strength = (matchActive && tt === TILE_DARK)\n"
    "              ? activeConfig.ENEMY_LIGHT_REPEL_STRENGTH * (activeConfig.MATCH_REPEL_MULTIPLIER || 3)\n"
    "              : activeConfig.ENEMY_LIGHT_REPEL_STRENGTH;\n"
    "            repelX += (enemy.x - fx) / fd * strength * dt;\n"
    "            repelY += (enemy.y - fy) / fd * strength * dt;\n"
    "          }\n"
    "        }\n"
    "      }\n"
    "      enemy.x += repelX;\n"
    "      enemy.y += repelY;\n"
    "    }"
)
assert OLD_REPEL in code, "Enemy light repel block not found"
code = code.replace(OLD_REPEL, NEW_REPEL, 1)

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(code)
print("patch4 OK — tile helpers added, tryMoveSister blocks dark, enemy uses tile-based repel")
