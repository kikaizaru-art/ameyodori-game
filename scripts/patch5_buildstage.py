"""
patch5: buildStage changes
  - Remove streetlightGlows/lightZones variable declarations
  - Replace init cleanup (streetlightGlows -> darkTileOverlays)
  - Replace tile building: remove TILE_STREETLIGHT/BREAKLIGHT/MIRROR lightZone push
  - Add TILE_DARK tile rendering
  - Update tileTexKeys and allTexKeys arrays
  - Update mirror mechanic: convert TILE_DARK -> TILE_FLOOR in MIRROR_RADIUS
  - Remove matchLightZone from lightZones
  - Remove breakable streetlight update block
  - Remove streetlight flicker code, add dark tile pulse
"""
PATH = r'C:\Users\kikai\OneDrive\Desktop\ameyodori_v13.html'
with open(PATH, encoding='utf-8') as f:
    code = f.read()

# ---- 1. Global variable declarations: remove streetlights, streetlightGlows, lightZones ----
OLD_VARS = "let walls, streetlights, mirrors;\nlet darkness, redOverlay;\nlet rainParticles = [], ripples = [], windStreaks = [];\nlet streetlightGlows = [], lightZones = [];"
NEW_VARS = "let walls, mirrors;\nlet darkness, redOverlay;\nlet rainParticles = [], ripples = [], windStreaks = [];\nlet darkTileOverlays = []; // track dark floor sprites for match pulse"
assert OLD_VARS in code, "global var block not found"
code = code.replace(OLD_VARS, NEW_VARS, 1)

# ---- 2. buildStage init cleanup: replace streetlightGlows/lightZones cleanup ----
OLD_INIT = (
    "  streetlights = [];\n"
    "  streetlightGlows.forEach(g => g.destroy());\n"
    "  streetlightGlows = [];\n"
    "  lightZones = [];\n"
    "  goalZones = [];"
)
NEW_INIT = (
    "  darkTileOverlays.forEach(o => o.destroy());\n"
    "  darkTileOverlays = [];\n"
    "  goalZones = [];"
)
assert OLD_INIT in code, "buildStage init cleanup not found"
code = code.replace(OLD_INIT, NEW_INIT, 1)

# ---- 3. tileTexKeys: swap streetlight/breaklight for dark_floor ----
OLD_TEXKEYS = (
    "  const tileTexKeys = [\n"
    "    'floor','wall','shop','streetlight','mirror','goal',\n"
    "    'breaklight','breaklight_dead','pushbox',\n"
    "    'switch_off','switch_on','door','match_item',\n"
    "    'hidden_wall','hidden_revealed',\n"
    "  ];"
)
NEW_TEXKEYS = (
    "  const tileTexKeys = [\n"
    "    'floor','dark_floor','wall','shop','mirror','goal',\n"
    "    'pushbox','switch_off','switch_on','door','match_item',\n"
    "    'hidden_wall','hidden_revealed',\n"
    "  ];"
)
assert OLD_TEXKEYS in code, "tileTexKeys not found"
code = code.replace(OLD_TEXKEYS, NEW_TEXKEYS, 1)

