#!/usr/bin/env python3
"""Source unique des schémas du dossier.

Un schéma est écrit ICI et nulle part ailleurs. Les pages qui veulent l'afficher
posent un marqueur :

    <!--SCHEMA:arch--><!--/SCHEMA:arch-->

et ce script remplit l'intervalle. Corriger un schéma = corriger ce fichier,
puis relancer build.py : l'atlas ET la pièce suivent.

Le CSS commun des schémas (.dg-*) est injecté une fois par page, entre
<!--DGCSS--> et <!--/DGCSS-->, ou juste avant le premier marqueur de schéma.
"""
import re, pathlib

ROOT = pathlib.Path(__file__).parent      # .../genesis/build  (ce script)
GROOT = ROOT.parent                        # .../genesis        (racine du module)
UP = GROOT  # conservé pour compat

DG_CSS = """<!--DGCSS-->
<style id="dgcss">
.dg{margin:26px 0}
.dg svg{display:block;width:100%;height:auto;color:var(--ink)}
.dg-accent{stroke:var(--ember)}
.dg-accent-t{fill:var(--ember)}
.dg-crit{stroke:var(--crit)}
.dg-crit-t{fill:var(--crit)}
.dg figcaption{font-size:14.5px;color:var(--ink-3);line-height:1.5;margin-top:14px;
  border-left:2px solid var(--rule);padding-left:14px;max-width:70ch}
.dg-scroll{overflow-x:auto}
.dg-scroll>svg{min-width:680px}
</style>
<!--/DGCSS-->"""

# ---------------------------------------------------------------- marqueurs
DEFS = """<defs>
  <marker id="{p}a1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/>
  </marker>
  <marker id="{p}a2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor" opacity="0.55"/>
  </marker>
</defs>"""


