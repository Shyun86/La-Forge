#!/usr/bin/env python3
"""Génère et injecte la barre de navigation dans le dossier ET les documents amont.

Usage : python3 build_nav.py
Met à jour le bloc <!--NAV--> ... <!--/NAV--> de chaque fichier listé.
Quand une nouvelle pièce est publiée, ajouter son URL dans PIECES et relancer.
"""
import re, pathlib

ROOT   = pathlib.Path(__file__).parent          # .../genesis/build  (ce script)
GROOT  = ROOT.parent                            # .../genesis        (racine du module)
PIECES_DIR = GROOT/"pieces"
AMONT_DIR  = GROOT/"amont"
UP = GROOT  # conservé pour les chemins relatifs affichés dans les logs

INDEX_URL = "https://claude.ai/code/artifact/58018a5a-16d8-4369-b076-cba5f54d18e2"

# (numéro, titre court, chemin, URL publiée ou None)
PIECES = [
    ("00", "Principes & règles",      PIECES_DIR/"00-principes.html",    "https://claude.ai/code/artifact/875328e3-7c7e-4455-8b34-e33f6411e8d6"),
    ("01", "Stack technique",         PIECES_DIR/"01-stack.html",         "https://claude.ai/code/artifact/4c2f6d71-1f24-451b-b2d5-27fcf394b8f9"),
    ("02", "Architecture",            PIECES_DIR/"02-architecture.html",  "https://claude.ai/code/artifact/f318e04b-8c92-4ee5-a51f-67133952aee3"),
    ("03", "Le Canon",                PIECES_DIR/"03-canon.html",         "https://claude.ai/code/artifact/e7e413f8-7559-42d1-a56e-c0d77f230597"),
    ("04", "La File des travaux",     PIECES_DIR/"04-file.html",          "https://claude.ai/code/artifact/f61c1dea-fdc2-4edf-bec4-9620464e1cc0"),
    ("05", "Le Catalogue",            PIECES_DIR/"05-catalogue.html",     None),
    ("06", "Le Récit",                PIECES_DIR/"06-recit.html",         None),
    ("07", "La Bibliothèque",         PIECES_DIR/"07-bibliotheque.html",  None),
    ("08", "Les rôles",               PIECES_DIR/"08-roles.html",         None),
    ("09", "L'Assistant",             PIECES_DIR/"09-assistant.html",     None),
    ("10", "Les recettes",            PIECES_DIR/"10-recettes.html",      None),
    ("11", "Images",                  PIECES_DIR/"11-images.html",        None),
    ("12", "3D",                      PIECES_DIR/"12-3d.html",            None),
    ("13", "Son",                     PIECES_DIR/"13-son.html",           None),
    ("14", "Les modèles",             PIECES_DIR/"14-modeles.html",       None),
    ("15", "Outils externes",         PIECES_DIR/"15-externes.html",      None),
    ("16", "Emplacements & stockage", PIECES_DIR/"16-stockage.html",      None),
    ("17", "Les liaisons",            PIECES_DIR/"17-liaisons.html",      None),
    ("18", "L'interface",             PIECES_DIR/"18-interface.html",     None),
    ("19", "Budget & consommation",   PIECES_DIR/"19-budget.html",        None),
    ("20", "Extensibilité & final",   PIECES_DIR/"20-extensibilite.html", None),
]

# (titre, chemin, URL)
AMONT = [
    ("Dossier de recherche",  AMONT_DIR/"forge.html",  "https://claude.ai/code/artifact/7239eea6-ecd0-4191-8f82-0bc1d30f4ca1"),
    ("Écrire ou déléguer",    AMONT_DIR/"bc.html",     "https://claude.ai/code/artifact/9145bc40-e4ec-4a1d-a246-901eed85c284"),
    ("Le plan de la Forge",   AMONT_DIR/"plan.html",   "https://claude.ai/code/artifact/5e3c070a-93a8-4ef2-bd4d-80633d85d0ba"),
    ("Le budget de contexte", AMONT_DIR/"budget.html", "https://claude.ai/code/artifact/26067661-97b6-4373-a778-245c83af0304"),
]

INDEX = GROOT/"index.html"
GLOSSAIRE = GROOT/"glossaire.html"
GLOSSAIRE_URL = "https://claude.ai/code/artifact/32346ead-8a36-46fb-9715-bf59c0e87cd3"
SCHEMAS = GROOT/"schemas.html"
SCHEMAS_URL = "https://claude.ai/code/artifact/b469a4b3-9ab7-488e-b28e-984e17f1446d"

