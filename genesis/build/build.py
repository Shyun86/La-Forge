#!/usr/bin/env python3
"""Le seul script à lancer.

    python3 build.py              → injecte les schémas, puis la navigation,
                                    puis liste ce qui doit être republié
    python3 build.py publie A B   → enregistre que A et B viennent d'être publiés

Pourquoi ce dernier verbe : les fichiers locaux sont toujours à jour après un
build, mais les pages en ligne gardent la version qu'elles avaient au moment de
leur publication. Sans registre, on oublie d'en republier une — c'est arrivé
avec les pièces 00 et 01, qui ignoraient le glossaire.

Le registre stocke une empreinte du contenu de chaque fichier au moment de sa
publication. Tout écart = page en ligne périmée.
"""
import hashlib, json, pathlib, sys

import build_schemas
import build_nav

ROOT = pathlib.Path(__file__).parent
REGISTRE = ROOT / "publie.json"


def empreinte(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def registre() -> dict:
    if REGISTRE.exists():
        return json.loads(REGISTRE.read_text(encoding="utf-8"))
    return {}


def cle(p: pathlib.Path) -> str:
    return str(p.relative_to(ROOT.parent))


def marquer(noms):
    reg = registre()
    connus = {p.name: p for p in build_nav.targets()}
    for n in noms:
        p = connus.get(n) or connus.get(n + ".html")
        if p is None or not p.exists():
            print(f"  inconnu : {n}")
            continue
        reg[cle(p)] = empreinte(p)
        print(f"  publié  : {cle(p)}")
    REGISTRE.write_text(json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")


def perimes() -> list:
    reg = registre()
    out = []
    for p in build_nav.targets():
        if not p.exists():
            continue
        k = cle(p)
        if k not in reg:
            out.append((k, "jamais publié"))
        elif reg[k] != empreinte(p):
            out.append((k, "modifié depuis la publication"))
    return out


def main():
    print("— schémas —")
    manque = build_schemas.main()

    print("\n— navigation —")
    build_nav.main()

    print("\n— à republier —")
    p = perimes()
    if not p:
        print("  rien : tout ce qui est en ligne correspond au local.")
    for k, why in p:
        print(f"  · {k}  ({why})")

    if manque:
        print("\n  (voir aussi les marqueurs de schéma manquants ci-dessus)")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "publie":
        marquer(sys.argv[2:])
    else:
        main()