# ================================================================ SCHÉMA 1
ARCH = """<figure class="dg dg-scroll">
<svg viewBox="0 0 960 660" role="img" aria-label="L'architecture de la Forge : l'interface parle à l'api ; l'api déclenche l'orchestrateur, qui tourne sur le desktop, et les recettes, qui tournent sur le VPS ; les deux pilotent les mêmes processus d'outils, l'un par le protocole d'agents, l'autre en HTTP direct ; le processus canon sert le domaine Canon, le processus atelier sert sept domaines ; ces deux processus sont les seuls à écrire dans Postgres et dans le stockage objet ; le worker GPU du desktop réclame ses travaux au processus atelier et ne touche jamais la base.">
""" + DEFS.format(p="ar") + """
<g font-family="Bricolage Grotesque, Helvetica Neue, Arial, sans-serif" fill="currentColor">

  <!-- interface -->
  <rect x="40" y="18" width="210" height="46" rx="4" fill="none" stroke="currentColor" stroke-width="1.75"/>
  <text x="145" y="41" text-anchor="middle" font-size="14" font-weight="600">Interface</text>
  <text x="145" y="56" text-anchor="middle" font-size="10" opacity="0.55" font-family="JetBrains Mono, monospace">forme décidée en pièce 18</text>
  <line x1="145" y1="64" x2="145" y2="86" stroke="currentColor" stroke-width="1.5" marker-end="url(#ara1)"/>

  <!-- api -->
  <rect x="40" y="92" width="320" height="54" rx="4" fill="none" stroke="currentColor" stroke-width="1.75"/>
  <text x="200" y="115" text-anchor="middle" font-size="14.5" font-weight="600">api — HTTP + WebSocket</text>
  <text x="200" y="132" text-anchor="middle" font-size="10.5" opacity="0.6">VPS · n'écrit aucune donnée métier</text>

  <line x1="105" y1="146" x2="105" y2="180" stroke="currentColor" stroke-width="1.5" marker-end="url(#ara1)"/>
  <line x1="290" y1="146" x2="290" y2="180" stroke="currentColor" stroke-width="1.5" marker-end="url(#ara1)"/>

  <!-- pilotes -->
  <rect x="40" y="186" width="150" height="72" rx="5" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="115" y="210" text-anchor="middle" font-size="14.5" font-weight="600">orchestrateur</text>
  <text x="115" y="227" text-anchor="middle" font-size="10.5" opacity="0.6">chemin choisi</text>
  <text x="115" y="245" text-anchor="middle" font-size="10" class="dg-accent-t" font-family="JetBrains Mono, monospace">desktop</text>

  <rect x="215" y="186" width="150" height="72" rx="5" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="210" text-anchor="middle" font-size="14.5" font-weight="600">recettes</text>
  <text x="290" y="227" text-anchor="middle" font-size="10.5" opacity="0.6">chemin écrit</text>
  <text x="290" y="245" text-anchor="middle" font-size="10" opacity="0.5" font-family="JetBrains Mono, monospace">VPS</text>

  <line x1="206" y1="216" x2="212" y2="216" stroke="currentColor" stroke-width="1.5" marker-end="url(#ara1)"/>
  <text x="196" y="178" text-anchor="middle" font-size="10" opacity="0.6" font-family="JetBrains Mono, monospace">déclenche</text>

  <!-- bus de l'orchestrateur : pointillés -->
  <polyline points="145,258 145,274 520,274 520,300" fill="none" stroke="currentColor" stroke-width="1.25" stroke-dasharray="4 4" opacity="0.8" marker-end="url(#ara2)"/>
  <polyline points="145,274 160,274 160,300" fill="none" stroke="currentColor" stroke-width="1.25" stroke-dasharray="4 4" opacity="0.8" marker-end="url(#ara2)"/>
  <text x="330" y="269" text-anchor="middle" font-size="10" opacity="0.6" font-family="JetBrains Mono, monospace">protocole d'agents</text>

  <!-- bus des recettes : trait plein -->
  <polyline points="252,258 252,288 592,288 592,300" fill="none" stroke="currentColor" stroke-width="1.4" marker-end="url(#ara1)"/>
  <polyline points="252,288 224,288 224,300" fill="none" stroke="currentColor" stroke-width="1.4" marker-end="url(#ara1)"/>
  <text x="420" y="284" text-anchor="middle" font-size="10" opacity="0.6" font-family="JetBrains Mono, monospace">HTTP direct</text>

  <!-- processus canon -->
  <rect x="40" y="306" width="300" height="196" rx="6" fill="none" class="dg-accent" stroke-width="1.75"/>
  <text x="56" y="327" font-size="12.5" font-weight="600" class="dg-accent-t">processus canon</text>
  <text x="324" y="327" text-anchor="end" font-size="10" opacity="0.5" font-family="JetBrains Mono, monospace">VPS</text>
  <rect x="56" y="338" width="132" height="70" rx="4" fill="none" stroke="currentColor" stroke-width="1.25"/>
  <text x="122" y="366" text-anchor="middle" font-size="12" font-family="JetBrains Mono, monospace">canon</text>
  <text x="122" y="386" text-anchor="middle" font-size="10" opacity="0.6">lecture + écriture</text>
  <rect x="196" y="338" width="128" height="70" rx="4" fill="none" stroke="currentColor" stroke-width="1.25"/>
  <text x="260" y="362" text-anchor="middle" font-size="11" font-family="JetBrains Mono, monospace">canon-lecture</text>
  <text x="260" y="386" text-anchor="middle" font-size="10" opacity="0.6">lecture seule</text>
  <rect x="56" y="420" width="268" height="62" rx="4" fill="none" stroke="currentColor" stroke-width="1.25"/>
  <text x="190" y="446" text-anchor="middle" font-size="13" font-weight="600">Canon</text>
  <text x="190" y="466" text-anchor="middle" font-size="10" opacity="0.6">la mémoire du monde · pièce 03</text>

  <!-- processus atelier -->
  <rect x="376" y="306" width="368" height="196" rx="6" fill="none" class="dg-accent" stroke-width="1.75"/>
  <text x="392" y="327" font-size="12.5" font-weight="600" class="dg-accent-t">processus atelier</text>
  <text x="728" y="327" text-anchor="end" font-size="10" opacity="0.5" font-family="JetBrains Mono, monospace">VPS</text>

  <rect x="392" y="338" width="108" height="70" rx="4" fill="none" stroke="currentColor" stroke-width="1.25"/>
  <text x="446" y="366" text-anchor="middle" font-size="12.5" font-weight="600">File</text>
  <text x="446" y="386" text-anchor="middle" font-size="9.5" opacity="0.6">l'exécution · 04</text>
  <rect x="512" y="338" width="108" height="70" rx="4" fill="none" stroke="currentColor" stroke-width="1.25"/>
  <text x="566" y="366" text-anchor="middle" font-size="12.5" font-weight="600">Catalogue</text>
  <text x="566" y="386" text-anchor="middle" font-size="9.5" opacity="0.6">le disponible · 05</text>
  <rect x="632" y="338" width="108" height="70" rx="4" fill="none" stroke="currentColor" stroke-width="1.25"/>
  <text x="686" y="362" text-anchor="middle" font-size="12" font-weight="600">Biblio-</text>
  <text x="686" y="377" text-anchor="middle" font-size="12" font-weight="600">thèque</text>
  <text x="686" y="394" text-anchor="middle" font-size="9.5" opacity="0.6">les assets · 07</text>

  <rect x="392" y="420" width="79" height="62" rx="4" fill="none" stroke="currentColor" stroke-width="1.25"/>
  <text x="432" y="446" text-anchor="middle" font-size="12" font-weight="600">Récit</text>
  <text x="432" y="465" text-anchor="middle" font-size="9.5" opacity="0.6">pièce 06</text>
  <rect x="481" y="420" width="79" height="62" rx="4" fill="none" stroke="currentColor" stroke-width="1.25"/>
  <text x="521" y="446" text-anchor="middle" font-size="12" font-weight="600">Images</text>
  <text x="521" y="465" text-anchor="middle" font-size="9.5" opacity="0.6">pièce 11</text>
  <rect x="570" y="420" width="79" height="62" rx="4" fill="none" stroke="currentColor" stroke-width="1.25"/>
  <text x="610" y="446" text-anchor="middle" font-size="12" font-weight="600">3D</text>
  <text x="610" y="465" text-anchor="middle" font-size="9.5" opacity="0.6">pièce 12</text>
  <rect x="659" y="420" width="79" height="62" rx="4" fill="none" stroke="currentColor" stroke-width="1.25"/>
  <text x="699" y="446" text-anchor="middle" font-size="12" font-weight="600">Son</text>
  <text x="699" y="465" text-anchor="middle" font-size="9.5" opacity="0.6">pièce 13</text>

  <text x="560" y="497" text-anchor="middle" font-size="9.5" opacity="0.45" font-family="JetBrains Mono, monospace">+ Vidéo, plus tard, sans rien changer d'autre</text>

  <!-- worker -->
  <rect x="784" y="306" width="136" height="196" rx="6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6 4"/>
  <text x="852" y="356" text-anchor="middle" font-size="14" font-weight="600">worker</text>
  <text x="852" y="376" text-anchor="middle" font-size="10.5" opacity="0.6">RTX 4070</text>
  <text x="852" y="393" text-anchor="middle" font-size="10" class="dg-accent-t" font-family="JetBrains Mono, monospace">desktop</text>
  <text x="852" y="414" text-anchor="middle" font-size="10" opacity="0.5">réveillé au besoin</text>
  <text x="852" y="452" text-anchor="middle" font-size="10" opacity="0.5">aucun accès</text>
  <text x="852" y="467" text-anchor="middle" font-size="10" opacity="0.5">à la base</text>

  <line x1="778" y1="352" x2="750" y2="352" stroke="currentColor" stroke-width="1.5" marker-end="url(#ara1)"/>
  <line x1="750" y1="380" x2="778" y2="380" stroke="currentColor" stroke-width="1.5" marker-end="url(#ara1)"/>
  <text x="764" y="341" text-anchor="middle" font-size="9" opacity="0.6" font-family="JetBrains Mono, monospace">réclame</text>
  <text x="764" y="398" text-anchor="middle" font-size="9" opacity="0.6" font-family="JetBrains Mono, monospace">rend</text>

  <!-- écritures -->
  <line x1="190" y1="502" x2="190" y2="554" stroke="currentColor" stroke-width="2.25" marker-end="url(#ara1)"/>
  <text x="200" y="532" font-size="10.5" class="dg-accent-t" font-family="JetBrains Mono, monospace">écrit</text>
  <line x1="470" y1="502" x2="470" y2="554" stroke="currentColor" stroke-width="2.25" marker-end="url(#ara1)"/>
  <text x="480" y="532" font-size="10.5" class="dg-accent-t" font-family="JetBrains Mono, monospace">écrit</text>

  <polyline points="744,440 764,440 764,530 774,530" fill="none" stroke="currentColor" stroke-width="2.25" marker-end="url(#ara1)"/>
  <text x="700" y="524" font-size="10.5" class="dg-accent-t" font-family="JetBrains Mono, monospace">dépose les fichiers</text>

  <!-- postgres -->
  <rect x="40" y="560" width="700" height="70" rx="5" fill="none" stroke="currentColor" stroke-width="1.75"/>
  <text x="60" y="586" font-size="14.5" font-weight="600">postgres</text>
  <text x="200" y="586" font-size="11" opacity="0.65" font-family="JetBrains Mono, monospace">schéma canon</text>
  <text x="340" y="586" font-size="11" opacity="0.65" font-family="JetBrains Mono, monospace">schéma atelier</text>
  <text x="486" y="586" font-size="11" opacity="0.65" font-family="JetBrains Mono, monospace">schéma journal</text>
  <text x="60" y="608" font-size="10.5" opacity="0.5">une seule base · une seule transaction · une seule sauvegarde · les métadonnées seulement</text>

  <!-- stockage objet -->
  <rect x="780" y="560" width="140" height="70" rx="5" fill="none" stroke="currentColor" stroke-width="1.75"/>
  <text x="850" y="584" text-anchor="middle" font-size="13" font-weight="600">stockage objet</text>
  <text x="850" y="601" text-anchor="middle" font-size="10" opacity="0.6">R2 · MinIO</text>
  <text x="850" y="616" text-anchor="middle" font-size="10" opacity="0.6">les binaires</text>

  <!-- retour journal -->
  <polyline points="40,594 22,594 22,119 34,119" fill="none" stroke="currentColor" stroke-width="1.25" stroke-dasharray="4 4" opacity="0.6" marker-end="url(#ara2)"/>
  <text x="26" y="356" font-size="9.5" opacity="0.55" font-family="JetBrains Mono, monospace" transform="rotate(-90 26 356)">lit le journal · diffuse</text>
</g>
</svg>
<figcaption><strong>Les trois flèches épaisses sont le cœur du schéma.</strong> Deux processus seulement écrivent — dans Postgres pour les métadonnées, dans le stockage objet pour les binaires. Les deux pilotes atteignent les mêmes serveurs par deux chemins différents : pointillés pour l'orchestrateur (protocole d'agents), trait plein pour les recettes (HTTP direct) — mêmes outils, mêmes refus. Les huit domaines sont répartis entre les deux processus, dont les sept du processus atelier : les trois du haut sont transversaux, les quatre du bas sont propres à une modalité et empruntent les autres. Le worker est le seul élément qui peut être absent, et il n'a aucun mot de passe de base de données.</figcaption>
</figure>"""