NAV_CSS = """
<style id="navcss">
.fnav{position:sticky;top:0;z-index:50;background:var(--surface);border-bottom:1px solid var(--rule);
  font-family:var(--f-mono);font-size:12px;letter-spacing:.03em}
.fnav-in{max-width:var(--nav-w,1040px);margin:0 auto;padding:0 24px;display:flex;align-items:center;
  gap:10px;min-height:46px;flex-wrap:wrap}
.fnav a{color:var(--ink-2);text-decoration:none;padding:5px 9px;border-radius:4px;white-space:nowrap}
.fnav a:hover,.fnav a:focus-visible{color:var(--ember);background:var(--surface-2)}
.fnav .home{font-weight:600;color:var(--ink);padding-left:0}
.fnav .home:hover{background:none}
.fnav .sep{color:var(--rule);user-select:none}
.fnav .here{color:var(--ember);font-weight:600;padding:5px 0}
.fnav .kind{color:var(--ink-3);padding:5px 0}
.fnav .spacer{flex:1;min-width:8px}
.fnav .pn{display:flex;gap:4px;align-items:center}
.fnav .pn .off{color:var(--ink-3);opacity:.45;padding:5px 9px;white-space:nowrap}
.fnav .fixes{display:flex;gap:2px;align-items:center}
.fnav .fixes a{border:1px solid transparent}
.fnav .fixes a:hover{border-color:var(--ember)}
.fnav .fixes .off{color:var(--ink-3);opacity:.45;padding:5px 9px}
details.fmenu{position:relative}
details.fmenu>summary{list-style:none;cursor:pointer;padding:5px 10px;border:1px solid var(--rule);
  border-radius:4px;color:var(--ink-2);white-space:nowrap;user-select:none}
details.fmenu>summary::-webkit-details-marker{display:none}
details.fmenu>summary:hover{color:var(--ember);border-color:var(--ember)}
details.fmenu[open]>summary{color:var(--ember);border-color:var(--ember);background:var(--surface-2)}
.fmenu-panel{position:absolute;right:0;top:calc(100% + 8px);width:min(92vw,680px);
  background:var(--surface);border:1px solid var(--rule);border-radius:6px;box-shadow:var(--shadow);
  padding:14px;display:grid;gap:2px;max-height:min(70vh,620px);overflow-y:auto}
@media(min-width:640px){.fmenu-panel{grid-template-columns:1fr 1fr}}
.fmenu-panel .grp{grid-column:1/-1;font-size:10px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-3);padding:8px 6px 5px;border-bottom:1px solid var(--rule);margin-bottom:3px;
  opacity:.85;background:none;font-family:var(--f-mono)}
.fmenu-panel .grp:not(:first-child){margin-top:10px}
.fmenu-panel a,.fmenu-panel span.off{display:flex;gap:9px;padding:6px 8px;border-radius:4px;
  font-size:12.5px;align-items:baseline;text-decoration:none;white-space:normal}
.fmenu-panel a{color:var(--ink-2)}
.fmenu-panel a:hover,.fmenu-panel a:focus-visible{background:var(--surface-2);color:var(--ember)}
.fmenu-panel span.off{color:var(--ink-3);opacity:.5}
.fmenu-panel .num{color:var(--ember);font-weight:600;min-width:22px;flex:none}
.fmenu-panel span.off .num{color:var(--ink-3)}
.fmenu-panel a.cur{background:var(--surface-2);color:var(--ember);font-weight:600}
@media(max-width:640px){.fnav .pn{display:none}}
@media(max-width:520px){.fnav .fixes{display:none}}
</style>
"""

def wrap_width(html):
    """Aligne la barre sur la largeur de contenu de la page."""
    m = re.search(r"\.wrap\{max-width:(\d+)px", html)
    return m.group(1) + "px" if m else "1040px"

