# La Forge

Système global, restructuré en 8 modules. Chaque module est un sous-dossier ;
tous n'ont pas encore de contenu.

| Module       | Couvre |
|--------------|--------|
| `genesis/`   | Création d'univers, mondes, histoires, lore, personnages — ex-« La Forge », le dossier de conception en 21 pièces |
| `anvil/`     | Développement, code, applications, services |
| `foundry/`   | IA/ML, entraînement, modèles, LoRA, datasets |
| `conductor/` | Orchestration, interactions, workflows, communication |
| `command/`   | Gestion de projets, tâches, roadmaps, ressources |
| `codex/`     | Documentation, connaissances, specs, références |
| `lens/`      | UI/UX, visualisation, dashboards |
| `toolbox/`   | Outils, agents, utilitaires, centralisation |

## genesis/ — seul module avec du contenu pour l'instant

```
genesis/
├── index.html          sommaire du dossier
├── glossaire.html      glossaire — obligatoire
├── schemas.html         atlas des schémas
├── pieces/              les pièces numérotées (5 posées sur 21)
│   ├── 00-principes.html
│   ├── 01-stack.html
│   ├── 02-architecture.html
│   ├── 03-canon.html
│   └── 04-file.html
├── amont/                documents de recherche préalables
│   ├── forge.html         dossier de recherche
│   ├── bc.html             écrire ou déléguer
│   ├── plan.html           le plan de la Forge
│   └── budget.html         le budget de contexte
├── outils/                scripts de calcul (budget de contexte, poids des outils)
│   ├── budget.py
│   ├── count.py
│   ├── count2.py
│   └── tools_naive.py
└── build/                  système de build/publication
    ├── build.py             point d'entrée : injecte schémas + nav, rapporte ce qui est à republier
    ├── build_nav.py         génère la barre de navigation
    ├── build_schemas.py     source unique des schémas (SVG), injectés par marqueur
    └── publie.json           registre des empreintes de publication (généré par build.py)
```

### Utilisation

```
cd genesis/build
python3 build.py                    # injecte schémas + nav, liste ce qui est à republier
python3 build.py publie 00-principes.html 01-stack.html   # après une vraie publication
```

Aucune dépendance externe — stdlib Python uniquement.
