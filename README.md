# DOSSIER Protocol

**Une enveloppe. MODE juge. Sans bornes = classique.**

DOSSIER lie QUELLE + TÉMOIN + EPSILON + HORIZON. Il n'invente pas un canal quantique.
`quantique` seulement si MODE le dit. L'existence d'un dossier n'est pas une frappe.

Où / qui / quand restent sur leurs rails (SITUS, FIGURE, HORIZON).
Cette rail est l'enveloppe. MODE juge.

Ce dépôt est la version 0. Téléphone + libre. MIT. Voir [INTERDIT.md](INTERDIT.md).

## Enveloppe

```
QUELLE + TÉMOIN + EPSILON + HORIZON  →  dossier  →  verdict MODE
```

Sans les quatre : `classique`. C'est le défaut honnête.
`quantique` seulement si MODE le dit. Un dossier sur disque n'est pas une porte.

| Lien | Porte que MODE exige encore |
|---|---|
| QUELLE | `qrng` \| `qkd` + appareil + pas simulé |
| TÉMOIN | `fabricant` \| `di` (`di` exige un transcript) |
| EPSILON | composable ε ∈ (0, 1) **exclusif** |
| HORIZON | suite + jour calendaire `YYYY-MM-DD` encore devant |

CHSH seulement via TÉMOIN, et seulement ≤ Tsirelson. Cette rail n'invente pas un canal, un photon, ni un Bell.

## Verrous physiques (cette rail)

