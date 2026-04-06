"""
patch6: Fear gauge + misc cleanup
  - Replace brotherInLight (lightZone-based) with brotherOnLight (tile-based)
  - Simplify fear rate: light tile = decreases, dark tile = increases
  - Remove STREETLIGHT_RADIUS/BREAKLIGHT_* from CONFIG and STAGE overrides
  - Remove DARKNESS_BASE (tiles communicate darkness now, overlay stays subtle)
  - Fix any stale brotherInLight references
  - Update story text (streetlight -> light road mechanic)
  - findNearestFloor: also accept TILE_DARK as fallback
  - scoreItems: allow placement on TILE_DARK
"""
PATH = r'C:\Users\kikai\OneDrive\Desktop\ameyodori_v13.html'
with open(PATH, encoding='utf-8') as f:
    code = f.read()

# ---- 1. CONFIG: remove STREETLIGHT_RADIUS ----
OLD_CONFIG_SL = (
    "  // 光源\n"
    "  STREETLIGHT_RADIUS: 70,\n"
    "  MIRROR_RADIUS: 60,"
)
NEW_CONFIG_SL = (
    "  // 光源\n"
    "  MIRROR_RADIUS: 60,"
)
assert OLD_CONFIG_SL in code, "CONFIG STREETLIGHT_RADIUS not found"
code = code.replace(OLD_CONFIG_SL, NEW_CONFIG_SL, 1)

# ---- 2. CONFIG: remove BREAKLIGHT_LIFETIME and BREAKLIGHT_WARN_TIME ----
OLD_CONFIG_BL = (
    "  // ギミック\n"
    "  BREAKLIGHT_LIFETIME: 15,\n"
    "  BREAKLIGHT_WARN_TIME: 5,\n"
    "  MATCH_LIGHT_RADIUS: 80,"
)
NEW_CONFIG_BL = (
    "  // ギミック\n"
    "  MATCH_LIGHT_RADIUS: 80,"
)
assert OLD_CONFIG_BL in code, "CONFIG BREAKLIGHT block not found"
code = code.replace(OLD_CONFIG_BL, NEW_CONFIG_BL, 1)

# ---- 3. STAGE2_OVERRIDES: remove STREETLIGHT_RADIUS and BREAKLIGHT_LIFETIME ----
OLD_S2_OV = (
    "  STREETLIGHT_RADIUS: 45,\n"
    "  MIRROR_RADIUS: 40,\n"
    "  GOAL_LIGHT_RADIUS: 50,"
)
NEW_S2_OV = (
    "  MIRROR_RADIUS: 40,\n"
    "  GOAL_LIGHT_RADIUS: 50,"
)
assert OLD_S2_OV in code, "STAGE2_OVERRIDES STREETLIGHT_RADIUS not found"
code = code.replace(OLD_S2_OV, NEW_S2_OV, 1)

OLD_S2_BL = "  BREAKLIGHT_LIFETIME: 12,\n};\n\n// ステージ3 CONFIG上書き"
NEW_S2_BL = "};\n\n// ステージ3 CONFIG上書き"
assert OLD_S2_BL in code, "STAGE2_OVERRIDES BREAKLIGHT_LIFETIME not found"
code = code.replace(OLD_S2_BL, NEW_S2_BL, 1)

# ---- 4. STAGE3_OVERRIDES: remove STREETLIGHT_RADIUS and BREAKLIGHT_LIFETIME ----
OLD_S3_OV = (
    "  STREETLIGHT_RADIUS: 55,\n"
    "  MIRROR_RADIUS: 50,\n"
    "  GOAL_LIGHT_RADIUS: 55,"
)
NEW_S3_OV = (
    "  MIRROR_RADIUS: 50,\n"
    "  GOAL_LIGHT_RADIUS: 55,"
)
assert OLD_S3_OV in code, "STAGE3_OVERRIDES STREETLIGHT_RADIUS not found"
code = code.replace(OLD_S3_OV, NEW_S3_OV, 1)

OLD_S3_BL = "  BREAKLIGHT_LIFETIME: 10,\n  LIGHTNING_INTERVAL_MIN"
NEW_S3_BL = "  LIGHTNING_INTERVAL_MIN"
assert OLD_S3_BL in code, "STAGE3_OVERRIDES BREAKLIGHT_LIFETIME not found"
code = code.replace(OLD_S3_BL, NEW_S3_BL, 1)