# ---- 4. Tile building loop: TILE_FLOOR + TILE_WALL + TILE_SHOP, then remove
#    TILE_STREETLIGHT + TILE_BREAKLIGHT blocks, add TILE_DARK block, fix TILE_MIRROR ----
OLD_TILES = (
    "      if (t === TILE_FLOOR) {\n"
    "        scene.add.image(x, y, 'floor').setDepth(0);\n"
    "      } else if (t === TILE_WALL) {\n"
    "        scene.add.image(x, y, 'wall').setDepth(0);\n"
    "        walls.create(x, y, 'wall').setSize(TILE, TILE).refreshBody();\n"
    "      } else if (t === TILE_SHOP) {\n"
    "        scene.add.image(x, y, 'shop').setDepth(0);\n"
    "        walls.create(x, y, 'shop').setSize(TILE, TILE).refreshBody();\n"
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
    "        });\n"
    "      } else if (t === TILE_MIRROR) {\n"
    "        scene.add.image(x, y, 'floor').setDepth(0);\n"
    "        scene.add.image(x, y, 'mirror').setDepth(2);\n"
    "        const m = mirrors.create(x, y, 'mirror').setSize(TILE, TILE).refreshBody();\n"
    "        m.isReflecting = false;\n"
    "        lightZones.push({ x, y, radius: 0, baseAlpha: 0.4, mirror: m });\n"
    "      } else if (t === TILE_GOAL) {\n"
    "        scene.add.image(x, y, 'goal').setDepth(0);\n"
    "        const gg = scene.add.image(x, y, 'goalglow').setBlendMode(Phaser.BlendModes.ADD).setAlpha(0.35).setDepth(5);\n"
    "        goalGlows.push(gg);\n"
    "        goalZones.push({ x, y });\n"
    "        lightZones.push({ x, y, radius: activeConfig.GOAL_LIGHT_RADIUS, baseAlpha: 0.35, goalGlow: gg });"
)
NEW_TILES = (
    "      if (t === TILE_FLOOR) {\n"
    "        scene.add.image(x, y, 'floor').setDepth(0);\n"
    "      } else if (t === TILE_DARK) {\n"
    "        // Dark road — enemies roam here, sister blocked unless match active\n"
    "        const dimg = scene.add.image(x, y, 'dark_floor').setDepth(0);\n"
    "        dimg.tileR = r; dimg.tileC = c;\n"
    "        darkTileOverlays.push(dimg);\n"
    "      } else if (t === TILE_WALL) {\n"
    "        scene.add.image(x, y, 'wall').setDepth(0);\n"
    "        walls.create(x, y, 'wall').setSize(TILE, TILE).refreshBody();\n"
    "      } else if (t === TILE_SHOP) {\n"
    "        scene.add.image(x, y, 'shop').setDepth(0);\n"
    "        walls.create(x, y, 'shop').setSize(TILE, TILE).refreshBody();\n"
    "      } else if (t === TILE_MIRROR) {\n"
    "        scene.add.image(x, y, 'floor').setDepth(0);\n"
    "        scene.add.image(x, y, 'mirror').setDepth(2);\n"
    "        const m = mirrors.create(x, y, 'mirror').setSize(TILE, TILE).refreshBody();\n"
    "        m.isReflecting = false;\n"
    "        // Store tile coords for TILE_DARK conversion mechanic\n"
    "        m.mirX = x; m.mirY = y; m.mirR = r; m.mirC = c;\n"
    "      } else if (t === TILE_GOAL) {\n"
    "        scene.add.image(x, y, 'goal').setDepth(0);\n"
    "        const gg = scene.add.image(x, y, 'goalglow').setBlendMode(Phaser.BlendModes.ADD).setAlpha(0.35).setDepth(5);\n"
    "        goalGlows.push(gg);\n"
    "        goalZones.push({ x, y });"
)
assert OLD_TILES in code, "tile building block not found"
code = code.replace(OLD_TILES, NEW_TILES, 1)

# ---- 5. matchLightZone: remove lightZones.push ----
OLD_MATCH_LZ = (
    "  matchGlow = scene.add.image(-200, -200, 'matchglow').setAlpha(0).setBlendMode(Phaser.BlendModes.ADD).setDepth(6);\n"
    "  matchLightZone = { x: -200, y: -200, radius: 0, baseAlpha: 0.4, isMatch: true };\n"
    "  lightZones.push(matchLightZone);"
)
NEW_MATCH_LZ = (
    "  matchGlow = scene.add.image(-200, -200, 'matchglow').setAlpha(0).setBlendMode(Phaser.BlendModes.ADD).setDepth(6);\n"
    "  matchLightZone = { x: -200, y: -200, radius: 0 }; // used for tile pulse and enemy repel"
)
assert OLD_MATCH_LZ in code, "matchLightZone push block not found"
code = code.replace(OLD_MATCH_LZ, NEW_MATCH_LZ, 1)

