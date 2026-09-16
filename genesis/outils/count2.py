import json, copy
from tools_naive import TOOLS
def ser(o,indent=None): return json.dumps(o,ensure_ascii=False,indent=indent,separators=(',',':') if indent is None else None)
LO,HI=3.5,2.9
def tk(c): return int(c/LO), int(c/HI)
T={t["name"]:t for t in TOOLS}

# ---- surcout de formatage : les harnais serialisent en JSON indente ----
mini=sum(len(ser(t)) for t in TOOLS); pretty=sum(len(ser(t,2)) for t in TOOLS)
print(f"JSON minifie  : {mini} car -> {tk(mini)[0]}-{tk(mini)[1]} tk")
print(f"JSON indente  : {pretty} car -> {tk(pretty)[0]}-{tk(pretty)[1]} tk  (x{pretty/mini:.2f})")

# ---- version compacte : descriptions courtes, params evidents non decrits ----
def compact(t):
    t=copy.deepcopy(t)
    t["description"]=t["description"].split(".")[0][:110]+"."
    for k,v in t["inputSchema"]["properties"].items():
        d=v.get("description","")
        if len(d)>60: v["description"]=d[:58].rsplit(" ",1)[0]+"."
        v.pop("default",None)
    return t
comp=[compact(t) for t in TOOLS]
cmini=sum(len(ser(t)) for t in comp)
print(f"\nCompact minifie: {cmini} car -> {tk(cmini)[0]}-{tk(cmini)[1]} tk  (-{100-100*cmini/mini:.0f}%)")

# ---- cloisonnement par role ----
ROLES={
 "Orchestrateur":["canon_search","canon_get_entity","canon_list_contradictions","jobs_list","jobs_status","canon_timeline"],
 "Sous-agent lore":["canon_get_entity","canon_search","canon_list_relations","canon_propose_fact","canon_get_schema","canon_get_knowledge","canon_timeline","canon_list_contradictions"],
 "Sous-agent visuel":["canon_get_entity","image_generate","image_list_styles","image_get","image_validate","image_describe","jobs_status"],
 "Sous-agent matiere":["canon_get_entity","mesh_generate","blender_open","blender_run","blender_bake","blender_screenshot","blender_export","unreal_import","unreal_screenshot","jobs_status"],
 "Sous-agent sonore":["canon_get_entity","voice_generate","music_generate","ambience_find","ambience_assemble","jobs_status"],
}
print("\n=== CLOISONNEMENT PAR ROLE (definitions compactes, indentees) ===")
mx=0
for r,names in ROLES.items():
    c=sum(len(ser(compact(T[n]),2)) for n in names)
    a,b=tk(c); mx=max(mx,b)
    print(f"{r:20s} {len(names):2d} outils  {a:5d}-{b:5d} tk")
print(f"\nPire cas pour un agent : ~{mx} tokens d'outils")
allp=sum(len(ser(t,2)) for t in TOOLS)
print(f"Tout charger d'un coup  : ~{tk(allp)[1]} tokens")
