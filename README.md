# DOSSIER Protocol

**Une enveloppe. MODE juge. Sans bornes = classique.**

DOSSIER lie QUELLE + TÉMOIN + EPSILON + HORIZON. Il n'invente pas un canal quantique.
`quantique` only if MODE says so. Existence of a dossier is not a mint.

Place / who / when stay on their own rails (SITUS, FIGURE, HORIZON).
This rail is the envelope. MODE judges.

This repository is version 0. Phone + free. MIT. See [INTERDIT.md](INTERDIT.md).

## Envelope

```
QUELLE + TÉMOIN + EPSILON + HORIZON  →  dossier  →  verdict MODE
```

Sans les quatre : `classique`. That is the honest default.
`quantique` seulement si MODE le dit. A dossier on disk is not a gate.

| Bind | Gate MODE still asks |
|---|---|
| QUELLE | `qrng` \| `qkd` + appareil + not simulated |
| TÉMOIN | `fabricant` \| `di` (`di` requires a transcript) |
| EPSILON | composable ε ∈ (0, 1) **exclusive** |
| HORIZON | suite + calendar day `YYYY-MM-DD` still ahead |

CHSH only via TÉMOIN, and only ≤ Tsirelson. This rail does not mint a channel, a photon, or a Bell.

## Physics locks (this rail)

- **INTERDIT 1.** A dossier existing is not `mode: quantique`.
- **INTERDIT 2.** IBM / QuNetSim / webcam as borne → not quantique.
- **INTERDIT 3.** Σε > plafond → refuse / classique. Never sold as sure. BUDGET : Σε ≤ 10⁻⁶.
- **INTERDIT 4.** Replay QUELLE sha256 → FRAÎCHEUR refuse.
- **INTERDIT 5.** Same Bell transcript on two FIGURE → MONOGAMIE refuse. One transcript, one FIGURE.
- **INTERDIT 6.** No token. No production badge.
- **INTERDIT 7.** ε=0 is a lie. Interval is (0, 1) exclusive (align [epsilon-protocol](https://github.com/carllaliberte/epsilon-protocol)). ε=1 is not a bound.
- **INTERDIT 8.** `simule` true only if a presented card claims it (quelle / temoin / bruit). Do not auto-stamp `simule=true` because mode is classique.
- **INTERDIT 9.** CHSH only via TÉMOIN; ≤ Tsirelson. Do not mint a channel here. MARGE : 2√2−S.
- **INTERDIT 10.** UFHY1 is a suite, not a date. Expired / missing horizon day → not quantique.

Default `classique`. No invented photon or Bell. QUANTUM stays off the JSON card — the card is not a seal.
Judgment = Carl: `python3 dossier.py juger`.

## How to run

```bash
python3 dossier.py lier
python3 dossier.py lier --quelle q.json --temoin t.json --epsilon e.json --horizon h.json
python3 dossier.py lire examples/classique.dossier.json
python3 dossier.py juger examples/classique.dossier.json
python3 dossier.py juger --quelle q.json --temoin t.json --epsilon e.json --horizon h.json
```

Empty `lier` (no rails) → `mode: classique`. If it prints `quantique`, the system is broken.

`juger` judges an existing dossier JSON, or the same `--quelle` / `--temoin` / `--epsilon` / `--horizon` rails. It does not mint a new `dossier_id`. It does not write a new carte unless `--vers` is asked.

Physics locks (stdlib, no extra packages):

```bash
python3 -m unittest discover -s tests -v
```

## Verified vs assumed

Tests lock the rows below. Nothing in this repository is a theorem. Nothing here is a QUANTUM seal.

| Claim | Status |
|---|---|
| empty `lier` / no rails → `classique` | **verified** by tests on this rail |
| existing dossier ≠ `mode: quantique` | **verified** |
| IBM / QuNetSim / webcam as borne → not quantique | **verified** |
| Σε > plafond → classique, not sold as sure | **verified** |
| replay QUELLE sha256 → fraicheur refuse | **verified** |
| same Bell transcript on two FIGURE → monogamie refuse | **verified** |
| no token / production badge on the JSON card | **verified** |
| ε=0 refused; ε=1 refused; interval (0, 1) exclusive | **verified** |
| `simule` only if a presented card claims it | **verified** |
| CHSH only via TÉMOIN; > Tsirelson refused; no minted channel | **verified** |
| UFHY1 as a date refused; expired / missing day → not quantique | **verified** |
| `juger` keeps the existing `dossier_id` and does not write unless asked | **verified** |
| QUANTUM word off the JSON card | **verified** |
| Portmann–Renner meaning of ε | **assumed** (paper, not proven here) |
| QUANTUM signature | **later** — keys off Git, not in this repo |
| EasyCrypt / formal-layer | **not here** |
| invented photon / Bell / quantum channel | **refused** |

## What v0 is not

See [INTERDIT.md](INTERDIT.md). In short:

1. Do not write `mode: quantique` because the dossier exists.
2. Do not paste a Job IBM / QuNetSim / webcam as a borne.
3. Do not sell Σε > plafond as sure.
4. Do not replay a QUELLE sha256.
5. Do not bind one Bell transcript to two FIGURE.
6. No token, no production badge.
7. Do not write `ε=0`. Do not write `ε=1` as a bound.
8. Do not stamp `simule=true` just because the mode is classique.
9. Do not mint a CHSH or a channel on this rail.
10. Do not write UFHY1 as a calendar date. Missing or expired day is not quantique.

The default is `classique`. Refusing that default is the only lie.

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