# ================================================================ SCHÉMA 2
FLUX = """<figure class="dg dg-scroll">
<svg viewBox="0 0 960 330" role="img" aria-label="Le flux d'un événement : le fait métier et l'événement sont écrits dans la même transaction ; à la validation, une notification portant le seul identifiant réveille l'api, qui relit la ligne et la diffuse en WebSocket ; la ligne reste en base comme archive.">
""" + DEFS.format(p="fx") + """
<g font-family="Bricolage Grotesque, Helvetica Neue, Arial, sans-serif" fill="currentColor">

  <rect x="36" y="52" width="424" height="152" rx="7" fill="none" class="dg-accent" stroke-width="1.75" stroke-dasharray="7 4"/>
  <text x="52" y="74" font-size="11.5" font-weight="600" class="dg-accent-t" font-family="JetBrains Mono, monospace">UNE SEULE TRANSACTION</text>

  <rect x="54" y="88" width="180" height="98" rx="4" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="144" y="118" text-anchor="middle" font-size="14" font-weight="600">le fait</text>
  <text x="144" y="140" text-anchor="middle" font-size="10.5" opacity="0.6">schéma canon</text>
  <text x="144" y="158" text-anchor="middle" font-size="10.5" opacity="0.6">les contraintes</text>
  <text x="144" y="173" text-anchor="middle" font-size="10.5" opacity="0.6">peuvent refuser ici</text>

  <line x1="234" y1="137" x2="258" y2="137" stroke="currentColor" stroke-width="1.5" marker-end="url(#fxa1)"/>

  <rect x="262" y="88" width="180" height="98" rx="4" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="352" y="118" text-anchor="middle" font-size="14" font-weight="600">l'événement</text>
  <text x="352" y="140" text-anchor="middle" font-size="10.5" opacity="0.6">schéma journal</text>
  <text x="352" y="158" text-anchor="middle" font-size="10.5" opacity="0.6">+ résumé en clair</text>
  <text x="352" y="173" text-anchor="middle" font-size="10.5" opacity="0.6">+ charge utile</text>

  <line x1="460" y1="128" x2="504" y2="128" stroke="currentColor" stroke-width="1.75" marker-end="url(#fxa1)"/>
  <text x="482" y="118" text-anchor="middle" font-size="10" class="dg-accent-t" font-family="JetBrains Mono, monospace">commit</text>

  <rect x="508" y="88" width="150" height="98" rx="4" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="583" y="118" text-anchor="middle" font-size="13.5" font-weight="600">notification</text>
  <text x="583" y="140" text-anchor="middle" font-size="10.5" opacity="0.6">l'identifiant seul</text>
  <text x="583" y="160" text-anchor="middle" font-size="10.5" opacity="0.6">jamais le contenu</text>
  <text x="583" y="176" text-anchor="middle" font-size="9.5" opacity="0.5" font-family="JetBrains Mono, monospace">plafond ≈ 8 Ko</text>

  <line x1="658" y1="128" x2="694" y2="128" stroke="currentColor" stroke-width="1.5" marker-end="url(#fxa1)"/>

  <rect x="698" y="88" width="112" height="98" rx="4" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="754" y="122" text-anchor="middle" font-size="14" font-weight="600">api</text>
  <text x="754" y="144" text-anchor="middle" font-size="10.5" opacity="0.6">relit la ligne</text>
  <text x="754" y="162" text-anchor="middle" font-size="10.5" opacity="0.6">en lecture seule</text>

  <line x1="810" y1="128" x2="840" y2="128" stroke="currentColor" stroke-width="1.5" marker-end="url(#fxa1)"/>

  <rect x="844" y="88" width="100" height="98" rx="4" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="894" y="122" text-anchor="middle" font-size="13.5" font-weight="600">interface</text>
  <text x="894" y="144" text-anchor="middle" font-size="10.5" opacity="0.6">WebSocket</text>
  <text x="894" y="162" text-anchor="middle" font-size="10.5" opacity="0.6">quelques ms</text>

  <!-- archive -->
  <line x1="352" y1="204" x2="352" y2="242" stroke="currentColor" stroke-width="1.25" stroke-dasharray="4 4" opacity="0.7" marker-end="url(#fxa2)"/>
  <rect x="196" y="248" width="312" height="56" rx="4" fill="none" stroke="currentColor" stroke-width="1.25" opacity="0.8"/>
  <text x="352" y="272" text-anchor="middle" font-size="12.5" font-weight="600">la ligne reste</text>
  <text x="352" y="291" text-anchor="middle" font-size="10.5" opacity="0.6">l'archive n'est jamais consommée — d'où le rattrapage</text>

  <!-- rattrapage -->
  <polyline points="508,276 754,276 754,192" fill="none" stroke="currentColor" stroke-width="1.25" stroke-dasharray="4 4" opacity="0.6" marker-end="url(#fxa2)"/>
  <text x="631" y="268" text-anchor="middle" font-size="9.5" opacity="0.55" font-family="JetBrains Mono, monospace">rattrapage à la reconnexion · pièce 17</text>
</g>
</svg>
<figcaption><strong>Le cadre en pointillés est toute la garantie.</strong> Parce que le fait et l'événement sont écrits dans la même parenthèse, il n'existe aucun instant où l'un est vrai sans l'autre : l'interface ne peut pas afficher un événement décrivant une action annulée, et aucun fait ne peut passer sans laisser de trace. La notification ne transporte que l'identifiant, parce que sa charge utile est plafonnée et que le dépassement échoue en silence. Et comme la ligne reste en base au lieu d'être consommée, un client déconnecté peut redemander tout ce qu'il a manqué.</figcaption>
</figure>"""