# ---- 5. Fear gauge: replace brotherInLight with tile-based brotherOnLight ----
OLD_BIL = (
    "  // --- BROTHER AI (grid-based, follows sister's trail) ---\n"
    "  const brotherInLight = isInLight(brother.x, brother.y);\n"
    "  var brotherInLightGlobal = brotherInLight; // HUD参照用\n"
    "  brother.setVelocity(0, 0);"
)
NEW_BIL = (
    "  // --- BROTHER AI (grid-based, follows sister's trail) ---\n"
    "  const brotherOnLight = isOnLightTile(brother); // tile-based: TILE_FLOOR or TILE_GOAL\n"
    "  const sisterOnLight = isOnLightTile(sister);\n"
    "  brother.setVelocity(0, 0);"
)
assert OLD_BIL in code, "brotherInLight declaration not found"
code = code.replace(OLD_BIL, NEW_BIL, 1)

# ---- 6. Fear gauge calculation: use brotherOnLight ----
OLD_FEAR = (
    "  // --- FEAR GAUGE ---\n"
    "  const enemyFearBonus = matchActive ? 0 : Math.max(0, (activeConfig.FEAR_ENEMY_RANGE - closestEnemyDist) / activeConfig.FEAR_ENEMY_RANGE) * activeConfig.FEAR_ENEMY_MAX;\n"
    "  const baseRate = (brotherInLight || matchActive) ? activeConfig.FEAR_RATE_LIT : activeConfig.FEAR_RATE_DARK;\n"
    "  const holdBonus = isHoldingHand ? activeConfig.FEAR_HOLDING_BONUS : 0;\n"
    "  const matchBonus = matchActive ? -25 : 0; // マッチ使用中は恐怖が急速回復\n"
    "  fearGauge = Phaser.Math.Clamp(fearGauge + (baseRate + enemyFearBonus + holdBonus + matchBonus) * dt, 0, 100);"
)
NEW_FEAR = (
    "  // --- FEAR GAUGE ---\n"
    "  const enemyFearBonus = matchActive ? 0 : Math.max(0, (activeConfig.FEAR_ENEMY_RANGE - closestEnemyDist) / activeConfig.FEAR_ENEMY_RANGE) * activeConfig.FEAR_ENEMY_MAX;\n"
    "  // Tile-based fear: light road = safe (decrease), dark road = scary (increase)\n"
    "  // Match active on dark = slower fear increase (dim light helps)\n"
    "  const baseRate = brotherOnLight\n"
    "    ? activeConfig.FEAR_RATE_LIT\n"
    "    : (matchActive ? activeConfig.FEAR_RATE_DARK * 0.4 : activeConfig.FEAR_RATE_DARK);\n"
    "  const holdBonus = isHoldingHand ? activeConfig.FEAR_HOLDING_BONUS : 0;\n"
    "  const matchBonus = matchActive ? -25 : 0; // マッチ使用中は恐怖が急速回復\n"
    "  fearGauge = Phaser.Math.Clamp(fearGauge + (baseRate + enemyFearBonus + holdBonus + matchBonus) * dt, 0, 100);"
)
assert OLD_FEAR in code, "fear gauge calculation not found"
code = code.replace(OLD_FEAR, NEW_FEAR, 1)

# ---- 7. Fix brotherInLight refs in brother-status DOM element ----
OLD_BSTATUS = (
    "  document.getElementById('brother-status').textContent =\n"
    "    brother.fearFrozen ? '😰 うずくまり中...' :\n"
    "    isHoldingHand ? '🤝 手をつないでいる' :\n"
    "    brotherInLight ? '追従中' : '⚠ 暗闇で鈍化中...';"
)
NEW_BSTATUS = (
    "  document.getElementById('brother-status').textContent =\n"
    "    brother.fearFrozen ? '😰 うずくまり中...' :\n"
    "    isHoldingHand ? '🤝 手をつないでいる' :\n"
    "    brotherOnLight ? '追従中' : '⚠ 暗い道にいる...';"
)
assert OLD_BSTATUS in code, "brother-status DOM ref not found"
code = code.replace(OLD_BSTATUS, NEW_BSTATUS, 1)