def panel(current):
    rows = ['<div class="grp">Les 21 pièces du dossier</div>']
    for n, t, f, u in PIECES:
        if f == current:
            rows.append(f'<a class="cur" href="#top"><span class="num">{n}</span>{t}</a>')
        elif u:
            rows.append(f'<a href="{u}"><span class="num">{n}</span>{t}</a>')
        else:
            rows.append(f'<span class="off"><span class="num">{n}</span>{t}</span>')

    rows.append('<div class="grp">Références permanentes</div>')
    for path, url, icone, label in (
        (INDEX,     INDEX_URL,     "▤", "Sommaire du dossier"),
        (GLOSSAIRE, GLOSSAIRE_URL, "§", "Glossaire — obligatoire"),
        (SCHEMAS,   SCHEMAS_URL,   "◈", "Atlas des schémas"),
    ):
        if current == path:
            rows.append(f'<a class="cur" href="#top"><span class="num">{icone}</span>{label}</a>')
        elif url:
            rows.append(f'<a href="{url}"><span class="num">{icone}</span>{label}</a>')
        else:
            rows.append(f'<span class="off"><span class="num">{icone}</span>{label}</span>')

    rows.append('<div class="grp">Documents amont — recherche</div>')
    for t, f, u in AMONT:
        cls = ' class="cur"' if f == current else ""
        href = "#top" if f == current else u
        rows.append(f'<a{cls} href="{href}"><span class="num">·</span>{t}</a>')
    return "\n      ".join(rows)


def build(current, nav_w):
    home = f'<a class="home" href="{INDEX_URL}">Dossier La Forge</a><span class="sep">/</span>'
    pn = ""

    if current == INDEX:
        crumb = home + '<span class="here">Sommaire</span>'
    elif current == GLOSSAIRE:
        crumb = home + '<span class="here">Glossaire</span><span class="sep">/</span><span class="kind">obligatoire</span>'
    elif current == SCHEMAS:
        crumb = home + '<span class="here">Atlas des schémas</span><span class="sep">/</span><span class="kind">source unique</span>'
    elif any(f == current for _, _, f, _ in PIECES):
        idx = next(i for i, p in enumerate(PIECES) if p[2] == current)
        n, t, _, _ = PIECES[idx]
        crumb = home + f'<span class="here">{n} — {t}</span>'
        prev_p = PIECES[idx - 1] if idx > 0 else None
        next_p = PIECES[idx + 1] if idx < len(PIECES) - 1 else None
        def side(p, arrow, before):
            if p is None:
                return ""
            label = f"{arrow} {p[0]}" if before else f"{p[0]} {arrow}"
            if p[3]:
                return f'<a href="{p[3]}" title="{p[1]}">{label}</a>'
            return f'<span class="off" title="{p[1]} — pas encore posée">{label}</span>'
        pn = f'<span class="pn">{side(prev_p,"←",True)}{side(next_p,"→",False)}</span>'
    else:
        t = next(t for t, f, _ in AMONT if f == current)
        crumb = home + '<span class="kind">Amont</span><span class="sep">/</span>' + f'<span class="here">{t}</span>'

    style = NAV_CSS.replace("<style id=\"navcss\">",
                            f"<style id=\"navcss\">\n:root{{--nav-w:{nav_w}}}")

    fixes = []
    for path, url, label in (
        (INDEX,     INDEX_URL,     "Sommaire"),
        (GLOSSAIRE, GLOSSAIRE_URL, "Glossaire"),
        (SCHEMAS,   SCHEMAS_URL,   "Schémas"),
    ):
        if current == path:
            continue
        if url:
            fixes.append(f'<a href="{url}">{label}</a>')
        else:
            fixes.append(f'<span class="off">{label}</span>')
    liens = "".join(fixes)

    return f"""<!--NAV-->
{style}
<nav class="fnav" id="top" aria-label="Navigation du dossier">
  <div class="fnav-in">
    {crumb}
    <span class="spacer"></span>
    {pn}
    <span class="fixes">{liens}</span>
    <details class="fmenu">
      <summary>Toutes les pièces ▾</summary>
      <div class="fmenu-panel">
      {panel(current)}
      </div>
    </details>
  </div>
</nav>
<!--/NAV-->"""


def inject(path: pathlib.Path):
    html = path.read_text(encoding="utf-8")
    nav = build(path, wrap_width(html))
    if "<!--NAV-->" in html:
        html = re.sub(r"<!--NAV-->.*?<!--/NAV-->", lambda m: nav, html, flags=re.S)
    else:
        html = re.sub(r"(<header\b)", nav + "\n\n" + r"\1", html, count=1)
    path.write_text(html, encoding="utf-8")
    print(f"nav → {path.relative_to(UP)}")

def targets():
    return [INDEX, GLOSSAIRE, SCHEMAS] + [p[2] for p in PIECES] + [a[1] for a in AMONT]


def main():
    for p in targets():
        if p.exists():
            inject(p)


if __name__ == "__main__":
    main()