# ================================================================ SCHÉMA 3
CANON = """<figure class="dg dg-scroll">
<svg viewBox="0 0 960 560" role="img" aria-label="Le modèle du Canon : quatre tables. Une entité porte un identifiant et un type pris dans une liste fermée. Un fait porte sur une entité et a deux périodes, celle du monde et celle de l'écriture, plus un statut candidat ou validé. Une relation lie deux entités et porte aussi une validité. Une croyance lie un porteur — un personnage ou le lecteur — à un fait, avec un statut et sa propre validité.">
""" + DEFS.format(p="cn") + """
<g font-family="Bricolage Grotesque, Helvetica Neue, Arial, sans-serif" fill="currentColor">

  <!-- relation : lien par le haut -->
  <polyline points="160,72 160,32 810,32 810,72" fill="none" stroke="currentColor" stroke-width="1.4" marker-end="url(#cna1)"/>
  <text x="485" y="26" text-anchor="middle" font-size="10.5" opacity="0.65" font-family="JetBrains Mono, monospace">source et cible</text>

  <!-- ENTITÉ -->
  <rect x="40" y="72" width="240" height="186" rx="6" fill="none" class="dg-accent" stroke-width="1.75"/>
  <text x="56" y="98" font-size="14" font-weight="600" class="dg-accent-t">ENTITÉ</text>
  <text x="264" y="98" text-anchor="end" font-size="9.5" opacity="0.5" font-family="JetBrains Mono, monospace">ce qui existe</text>
  <line x1="56" y1="108" x2="264" y2="108" stroke="currentColor" stroke-width="0.75" opacity="0.3"/>
  <text x="56" y="130" font-size="11.5" font-family="JetBrains Mono, monospace">identifiant</text>
  <text x="56" y="152" font-size="11.5" font-family="JetBrains Mono, monospace">type</text>
  <text x="130" y="152" font-size="10" opacity="0.55">liste fermée</text>
  <text x="56" y="174" font-size="11.5" font-family="JetBrains Mono, monospace">nom</text>
  <text x="56" y="196" font-size="11.5" font-family="JetBrains Mono, monospace">autres noms</text>
  <text x="56" y="222" font-size="10" opacity="0.55">aucun champ libre :</text>
  <text x="56" y="238" font-size="10" opacity="0.55">tout le reste est un fait</text>

  <!-- FAIT -->
  <rect x="360" y="72" width="280" height="228" rx="6" fill="none" class="dg-accent" stroke-width="1.75"/>
  <text x="376" y="98" font-size="14" font-weight="600" class="dg-accent-t">FAIT</text>
  <text x="624" y="98" text-anchor="end" font-size="9.5" opacity="0.5" font-family="JetBrains Mono, monospace">ce qui est vrai</text>
  <line x1="376" y1="108" x2="624" y2="108" stroke="currentColor" stroke-width="0.75" opacity="0.3"/>
  <text x="376" y="130" font-size="11.5" font-family="JetBrains Mono, monospace">sujet</text>
  <text x="450" y="130" font-size="10" opacity="0.55">une entité</text>
  <text x="376" y="152" font-size="11.5" font-family="JetBrains Mono, monospace">attribut · valeur</text>
  <text x="376" y="180" font-size="11.5" font-family="JetBrains Mono, monospace" class="dg-accent-t">validité</text>
  <text x="470" y="180" font-size="10" opacity="0.55">temps du monde</text>
  <text x="376" y="202" font-size="11.5" font-family="JetBrains Mono, monospace" class="dg-accent-t">écrit le</text>
  <text x="470" y="202" font-size="10" opacity="0.55">temps d'écriture</text>
  <text x="376" y="230" font-size="11.5" font-family="JetBrains Mono, monospace">statut</text>
  <text x="450" y="230" font-size="10" opacity="0.55">candidat ou validé</text>
  <text x="376" y="252" font-size="11.5" font-family="JetBrains Mono, monospace">provenance</text>
  <text x="376" y="280" font-size="10" opacity="0.55">jamais écrasé — on ferme sa validité</text>

  <line x1="286" y1="130" x2="354" y2="130" stroke="currentColor" stroke-width="1.5" marker-end="url(#cna1)"/>
  <text x="320" y="122" text-anchor="middle" font-size="10" opacity="0.65" font-family="JetBrains Mono, monospace">sujet</text>

  <!-- RELATION -->
  <rect x="700" y="72" width="220" height="186" rx="6" fill="none" class="dg-accent" stroke-width="1.75"/>
  <text x="716" y="98" font-size="14" font-weight="600" class="dg-accent-t">RELATION</text>
  <line x1="716" y1="108" x2="904" y2="108" stroke="currentColor" stroke-width="0.75" opacity="0.3"/>
  <text x="716" y="130" font-size="11.5" font-family="JetBrains Mono, monospace">source · cible</text>
  <text x="716" y="152" font-size="11.5" font-family="JetBrains Mono, monospace">type</text>
  <text x="716" y="180" font-size="11.5" font-family="JetBrains Mono, monospace" class="dg-accent-t">validité</text>
  <text x="716" y="208" font-size="10" opacity="0.55">une alliance a un début</text>
  <text x="716" y="224" font-size="10" opacity="0.55">et souvent une fin</text>

  <!-- CROYANCE -->
  <line x1="500" y1="300" x2="500" y2="356" stroke="currentColor" stroke-width="1.5" marker-end="url(#cna1)"/>
  <text x="510" y="332" font-size="10" opacity="0.65" font-family="JetBrains Mono, monospace">porte sur</text>

  <polyline points="160,258 160,420 354,420" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#cna1)"/>
  <text x="170" y="412" font-size="10" opacity="0.65" font-family="JetBrains Mono, monospace">porteur</text>

  <rect x="360" y="360" width="280" height="164" rx="6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6 4"/>
  <text x="376" y="386" font-size="14" font-weight="600">CROYANCE</text>
  <text x="624" y="386" text-anchor="end" font-size="9.5" opacity="0.5" font-family="JetBrains Mono, monospace">facultatif</text>
  <line x1="376" y1="396" x2="624" y2="396" stroke="currentColor" stroke-width="0.75" opacity="0.3"/>
  <text x="376" y="418" font-size="11.5" font-family="JetBrains Mono, monospace">porteur · fait</text>
  <text x="376" y="440" font-size="11.5" font-family="JetBrains Mono, monospace">statut</text>
  <text x="376" y="460" font-size="10" opacity="0.55">sait · ignore · croit faux · soupçonne</text>
  <text x="376" y="484" font-size="11.5" font-family="JetBrains Mono, monospace" class="dg-accent-t">validité</text>
  <text x="470" y="484" font-size="10" opacity="0.55">on apprend à une date</text>
  <text x="376" y="510" font-size="10" opacity="0.55">n'existe que sur les faits marqués sensibles</text>

  <rect x="700" y="360" width="220" height="164" rx="6" fill="none" stroke="currentColor" stroke-width="1.25" opacity="0.75"/>
  <text x="716" y="386" font-size="12.5" font-weight="600">Le lecteur</text>
  <line x1="716" y1="396" x2="904" y2="396" stroke="currentColor" stroke-width="0.75" opacity="0.3"/>
  <text x="716" y="418" font-size="11" opacity="0.7">est un porteur comme</text>
  <text x="716" y="434" font-size="11" opacity="0.7">un autre — sauf que sa</text>
  <text x="716" y="450" font-size="11" opacity="0.7">validité se compte en</text>
  <text x="716" y="466" font-size="11" opacity="0.7">chapitres, pas en années</text>
  <text x="716" y="494" font-size="10" opacity="0.5">d'où : pas de troisième</text>
  <text x="716" y="510" font-size="10" opacity="0.5">axe temporel à construire</text>

  <line x1="694" y1="442" x2="646" y2="442" stroke="currentColor" stroke-width="1.25" stroke-dasharray="4 4" opacity="0.7" marker-end="url(#cna2)"/>
</g>
</svg>
<figcaption><strong>Quatre tables, et une seule est facultative.</strong> Une entité ne porte que son identité — tout ce qui pourrait changer est un <em>fait</em>, ce qui est la raison pour laquelle il n'y a aucun champ libre sur l'entité. Un fait porte deux temps : celui du monde et celui de l'écriture. Une relation est datée elle aussi, parce qu'une alliance commence et finit. La croyance, en pointillés, n'existe que sur les faits que tu marques comme sensibles — et le lecteur y entre comme un porteur de plus, ce qui évite d'inventer un troisième axe de temps.</figcaption>
</figure>"""


