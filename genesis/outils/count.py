import json, re
from tools_naive import TOOLS

def ser(o): return json.dumps(o, ensure_ascii=False, separators=(',',':'))

# Estimation calibrée : pour du JSON contenant du texte francais,
# les tokenizers BPE modernes (o200k, Qwen, Llama3) donnent ~2.9 a 3.5 car/token.
LO, HI = 3.5, 2.9   # LO -> borne basse de tokens, HI -> borne haute

groups = {"canon_":"Canon","jobs_":"File","image_":"Images",
          "mesh_":"3D","blender_":"3D","unreal_":"3D",
          "voice_":"Son","music_":"Son","ambience_":"Son"}

per = {}
rows=[]
tot_c=0
for t in TOOLS:
    c = len(ser(t)); tot_c += c
    srv = next(v for k,v in groups.items() if t["name"].startswith(k))
    per.setdefault(srv,[0,0]); per[srv][0]+=1; per[srv][1]+=c
    rows.append((t["name"], c))

def tk(c): return int(c/LO), int(c/HI)

print("=== PAR SERVEUR (version naive) ===")
for srv,(n,c) in sorted(per.items(), key=lambda x:-x[1][1]):
    a,b = tk(c)
    print(f"{srv:8s} {n:2d} outils  {c:6d} car  ->  {a:5d}-{b:5d} tokens   ({a//n}-{b//n} par outil)")
a,b = tk(tot_c)
print(f"{'TOTAL':8s} {len(TOOLS):2d} outils  {tot_c:6d} car  ->  {a:5d}-{b:5d} tokens")

print("\n=== 8 OUTILS LES PLUS LOURDS ===")
for name,c in sorted(rows,key=lambda r:-r[1])[:8]:
    a,b=tk(c); print(f"  {a:4d}-{b:4d} tk   {name}")
med = sorted(c for _,c in rows)[len(rows)//2]
a,b=tk(med); print(f"  mediane : {a}-{b} tokens par outil")