- **INTERDIT 1.** Un dossier existant n'est pas `mode: quantique`.
- **INTERDIT 2.** IBM / QuNetSim / webcam comme borne → pas quantique.
- **INTERDIT 3.** Σε > plafond → refuse / classique. Jamais vendue comme sûre. BUDGET : Σε ≤ 10⁻⁶.
- **INTERDIT 4.** Rejouer une empreinte QUELLE sha256 → FRAÎCHEUR refuse.
- **INTERDIT 5.** Même transcript Bell sur deux FIGURE → MONOGAMIE refuse. Un transcript, une FIGURE.
- **INTERDIT 6.** Pas de token. Pas de badge production.
- **INTERDIT 7.** ε=0 est un mensonge. Intervalle (0, 1) exclusif (aligné [epsilon-protocol](https://github.com/carllaliberte/epsilon-protocol)). ε=1 n'est pas une borne.
- **INTERDIT 8.** `simule` true seulement si une carte présentée le dit (quelle / temoin / bruit). Ne pas estampiller `simule=true` parce que le mode est classique.
- **INTERDIT 9.** CHSH seulement via TÉMOIN ; ≤ Tsirelson. Ne pas inventer un canal ici. MARGE : 2√2−S.
- **INTERDIT 10.** UFHY1 est une suite, pas une date. Jour d'horizon passé ou absent → pas quantique.

Défaut `classique`. Pas de photon ni de Bell inventé. QUANTUM reste hors de la carte JSON — la carte n'est pas un sceau.
Judgment = Carl : `python3 dossier.py juger`.

## Comment lancer

```bash
python3 dossier.py lier
python3 dossier.py lier --quelle q.json --temoin t.json --epsilon e.json --horizon h.json
python3 dossier.py lire examples/classique.dossier.json
python3 dossier.py juger examples/classique.dossier.json
python3 dossier.py juger --quelle q.json --temoin t.json --epsilon e.json --horizon h.json
```

`lier` vide (sans rails) → `mode: classique`. S'il imprime `quantique`, le système est cassé.

`juger` juge un JSON dossier existant, ou les mêmes rails `--quelle` / `--temoin` / `--epsilon` / `--horizon`. Il ne frappe pas un nouveau `dossier_id`. Il n'écrit pas une nouvelle carte sauf si `--vers` est demandé.

Verrous physiques (stdlib, sans paquets en plus) :

```bash
python3 -m unittest discover -s tests -v
```

## Vérifié vs assumé

Les tests verrouillent les lignes ci-dessous. Rien dans ce dépôt n'est un théorème. Rien ici n'est un sceau QUANTUM.

| Affirmation | Statut |
|---|---|
| `lier` vide / sans rails → `classique` | **vérifié** par les tests de cette rail |
| dossier existant ≠ `mode: quantique` | **vérifié** |
| IBM / QuNetSim / webcam comme borne → pas quantique | **vérifié** |
| Σε > plafond → classique, pas vendue comme sûre | **vérifié** |
| rejouer QUELLE sha256 → fraicheur refuse | **vérifié** |
| même transcript Bell sur deux FIGURE → monogamie refuse | **vérifié** |
| pas de token / badge production sur la carte JSON | **vérifié** |
| ε=0 refusé ; ε=1 refusé ; intervalle (0, 1) exclusif | **vérifié** |
| `simule` seulement si une carte présentée le dit | **vérifié** |
| CHSH seulement via TÉMOIN ; > Tsirelson refusé ; pas de canal inventé | **vérifié** |
| UFHY1 comme date refusée ; jour passé ou absent → pas quantique | **vérifié** |
| `juger` garde le `dossier_id` existant et n'écrit que si demandé | **vérifié** |
| mot QUANTUM hors de la carte JSON | **vérifié** |
| sens Portmann–Renner de ε | **assumé** (papier, pas prouvé ici) |
| signature QUANTUM | **plus tard** — clés hors Git, pas dans ce dépôt |
| EasyCrypt / couche formelle | **pas ici** |
| photon / Bell / canal quantique inventé | **refusé** |

## Ce que v0 n'est pas

Voir [INTERDIT.md](INTERDIT.md). En bref :

1. Ne pas écrire `mode: quantique` parce que le dossier existe.
2. Ne pas coller un Job IBM / QuNetSim / webcam comme borne.
3. Ne pas vendre Σε > plafond comme sûre.
4. Ne pas rejouer une empreinte QUELLE sha256.
5. Ne pas lier un transcript Bell à deux FIGURE.
6. Pas de token, pas de badge production.
7. Ne pas écrire `ε=0`. Ne pas écrire `ε=1` comme borne.
8. Ne pas estampiller `simule=true` juste parce que le mode est classique.
9. Ne pas inventer un CHSH ni un canal sur cette rail.
10. Ne pas écrire UFHY1 comme date de calendrier. Jour absent ou passé n'est pas quantique.

Le défaut est `classique`. Refuser ce défaut est le seul mensonge.

## Famille

| Rail | Question |
|---|---|
| [FIGURE](https://github.com/carllaliberte/figure-protocol) | qui |
| [SITUS](https://github.com/carllaliberte/situs-protocol) | où |
| [UNFORGE](https://github.com/carllaliberte/unforge-check) | quoi |
| [QUELLE](https://github.com/carllaliberte/quelle) | d'où le bit |
| [TÉMOIN](https://github.com/carllaliberte/temoin-protocol) | avec quelle force |
| [BRUIT](https://github.com/carllaliberte/bruit-protocol) | ce que le score a vu |
| [HORIZON](https://github.com/carllaliberte/horizon-protocol) | jusqu'à quand le sceau tient |
| [EPSILON](https://github.com/carllaliberte/epsilon-protocol) | avec quel ε |
| [MODE](https://github.com/carllaliberte/mode-protocol) | le collapse des quatre |
| [DOSSIER](https://github.com/carllaliberte/dossier-protocol) | l'enveloppe des quatre |

MIT (protocoles) · Apache-2.0 (œil UNFORGE). QUANTUM signe **plus tard**. Les clés restent hors Git. Ce dépôt n'est pas un sceau QUANTUM.

## Fichiers

- [`INTERDIT.md`](INTERDIT.md) — ce qu'on ne prétend pas
- [`JUGE.md`](JUGE.md) — cette rail nomme le dossier, MODE juge
- [`schema/dossier.v0.json`](schema/dossier.v0.json)
- [`dossier.py`](dossier.py) — `python3 dossier.py lier` / `lire` / `juger`
- [`examples/classique.dossier.json`](examples/classique.dossier.json) — téléphone sans dongle
- [`tests/test_physics_locks.py`](tests/test_physics_locks.py) — verrous physiques
- [`.github/workflows/physics.yml`](.github/workflows/physics.yml) — CI des tests