# ================================================================ SCHÉMA 4
TEMPS = """<figure class="dg dg-scroll">
<svg viewBox="0 0 960 330" role="img" aria-label="Les deux axes de temps : sur l'axe du monde, une première version dit que Kael vit à la capitale de l'an 3 à toujours, une seconde version la remplace en la limitant à l'an 12 ; sur l'axe d'écriture, la première a été écrite le 2 mars et la seconde le 14 mai, et la première n'est pas effacée.">
""" + DEFS.format(p="tp") + """
<g font-family="Bricolage Grotesque, Helvetica Neue, Arial, sans-serif" fill="currentColor">

  <text x="40" y="34" font-size="12.5" font-weight="600" class="dg-accent-t">TEMPS DU MONDE — quand c'est vrai dans ton univers</text>

  <line x1="40" y1="60" x2="920" y2="60" stroke="currentColor" stroke-width="1" opacity="0.35"/>
  <text x="150" y="52" text-anchor="middle" font-size="10" opacity="0.55" font-family="JetBrains Mono, monospace">an 3</text>
  <text x="520" y="52" text-anchor="middle" font-size="10" opacity="0.55" font-family="JetBrains Mono, monospace">an 12</text>
  <line x1="150" y1="54" x2="150" y2="66" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <line x1="520" y1="54" x2="520" y2="66" stroke="currentColor" stroke-width="1" opacity="0.4"/>

  <rect x="150" y="78" width="770" height="34" rx="4" fill="none" stroke="currentColor" stroke-width="1.25" stroke-dasharray="5 4" opacity="0.55"/>
  <text x="164" y="100" font-size="11.5" opacity="0.55">Kael vit à la capitale · an 3 → toujours</text>
  <text x="906" y="100" text-anchor="end" font-size="10" opacity="0.45" font-family="JetBrains Mono, monospace">version close</text>

  <rect x="150" y="124" width="370" height="34" rx="4" fill="none" class="dg-accent" stroke-width="1.75"/>
  <text x="164" y="146" font-size="11.5" font-weight="600">Kael vit à la capitale · an 3 → an 12</text>
  <text x="506" y="146" text-anchor="end" font-size="10" class="dg-accent-t" font-family="JetBrains Mono, monospace">en vigueur</text>

  <text x="40" y="210" font-size="12.5" font-weight="600" class="dg-accent-t">TEMPS D'ÉCRITURE — quand tu l'as su</text>

  <line x1="40" y1="240" x2="920" y2="240" stroke="currentColor" stroke-width="1" opacity="0.35"/>
  <circle cx="300" cy="240" r="5" fill="currentColor"/>
  <circle cx="660" cy="240" r="5" fill="currentColor"/>
  <line x1="300" y1="240" x2="300" y2="112" stroke="currentColor" stroke-width="1" stroke-dasharray="3 4" opacity="0.4"/>
  <line x1="660" y1="240" x2="660" y2="158" stroke="currentColor" stroke-width="1" stroke-dasharray="3 4" opacity="0.4"/>
  <text x="300" y="264" text-anchor="middle" font-size="11" font-weight="600">2 mars</text>
  <text x="300" y="282" text-anchor="middle" font-size="10.5" opacity="0.6">le fait est écrit</text>
  <text x="660" y="264" text-anchor="middle" font-size="11" font-weight="600">14 mai</text>
  <text x="660" y="282" text-anchor="middle" font-size="10.5" opacity="0.6">on ferme sa validité</text>
  <text x="660" y="300" text-anchor="middle" font-size="10.5" opacity="0.6">on n'efface rien</text>
</g>
</svg>
<figcaption><strong>La ligne du haut n'est pas supprimée, elle est close.</strong> C'est toute la différence entre « le monde a changé » et « je me suis trompé » : les deux axes permettent de distinguer <em>Kael a quitté la capitale en l'an 12</em> de <em>je croyais qu'il y était resté et j'ai appris le contraire le 14 mai</em>. Sans le second axe, un flashback écrit après coup devient impossible à dater ; sans le premier, on perd la capacité d'interroger le monde à une date donnée.</figcaption>
</figure>"""