# ---- 8. Fix HUD bro-status (brotherInLightGlobal) ----
OLD_HUD = (
    "    else if (typeof brotherInLightGlobal !== 'undefined' && !brotherInLightGlobal) broStatus.textContent = '⚠暗';\n"
    "    else broStatus.textContent = '追従';"
)
NEW_HUD = "    else broStatus.textContent = '追従';"
assert OLD_HUD in code, "HUD brotherInLightGlobal not found"
code = code.replace(OLD_HUD, NEW_HUD, 1)

# ---- 9. Darkness overlay: reduce alpha (tiles communicate dark, overlay is subtle) ----
OLD_DARK = (
    "  let darkAlpha = activeConfig.DARKNESS_BASE + Math.max(0, (200 - closestEnemyDist) / 200) * activeConfig.DARKNESS_ENEMY_BONUS;\n"
    "  // Lightning dark phase adds extra darkness\n"
    "  if (currentStage === 3 && lightningPhase === 'dark') {\n"
    "    darkAlpha = Math.min(darkAlpha + 0.12, 0.97);\n"
    "  }\n"
    "  darkness.setAlpha(darkAlpha);"
)
NEW_DARK = (
    "  // Darkness overlay: tiles communicate dark vs light; overlay stays subtle\n"
    "  let darkAlpha = 0.40 + Math.max(0, (200 - closestEnemyDist) / 200) * activeConfig.DARKNESS_ENEMY_BONUS;\n"
    "  if (currentStage === 3 && lightningPhase === 'dark') {\n"
    "    darkAlpha = Math.min(darkAlpha + 0.15, 0.85);\n"
    "  }\n"
    "  darkness.setAlpha(darkAlpha);"
)
assert OLD_DARK in code, "darkness alpha block not found"
code = code.replace(OLD_DARK, NEW_DARK, 1)

# ---- 10. Story text: replace streetlight mention with light/dark road mechanic ----
OLD_STORY = (
    "      影が、追ってくる。<br>\n"
    "      <span>街灯</span>の光だけが頼り。<br>\n"
    "      弟の手を離さないで。"
)
NEW_STORY = (
    "      影が、追ってくる。<br>\n"
    "      <span>明るい道</span>を歩け。<span>暗い道</span>には入るな。<br>\n"
    "      マッチの灯で、闇を照らせ。<br>\n"
    "      弟の手を離さないで。"
)
assert OLD_STORY in code, "story text not found"
code = code.replace(OLD_STORY, NEW_STORY, 1)

# ---- 11. findNearestFloor: accept TILE_DARK as fallback spawn ----
OLD_FNF = (
    "          if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS && MAP[nr] && MAP[nr][nc] === TILE_FLOOR) {\n"
    "            return {r: nr, c: nc};\n"
    "          }"
)
NEW_FNF = (
    "          const ft = MAP[nr] ? MAP[nr][nc] : TILE_WALL;\n"
    "          if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS && (ft === TILE_FLOOR || ft === TILE_DARK)) {\n"
    "            return {r: nr, c: nc};\n"
    "          }"
)
assert OLD_FNF in code, "findNearestFloor inner check not found"
code = code.replace(OLD_FNF, NEW_FNF, 1)

# ---- 12. scoreItems: allow placement on TILE_DARK too ----
OLD_SCORE = (
    "  scorePositions.forEach(sp => {\n"
    "    if (!MAP[sp.r] || MAP[sp.r][sp.c] !== TILE_FLOOR) return; // skip if not on floor"
)
NEW_SCORE = (
    "  scorePositions.forEach(sp => {\n"
    "    const st = MAP[sp.r] ? MAP[sp.r][sp.c] : TILE_WALL;\n"
    "    if (st === TILE_WALL || st === TILE_SHOP || st === TILE_DOOR) return; // allow floor or dark"
)
assert OLD_SCORE in code, "scoreItems floor check not found"
code = code.replace(OLD_SCORE, NEW_SCORE, 1)

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(code)
print("patch6 OK — fear gauge uses tile-based logic, CONFIG cleaned, story updated, misc fixed")