# ---- 6. Mirror update: replace lightZones mirror loop with TILE_DARK conversion ----
OLD_MIRROR = (
    "  // --- MIRROR UPDATE ---\n"
    "  lightZones.forEach(z => {\n"
    "    if (z.mirror) {\n"
    "      const d = Phaser.Math.Distance.Between(sister.x, sister.y, z.x, z.y);\n"
    "      z.radius = d < activeConfig.MIRROR_ACTIVATE_DIST ? activeConfig.MIRROR_RADIUS : 0;\n"
    "      z.mirror.isReflecting = d < activeConfig.MIRROR_ACTIVATE_DIST;\n"
    "    }\n"
    "  });"
)
NEW_MIRROR = (
    "  // --- MIRROR UPDATE ---\n"
    "  // When sister approaches a mirror, permanently convert TILE_DARK -> TILE_FLOOR nearby\n"
    "  mirrors.children.entries.forEach(m => {\n"
    "    if (m.mirR === undefined) return;\n"
    "    const d = Phaser.Math.Distance.Between(sister.x, sister.y, m.mirX, m.mirY);\n"
    "    m.isReflecting = d < activeConfig.MIRROR_ACTIVATE_DIST;\n"
    "    if (m.isReflecting && currentMap) {\n"
    "      const tileRadius = Math.ceil(activeConfig.MIRROR_RADIUS / TILE);\n"
    "      for (let dr = -tileRadius; dr <= tileRadius; dr++) {\n"
    "        for (let dc = -tileRadius; dc <= tileRadius; dc++) {\n"
    "          const tr = m.mirR + dr, tc = m.mirC + dc;\n"
    "          if (tr < 0 || tr >= ROWS || tc < 0 || tc >= COLS) continue;\n"
    "          if (currentMap[tr][tc] !== TILE_DARK) continue;\n"
    "          const dist = Math.sqrt((dr * TILE) ** 2 + (dc * TILE) ** 2);\n"
    "          if (dist <= activeConfig.MIRROR_RADIUS) {\n"
    "            currentMap[tr][tc] = TILE_FLOOR;\n"
    "            // Update visual: replace dark tile sprite with floor tile\n"
    "            const ov = darkTileOverlays.find(o => o.tileR === tr && o.tileC === tc);\n"
    "            if (ov) ov.setTexture('floor');\n"
    "            else currentScene.add.image(tc * TILE + TILE/2, tr * TILE + TILE/2, 'floor').setDepth(0);\n"
    "          }\n"
    "        }\n"
    "      }\n"
    "    }\n"
    "  });"
)
assert OLD_MIRROR in code, "MIRROR UPDATE block not found"
code = code.replace(OLD_MIRROR, NEW_MIRROR, 1)

# ---- 7. Remove breakable streetlight update block ----
OLD_BL = (
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
    "  });"
)
NEW_BL = "  // (breakable streetlights removed in v13 — replaced by dark tile mechanic)"
assert OLD_BL in code, "BREAKABLE STREETLIGHTS block not found"
code = code.replace(OLD_BL, NEW_BL, 1)

# ---- 8. Replace streetlight flicker code with dark tile pulse ----
OLD_FLICKER = (
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
    "  });"
)
NEW_FLICKER = (
    "  // Dark tile pulse: glow when match is active and tile is within match radius\n"
    "  if (darkTileOverlays.length > 0) {\n"
    "    const mRadius = matchActive ? (matchLightZone ? matchLightZone.radius : activeConfig.MATCH_LIGHT_RADIUS) : 0;\n"
    "    darkTileOverlays.forEach(ov => {\n"
    "      if (ov.texture && ov.texture.key !== 'dark_floor') return; // already converted\n"
    "      if (matchActive && mRadius > 0) {\n"
    "        const dist = Phaser.Math.Distance.Between(ov.x, ov.y, sister.x, sister.y);\n"
    "        if (dist < mRadius) {\n"
    "          ov.setTint(0x6633bb);\n"
    "          ov.setAlpha(0.5 + Math.sin(time / 180 + ov.x * 0.1) * 0.25);\n"
    "          return;\n"
    "        }\n"
    "      }\n"
    "      ov.clearTint();\n"
    "      ov.setAlpha(1);\n"
    "    });\n"
    "  }"
)
assert OLD_FLICKER in code, "Streetlight flicker block not found"
code = code.replace(OLD_FLICKER, NEW_FLICKER, 1)

# ---- 9. allTexKeys in triggerClear ----
OLD_ALL = (
    "  const allTexKeys = [\n"
    "    'floor','wall','shop','streetlight','mirror','goal',\n"
    "    'breaklight','breaklight_dead','pushbox',\n"
    "    'switch_off','switch_on','door','match_item',\n"
    "    'hidden_wall','hidden_revealed',\n"
    "  ];"
)
NEW_ALL = (
    "  const allTexKeys = [\n"
    "    'floor','dark_floor','wall','shop','mirror','goal',\n"
    "    'pushbox','switch_off','switch_on','door','match_item',\n"
    "    'hidden_wall','hidden_revealed',\n"
    "  ];"
)
assert OLD_ALL in code, "allTexKeys not found"
code = code.replace(OLD_ALL, NEW_ALL, 1)

# ---- 10. darkTileOverlays reset in retryStage ----
OLD_RETRY = "    darkness = null; redOverlay = null;\n    buildStage(currentScene);"
NEW_RETRY = "    darkness = null; redOverlay = null;\n    darkTileOverlays = [];\n    buildStage(currentScene);"
assert OLD_RETRY in code, "retryStage darkness reset not found"
code = code.replace(OLD_RETRY, NEW_RETRY, 1)

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(code)
print("patch5 OK — buildStage updated: dark tiles, no lightZones, mirror converts dark->light, dark pulse")