# ================================================================ SCHÉMA 5
PROMOTION = """<figure class="dg dg-scroll">
<svg viewBox="0 0 960 420" role="img" aria-label="Le chemin d'un fait : un agent propose, le fait entre comme candidat après un contrôle d'intégrité, l'audit le relit par plusieurs relecteurs séparés, puis il est promu en validé — c'est seulement à ce moment que les règles du monde s'appliquent — ou rejeté ; dans les deux cas le rapport de session en garde la trace.">
""" + DEFS.format(p="pm") + """
<g font-family="Bricolage Grotesque, Helvetica Neue, Arial, sans-serif" fill="currentColor">

  <rect x="34" y="120" width="140" height="76" rx="5" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="104" y="150" text-anchor="middle" font-size="13.5" font-weight="600">un agent</text>
  <text x="104" y="170" text-anchor="middle" font-size="11" opacity="0.6">propose</text>
  <text x="104" y="186" text-anchor="middle" font-size="10" opacity="0.5">librement</text>

  <line x1="174" y1="158" x2="222" y2="158" stroke="currentColor" stroke-width="1.5" marker-end="url(#pma1)"/>
  <text x="198" y="118" text-anchor="middle" font-size="10" class="dg-crit-t" font-family="JetBrains Mono, monospace">étage 1</text>
  <text x="198" y="132" text-anchor="middle" font-size="9.5" class="dg-crit-t" font-family="JetBrains Mono, monospace">intégrité</text>
  <line x1="198" y1="140" x2="198" y2="150" class="dg-crit" stroke-width="1.5"/>

  <rect x="226" y="120" width="150" height="76" rx="5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6 4"/>
  <text x="301" y="150" text-anchor="middle" font-size="13.5" font-weight="600">candidat</text>
  <text x="301" y="170" text-anchor="middle" font-size="10.5" opacity="0.6">dans le canon,</text>
  <text x="301" y="186" text-anchor="middle" font-size="10.5" opacity="0.6">pas encore vrai</text>

  <line x1="376" y1="158" x2="416" y2="158" stroke="currentColor" stroke-width="1.5" marker-end="url(#pma1)"/>

  <rect x="420" y="106" width="180" height="104" rx="5" fill="none" class="dg-accent" stroke-width="1.75"/>
  <text x="510" y="134" text-anchor="middle" font-size="13.5" font-weight="600">l'audit</text>
  <text x="510" y="154" text-anchor="middle" font-size="10.5" opacity="0.6">cohérence · canon</text>
  <text x="510" y="170" text-anchor="middle" font-size="10.5" opacity="0.6">style · technique</text>
  <text x="510" y="192" text-anchor="middle" font-size="10" class="dg-accent-t" font-family="JetBrains Mono, monospace">jamais le producteur</text>

  <polyline points="600,140 656,140 656,96" fill="none" stroke="currentColor" stroke-width="1.75" marker-end="url(#pma1)"/>
  <polyline points="600,176 656,176 656,252" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#pma1)"/>

  <text x="700" y="46" font-size="10" class="dg-crit-t" font-family="JetBrains Mono, monospace">étage 2 — les règles de ton monde</text>
  <text x="700" y="60" font-size="9.5" opacity="0.55" font-family="JetBrains Mono, monospace">sévérité réglable · refus ou signalement</text>
  <line x1="694" y1="68" x2="694" y2="82" class="dg-crit" stroke-width="1.5"/>

  <rect x="672" y="88" width="248" height="76" rx="5" fill="none" class="dg-accent" stroke-width="1.75"/>
  <text x="796" y="118" text-anchor="middle" font-size="13.5" font-weight="600">validé</text>
  <text x="796" y="138" text-anchor="middle" font-size="10.5" opacity="0.6">c'est vrai de ton monde</text>
  <text x="796" y="154" text-anchor="middle" font-size="10" opacity="0.5">plus jamais écrasé</text>

  <rect x="672" y="244" width="248" height="76" rx="5" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="796" y="274" text-anchor="middle" font-size="13.5" font-weight="600">rejeté</text>
  <text x="796" y="294" text-anchor="middle" font-size="10.5" opacity="0.6">conservé, avec son motif</text>
  <text x="796" y="310" text-anchor="middle" font-size="10" opacity="0.5">un rejet est une information</text>

  <polyline points="510,210 510,300 656,300" fill="none" stroke="currentColor" stroke-width="1.25" stroke-dasharray="4 4" opacity="0.7"/>
  <rect x="286" y="300" width="224" height="72" rx="5" fill="none" stroke="currentColor" stroke-width="1.25" opacity="0.85"/>
  <text x="398" y="328" text-anchor="middle" font-size="12.5" font-weight="600">rapport de session</text>
  <text x="398" y="348" text-anchor="middle" font-size="10.5" opacity="0.6">étage 3 — ce qui est signalé</text>
  <text x="398" y="364" text-anchor="middle" font-size="10.5" opacity="0.6">et attend ton arbitrage</text>
  <line x1="510" y1="300" x2="512" y2="300" stroke="currentColor" stroke-width="1.25"/>
</g>
</svg>
<figcaption><strong>Les règles de ton monde ne s'appliquent qu'à la promotion, jamais à la proposition.</strong> C'est ce qui permet à un agent d'écrire vite sans salir le canon : il propose librement, seul le contrôle d'intégrité l'arrête à l'entrée. Le reste — les incohérences de monde — se découvre à l'audit et remonte dans ton rapport de session, où tu tranches. Un fait rejeté est conservé avec son motif : savoir qu'une piste a été écartée, et pourquoi, vaut mieux que de la retrouver six mois plus tard sans le contexte.</figcaption>
</figure>"""


