"""
patch1: Add TILE_DARK=13 constant after TILE_HIDDEN=11
"""
PATH = r'C:\Users\kikai\OneDrive\Desktop\ameyodori_v13.html'
with open(PATH, encoding='utf-8') as f:
    code = f.read()

OLD = 'const TILE_HIDDEN = 11;'
NEW = 'const TILE_HIDDEN = 11;\nconst TILE_DARK = 13;'
assert OLD in code, "TILE_HIDDEN not found"
code = code.replace(OLD, NEW, 1)

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(code)
print("patch1 OK — TILE_DARK=13 added")
