"""
patch2: Replace streetlight/breaklight textures with dark_floor texture.
        Remove streetglow texture. Keep matchglow.
"""
PATH = r'C:\Users\kikai\OneDrive\Desktop\ameyodori_v13.html'
with open(PATH, encoding='utf-8') as f:
    code = f.read()

# --- Remove streetlight, breaklight, breaklight_dead textures ---
OLD_SL = (
    "  // streetlight\n"
    "  g.clear(); g.fillStyle(0x1a1a2e); g.fillRect(0,0,TILE,TILE);\n"
    "  g.fillStyle(0x555566); g.fillRect(14,8,4,20);\n"
    "  g.fillStyle(0xffdd88); g.fillRect(10,4,12,6);\n"
    "  g.generateTexture('streetlight', TILE, TILE);\n"
    "\n"
    "  // breakable streetlight (reddish tint, crack mark)\n"
    "  g.clear(); g.fillStyle(0x1a1a2e); g.fillRect(0,0,TILE,TILE);\n"
    "  g.fillStyle(0x665544); g.fillRect(14,8,4,20);\n"
    "  g.fillStyle(0xffcc66); g.fillRect(10,4,12,6);\n"
    "  g.fillStyle(0xcc4422); g.fillRect(10,2,2,2);\n"
    "  g.generateTexture('breaklight', TILE, TILE);\n"
    "\n"
    "  // dead breakable streetlight\n"
    "  g.clear(); g.fillStyle(0x1a1a2e); g.fillRect(0,0,TILE,TILE);\n"
    "  g.fillStyle(0x333333); g.fillRect(14,8,4,20);\n"
    "  g.fillStyle(0x444444); g.fillRect(10,4,12,6);\n"
    "  g.generateTexture('breaklight_dead', TILE, TILE);\n"
    "\n"
    "  // mirror"
)
NEW_SL = (
    "  // dark road tile — dark purple base with faint grid lines\n"
    "  g.clear(); g.fillStyle(0x0e0a18); g.fillRect(0,0,TILE,TILE);\n"
    "  g.fillStyle(0x2a1845, 0.4); g.fillRect(0,0,TILE,1); g.fillRect(0,0,1,TILE);\n"
    "  g.fillStyle(0x1a1030, 0.25); g.fillRect(4,4,TILE-8,TILE-8);\n"
    "  g.generateTexture('dark_floor', TILE, TILE);\n"
    "\n"
    "  // mirror"
)
assert OLD_SL in code, "streetlight texture block not found"
code = code.replace(OLD_SL, NEW_SL, 1)

# --- Remove streetglow texture (keep matchglow) ---
OLD_SG = (
    "  // streetglow (dimmer)\n"
    "  g.clear();\n"
    "  for (let i = 32; i > 0; i--) {\n"
    "    g.fillStyle(0xffddaa, (1-i/32)*0.18);\n"
    "    g.fillCircle(80,80,(i/32)*80);\n"
    "  }\n"
    "  g.generateTexture('streetglow', 160, 160);\n"
    "\n"
    "  // matchglow"
)
NEW_SG = "  // matchglow"
assert OLD_SG in code, "streetglow texture block not found"
code = code.replace(OLD_SG, NEW_SG, 1)

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(code)
print("patch2 OK — dark_floor texture added, streetlight/glow textures removed")