SCHEMAS = {
    "arch": ARCH,
    "flux": FLUX,
    "canon": CANON,
    "temps": TEMPS,
    "promotion": PROMOTION,
}

# Où chaque schéma doit apparaître, en plus de l'atlas (pour le contrôle).
ATTENDU = {
    "arch": ["02-architecture.html", "schemas.html"],
    "flux": ["02-architecture.html", "schemas.html"],
    "canon": ["03-canon.html", "schemas.html"],
    "temps": ["03-canon.html", "schemas.html"],
    "promotion": ["03-canon.html", "schemas.html"],
}


def inject(path: pathlib.Path) -> list:
    html = path.read_text(encoding="utf-8")
    orig = html
    poses = []
    for name, svg in SCHEMAS.items():
        marker = f"<!--SCHEMA:{name}-->"
        end = f"<!--/SCHEMA:{name}-->"
        if marker not in html:
            continue
        html = re.sub(
            re.escape(marker) + r".*?" + re.escape(end),
            lambda m: marker + "\n" + svg + "\n" + end,
            html, flags=re.S)
        poses.append(name)
    if poses and "<!--DGCSS-->" not in html:
        first = min(html.index(f"<!--SCHEMA:{n}-->") for n in poses)
        html = html[:first] + DG_CSS + "\n\n" + html[first:]
    elif poses:
        html = re.sub(r"<!--DGCSS-->.*?<!--/DGCSS-->", lambda m: DG_CSS, html, flags=re.S)
    if html != orig:
        path.write_text(html, encoding="utf-8")
    return poses


def main():
    touched = {}
    fichiers = sorted(
        list(GROOT.glob("*.html"))
        + list((GROOT / "pieces").glob("*.html"))
        + list((GROOT / "amont").glob("*.html"))
    )
    for p in fichiers:
        got = inject(p)
        if got:
            touched[p.name] = got
            print(f"schémas → {p.name} : {', '.join(got)}")

    # contrôle : chaque schéma est-il là où on l'attend ?
    manque = []
    for name, fichiers in ATTENDU.items():
        for f in fichiers:
            if name not in touched.get(f, []):
                manque.append(f"{name} absent de {f}")
    if manque:
        print("\n  ATTENTION — marqueur manquant :")
        for m in manque:
            print(f"    · {m}")
    return manque


if __name__ == "__main__":
    main()
