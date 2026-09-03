#!/usr/bin/env python3
"""DOSSIER v0 — enveloppe. MODE juge. Pas de canal quantique."""

from __future__ import annotations

import argparse
import json
import math
import sys
import uuid
from datetime import date, datetime, timezone
from pathlib import Path

FORMAT = "dossier.v0"
TSIRELSON = 2 * math.sqrt(2)
PLAFOND = 1e-6
FAUX_BORNES = ("ibm", "qunetsim", "webcam")
SUITES = ("UFHY1", "mldsa87", "ed25519")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load(chemin: str | None):
    if not chemin:
        return None
    p = Path(chemin).expanduser()
    if not p.is_file():
        raise SystemExit("introuvable : " + str(p))
    return json.loads(p.read_text(encoding="utf-8"))


def _reg(chemin: Path) -> dict:
    if chemin.is_file():
        return json.loads(chemin.read_text(encoding="utf-8"))
    return {}


def fraicheur(quelle, registre):
    if quelle is None or registre is None:
        return []
    sha = quelle.get("sha256")
    if not sha:
        return ["quelle: pas de sha256"]
    if sha in (_reg(registre).get("sha256") or []):
        return ["fraicheur: empreinte déjà vue"]
    return []


def noter_vue(quelle, registre):
    if quelle is None or registre is None:
        return
    sha = quelle.get("sha256")
    if not sha:
        return
    mem = _reg(registre)
    vues = list(mem.get("sha256") or [])
    if sha not in vues:
        vues.append(sha)
    mem["sha256"] = vues
    registre.write_text(json.dumps(mem, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def monogamie(temoin, figure, registre, noter=False):
    if temoin is None:
        return []
    tr = temoin.get("transcript_sha256")
    if not tr or registre is None:
        return []
    fid = (figure or {}).get("figure_id") or temoin.get("figure_id")
    mem = _reg(registre)
    liens = mem.get("transcript") or {}
    deja = liens.get(tr)
    if deja and fid and deja != fid:
        return ["monogamie: transcript déjà lié à " + deja]
    if noter and fid:
        liens[tr] = fid
        mem["transcript"] = liens
        registre.write_text(json.dumps(mem, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return []


def budget(epsilon, extra, plafond):
    termes = list(extra or [])
    if epsilon and epsilon.get("epsilon") is not None:
        termes.append(float(epsilon["epsilon"]))
    if epsilon and epsilon.get("termes"):
        termes.extend(float(x) for x in epsilon["termes"])
    if not termes:
        return None, []
    s = sum(termes)
    if s > plafond:
        return s, ["budget: somme ε=%.3g > plafond=%.3g" % (s, plafond)]
    return s, []


def marge(temoin):
    if not temoin or temoin.get("chsh") is None:
        return None
    return TSIRELSON - float(temoin["chsh"])


def _simule_presente(quelle, temoin, bruit) -> bool:
    return any(c is not None and c.get("simule") is True for c in (quelle, temoin, bruit))


def _faux_bornes(*cartes) -> list[str]:
    vues = []
    raisons = []
    for c in cartes:
        if not isinstance(c, dict):
            continue
        blob = json.dumps(c, ensure_ascii=False).lower()
        for nom in FAUX_BORNES:
            if nom in blob and nom not in vues:
                vues.append(nom)
                raisons.append("borne " + nom + " : pas quantique")
    return raisons


def _mode_raisons(quelle, temoin, epsilon, horizon, bruit):
    r = []
    if quelle is None:
        r.append("quelle absente")
    else:
        if quelle.get("source") not in ("qrng", "qkd"):
            r.append("quelle: source ≠ qrng|qkd")
        if not quelle.get("appareil"):
            r.append("quelle: pas d'appareil")
        if quelle.get("simule") is True:
            r.append("quelle: simule")
    if temoin is None:
        r.append("temoin absent")
    else:
        niv = temoin.get("niveau")
        if niv not in ("fabricant", "di"):
            r.append("temoin: niveau ≠ fabricant|di")
        if niv == "di":
            if temoin.get("simule") is True:
                r.append("temoin: di + simule")
            if not temoin.get("transcript_sha256"):
                r.append("temoin: di sans transcript")
            chsh = temoin.get("chsh")
            if chsh is not None:
                x = float(chsh)
                if x <= 2:
                    r.append("temoin: CHSH ≤ 2")
                if x > TSIRELSON + 1e-9:
                    r.append("temoin: CHSH > 2√2")
    if epsilon is None:
        r.append("epsilon absent")
    else:
        if epsilon.get("modele") in (None, "none"):
            r.append("epsilon: modele none")
        if "epsilon" not in epsilon or epsilon.get("epsilon") is None:
            r.append("epsilon: ε absent")
        else:
            eps = epsilon.get("epsilon")
            if not isinstance(eps, (int, float)) or isinstance(eps, bool):
                r.append("epsilon: ε illisible")
            elif eps <= 0 or eps >= 1:
                if eps == 0:
                    r.append("epsilon: ε=0 est un mensonge")
                else:
                    r.append("epsilon: ε hors (0, 1)")
    if horizon is None:
        r.append("horizon absent")
    else:
        if horizon.get("suite") not in ("UFHY1", "mldsa87"):
            r.append("horizon: suite ≠ UFHY1|mldsa87")
        jour = horizon.get("re_presser_avant")
        if jour in SUITES:
            r.append("horizon: UFHY1 est une suite, pas une date")
        else:
            try:
                if not jour or date.fromisoformat(str(jour)) <= datetime.now(timezone.utc).date():
                    r.append("horizon: date passée ou absente")
            except ValueError:
                r.append("horizon: date illisible")
    if bruit is not None and bruit.get("trous") == "fermes" and bruit.get("simule") is True:
        r.append("bruit: fermes + simule")
    r.extend(_faux_bornes(quelle, temoin, epsilon, horizon, bruit))
    return r


def juger(
    quelle=None,
    temoin=None,
    epsilon=None,
    horizon=None,
    bruit=None,
    figure=None,
    extra_eps=None,
    plafond=PLAFOND,
    vues=None,
    liens=None,
    noter=False,
    carte=None,
):
    """MODE juge. Existence d'un dossier ≠ mint quantique. Ne frappe pas un id."""
    raisons = _mode_raisons(quelle, temoin, epsilon, horizon, bruit)
    raisons.extend(fraicheur(quelle, vues))
    raisons.extend(monogamie(temoin, figure, liens, noter=noter))
    som, br = budget(epsilon, extra_eps or [], plafond)
    raisons.extend(br)
    if noter and "fraicheur: empreinte déjà vue" not in raisons:
        noter_vue(quelle, vues)
    quantique = not raisons
    existant = carte if isinstance(carte, dict) else None
    return {
        "mode": "quantique" if quantique else "classique",
        "raisons": [] if quantique else raisons,
        "dossier_id": (existant or {}).get("dossier_id"),
        "quelle_id": (quelle or {}).get("id"),
        "temoin_id": (temoin or {}).get("temoin_id"),
        "epsilon_id": (epsilon or {}).get("epsilon_id"),
        "horizon_id": (horizon or {}).get("horizon_id"),
        "bruit_id": (bruit or {}).get("bruit_id") if bruit else None,
        "figure_id": (figure or {}).get("figure_id") if figure else (temoin or {}).get("figure_id"),
        "budget": som,
        "plafond": plafond,
        "marge": marge(temoin),
        "simule": _simule_presente(quelle, temoin, bruit),
        "note": "bornes tenues." if quantique else "classique. raisons = bornes manquantes.",
    }


def composer(
    quelle=None,
    temoin=None,
    epsilon=None,
    horizon=None,
    bruit=None,
    figure=None,
    extra_eps=None,
    plafond=PLAFOND,
    vues=None,
    liens=None,
    noter=False,
    carte=None,
):
    j = juger(
        quelle=quelle,
        temoin=temoin,
        epsilon=epsilon,
        horizon=horizon,
        bruit=bruit,
        figure=figure,
        extra_eps=extra_eps,
        plafond=plafond,
        vues=vues,
        liens=liens,
        noter=noter,
        carte=carte,
    )
    return {
        "format": FORMAT,
        "dossier_id": j.get("dossier_id") or ("DS-" + uuid.uuid4().hex[:12]),
        "mode": j["mode"],
        "quelle_id": j.get("quelle_id"),
        "temoin_id": j.get("temoin_id"),
        "epsilon_id": j.get("epsilon_id"),
        "horizon_id": j.get("horizon_id"),
        "bruit_id": j.get("bruit_id"),
        "figure_id": j.get("figure_id"),
        "budget": j.get("budget"),
        "plafond": j.get("plafond"),
        "marge": j.get("marge"),
        "raisons": j["raisons"],
        "simule": j["simule"],
        "juridiction": "QC",
        "langue": "fr-CA",
        "pose_at": _now(),
        "note": j["note"],
    }


def _rails(args):
    return dict(
        quelle=_load(args.quelle),
        temoin=_load(args.temoin),
        epsilon=_load(args.epsilon),
        horizon=_load(args.horizon),
        bruit=_load(args.bruit),
        figure=_load(args.figure),
        extra_eps=args.terme,
        plafond=args.plafond,
        vues=Path(args.vues) if args.vues else None,
        liens=Path(args.liens) if args.liens else None,
    )


def _add_rails(parser, vers=None):
    parser.add_argument("--quelle", default=None)
    parser.add_argument("--temoin", default=None)
    parser.add_argument("--epsilon", default=None)
    parser.add_argument("--horizon", default=None)
    parser.add_argument("--bruit", default=None)
    parser.add_argument("--figure", default=None)
    parser.add_argument("--terme", action="append", type=float, default=[])
    parser.add_argument("--plafond", type=float, default=PLAFOND)
    parser.add_argument("--vues", default=None)
    parser.add_argument("--liens", default=None)
    if vers == "lier":
        parser.add_argument("--vers", default="carte.dossier.json")
    elif vers == "juger":
        parser.add_argument("--vers", default=None)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="dossier")
    sub = p.add_subparsers(dest="cmd", required=True)
    slier = sub.add_parser("lier")
    _add_rails(slier, vers="lier")
    sj = sub.add_parser("juger")
    sj.add_argument("fichier", nargs="?", default=None)
    _add_rails(sj, vers="juger")
    sl = sub.add_parser("lire")
    sl.add_argument("fichier")
    args = p.parse_args(argv)
    if args.cmd == "lire":
        print(json.dumps(json.loads(Path(args.fichier).read_text(encoding="utf-8")), ensure_ascii=False, indent=2))
        return 0
    kwargs = _rails(args)
    if args.cmd == "juger":
        carte = None
        if args.fichier:
            carte = _load(args.fichier)
            if not isinstance(carte, dict) or carte.get("format") != FORMAT:
                raise SystemExit("pas une fiche dossier.v0")
        d = juger(carte=carte, noter=False, **kwargs)
        if args.vers:
            Path(args.vers).write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            d = dict(d)
            d["fichier"] = args.vers
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return 0
    d = composer(noter=True, **kwargs)
    Path(args.vers).write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    d["fichier"] = args.vers
    print(json.dumps(d, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
