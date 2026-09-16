# Budget de contexte d'un tour, sous-agent lore (le pire cas), fenetre 32k utile
W=32768
FIXE = {
 "Instructions systeme de l'agent": 750,
 "Definitions d'outils (compact, cloisonne)": 2750,
 "Fiche de style / regles d'ecriture": 400,
}
RESERVE = {"Reserve pour la reponse du modele": 3000}

# contexte canon injecte, budget par couche facon AutoWorldBuilder mais en mode 'riche'
CANON = {
 "Essentiel (20%)": 800,
 "Pertinent, recupere (35%)": 1400,
 "Resume (20%)": 800,
 "Collaboration inter-agents (25%)": 1000,
}
f=sum(FIXE.values()); r=sum(RESERVE.values()); c=sum(CANON.values())
print("=== BUDGET D'UN TOUR (fenetre 32 768) ===")
for k,v in {**FIXE,**CANON,**RESERVE}.items(): print(f"  {v:6d}  {k}")
print(f"  ------")
print(f"  {f+c+r:6d}  sous-total incompressible ({100*(f+c+r)/W:.0f}% de la fenetre)")
print(f"  {W-f-c-r:6d}  RESTE pour la conversation et les resultats d'outils\n")

# accumulation sur une session
print("=== CE QUI SATURE REELLEMENT : les resultats d'outils ===")
RES = {"canon_get_entity (fiche complete)":1200,"canon_search (10 resultats)":900,
       "canon_list_relations (profondeur 2)":1500,"canon_get_knowledge":700,
       "canon_list_contradictions":600,"blender_screenshot (image)":1600}
for k,v in RES.items(): print(f"  {v:6d}  {k}")
budget=W-f-c-r
print(f"\n  Budget disponible : {budget}")
moy=sum(RES.values())/len(RES)
print(f"  Appel d'outil moyen : {moy:.0f} tokens de resultat")
print(f"  -> saturation apres ~{budget/(moy+250):.0f} appels d'outils dans un meme fil")
print(f"     (250 tk = le message de l'agent qui accompagne chaque appel)")

print("\n=== SI ON NE CLOISONNE PAS (39 outils charges) ===")
f2 = f - 2750 + 12308
print(f"  Sous-total incompressible : {f2+c+r} ({100*(f2+c+r)/W:.0f}% de la fenetre)")
print(f"  Reste : {W-f2-c-r}  ->  ~{(W-f2-c-r)/(moy+250):.0f} appels d'outils seulement")
