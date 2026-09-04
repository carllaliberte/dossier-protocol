#!/usr/bin/env python3
"""Physics locks for DOSSIER v0. Tests, not a theorem. Not a QUANTUM seal."""

from __future__ import annotations

import json
import math
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import dossier  # noqa: E402

TSIRELSON = 2 * math.sqrt(2)


def _quelle(**overrides):
    carte = {
        "id": "QL-test",
        "source": "qrng",
        "appareil": "IDQ-Quantis",
        "simule": False,
        "sha256": "a" * 64,
    }
    carte.update(overrides)
    return carte


def _temoin(**overrides):
    carte = {
        "temoin_id": "TM-test",
        "niveau": "fabricant",
        "figure_id": "FG-one",
    }
    carte.update(overrides)
    return carte


def _epsilon(**overrides):
    carte = {
        "epsilon_id": "EP-test",
        "modele": "composable",
        "epsilon": 1e-6,
    }
    carte.update(overrides)
    return carte


def _horizon(**overrides):
    carte = {
        "horizon_id": "HZ-test",
        "suite": "UFHY1",
        "re_presser_avant": "2028-08-31",
    }
    carte.update(overrides)
    return carte


def _juger(**overrides):
    kwargs = {
        "quelle": _quelle(),
        "temoin": _temoin(),
        "epsilon": _epsilon(),
        "horizon": _horizon(),
    }
    kwargs.update(overrides)
    return dossier.juger(**kwargs)


def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)


def _cli(args, cwd=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "dossier.py"), *args],
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
    )


def _write(tmp, name, obj) -> str:
    p = Path(tmp) / name
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return str(p)


class EmptyLierIsClassique(unittest.TestCase):
    def test_composer_without_rails_is_classique(self):
        carte = dossier.composer()
        self.assertEqual(carte["mode"], "classique")
        self.assertIn("quelle absente", carte["raisons"])
        self.assertIn("temoin absent", carte["raisons"])
        self.assertIn("epsilon absent", carte["raisons"])
        self.assertIn("horizon absent", carte["raisons"])
        self.assertNotEqual(carte["mode"], "quantique")

    def test_juger_without_rails_is_classique(self):
        jugement = dossier.juger()
        self.assertEqual(jugement["mode"], "classique")
        self.assertIsNone(jugement["dossier_id"])
        self.assertIn("quelle absente", jugement["raisons"])

    def test_cli_lier_without_rails_is_classique(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "carte.dossier.json"
            proc = _cli(["lier", "--vers", str(dest)], cwd=tmp)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertEqual(out["mode"], "classique")
            self.assertNotEqual(out["mode"], "quantique")
            written = json.loads(dest.read_text(encoding="utf-8"))
            self.assertEqual(written["mode"], "classique")

    def test_cli_juger_without_rails_is_classique_and_does_not_mint(self):
        proc = _cli(["juger"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["mode"], "classique")
        self.assertIsNone(out.get("dossier_id"))
        self.assertNotIn("format", out)

    def test_example_classique_card_names_four_absences(self):
        carte = json.loads((ROOT / "examples" / "classique.dossier.json").read_text(encoding="utf-8"))
        self.assertEqual(carte["mode"], "classique")
        self.assertIn("quelle absente", carte["raisons"])
        self.assertIn("temoin absent", carte["raisons"])
        self.assertIn("epsilon absent", carte["raisons"])
        self.assertIn("horizon absent", carte["raisons"])


class Interdit1ExistenceIsNotQuantique(unittest.TestCase):
    def test_juger_existing_dossier_does_not_mint_quantique(self):
        existant = json.loads((ROOT / "examples" / "classique.dossier.json").read_text(encoding="utf-8"))
        jugement = dossier.juger(carte=existant)
        self.assertEqual(jugement["mode"], "classique")
        self.assertEqual(jugement["dossier_id"], "DS-fictif-001")
        self.assertNotEqual(jugement["mode"], "quantique")

    def test_juger_card_claiming_quantique_without_rails_is_classique(self):
        mensonge = {
            "format": "dossier.v0",
            "dossier_id": "DS-lie-001",
            "mode": "quantique",
            "raisons": [],
            "simule": False,
        }
        jugement = dossier.juger(carte=mensonge)
        self.assertEqual(jugement["mode"], "classique")
        self.assertEqual(jugement["dossier_id"], "DS-lie-001")
        self.assertIn("quelle absente", jugement["raisons"])

    def test_cli_juger_example_keeps_id_and_does_not_write(self):
        example = ROOT / "examples" / "classique.dossier.json"
        before = example.read_text(encoding="utf-8")
        proc = _cli(["juger", str(example)])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["mode"], "classique")
        self.assertEqual(out["dossier_id"], "DS-fictif-001")
        self.assertNotIn("fichier", out)
        self.assertEqual(example.read_text(encoding="utf-8"), before)

    def test_cli_juger_does_not_write_unless_asked(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "no-write.dossier.json"
            proc = _cli(["juger"], cwd=tmp)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertFalse(dest.exists())
            self.assertFalse((Path(tmp) / "carte.dossier.json").exists())

    def test_cli_juger_writes_only_if_vers_asked(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "jugement.json"
            proc = _cli(["juger", str(ROOT / "examples" / "classique.dossier.json"), "--vers", str(dest)])
            self.assertEqual(proc.returncode, 0, proc.stderr)
            written = json.loads(dest.read_text(encoding="utf-8"))
            self.assertEqual(written["dossier_id"], "DS-fictif-001")
            self.assertEqual(written["mode"], "classique")


class Interdit2IbmQunetsimWebcam(unittest.TestCase):
    def test_ibm_as_borne_is_not_quantique(self):
        jugement = _juger(quelle=_quelle(appareil="IBM Quantum Processor"))
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("ibm" in r for r in jugement["raisons"]))

    def test_qunetsim_as_borne_is_not_quantique(self):
        jugement = _juger(temoin=_temoin(note="QuNetSim lab run"))
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("qunetsim" in r for r in jugement["raisons"]))

    def test_webcam_as_borne_is_not_quantique(self):
        jugement = _juger(quelle=_quelle(appareil="webcam entropy"))
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("webcam" in r for r in jugement["raisons"]))

    def test_four_gates_without_faux_borne_may_be_quantique(self):
        jugement = _juger()
        self.assertEqual(jugement["mode"], "quantique")
        self.assertEqual(jugement["raisons"], [])


class Interdit3BudgetOverPlafond(unittest.TestCase):
    def test_somme_over_plafond_is_classique(self):
        jugement = _juger(epsilon=_epsilon(epsilon=1e-6, termes=[1e-6]), plafond=1e-6)
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("budget" in r and "plafond" in r for r in jugement["raisons"]))
        dumped = _dump(jugement).lower()
        self.assertNotIn("sûre", dumped)
        self.assertNotIn("sure", dumped)

    def test_cli_terme_over_plafond_is_classique(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = {
                "quelle": _write(tmp, "q.json", _quelle()),
                "temoin": _write(tmp, "t.json", _temoin()),
                "epsilon": _write(tmp, "e.json", _epsilon()),
                "horizon": _write(tmp, "h.json", _horizon()),
            }
            proc = _cli(
                [
                    "juger",
                    "--quelle", paths["quelle"],
                    "--temoin", paths["temoin"],
                    "--epsilon", paths["epsilon"],
                    "--horizon", paths["horizon"],
                    "--terme", "1e-5",
                ]
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertEqual(out["mode"], "classique")
            self.assertTrue(any("budget" in r for r in out["raisons"]))
            self.assertNotIn("sure", proc.stdout.lower())


class Interdit4FraicheurReplay(unittest.TestCase):
    def test_replay_quelle_sha256_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            vues = Path(tmp) / "vues.json"
            vues.write_text(json.dumps({"sha256": ["a" * 64]}), encoding="utf-8")
            jugement = _juger(vues=vues)
            self.assertEqual(jugement["mode"], "classique")
            self.assertIn("fraicheur: empreinte déjà vue", jugement["raisons"])

    def test_juger_replay_does_not_write_vues(self):
        with tempfile.TemporaryDirectory() as tmp:
            vues = Path(tmp) / "vues.json"
            vues.write_text(json.dumps({"sha256": []}), encoding="utf-8")
            jugement = _juger(vues=vues, noter=False)
            self.assertEqual(jugement["mode"], "quantique")
            mem = json.loads(vues.read_text(encoding="utf-8"))
            self.assertEqual(mem.get("sha256"), [])

    def test_lier_notes_sha_then_replay_refuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            vues = Path(tmp) / "vues.json"
            first = dossier.composer(
                quelle=_quelle(),
                temoin=_temoin(),
                epsilon=_epsilon(),
                horizon=_horizon(),
                vues=vues,
                noter=True,
            )
            self.assertEqual(first["mode"], "quantique")
            second = dossier.juger(
                quelle=_quelle(),
                temoin=_temoin(),
                epsilon=_epsilon(),
                horizon=_horizon(),
                vues=vues,
            )
            self.assertEqual(second["mode"], "classique")
            self.assertIn("fraicheur: empreinte déjà vue", second["raisons"])


class Interdit5Monogamie(unittest.TestCase):
    def test_same_transcript_on_two_figure_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            liens = Path(tmp) / "liens.json"
            tr = "b" * 64
            first = dossier.composer(
                quelle=_quelle(),
                temoin=_temoin(niveau="di", transcript_sha256=tr, chsh=2.5, figure_id="FG-one"),
                epsilon=_epsilon(),
                horizon=_horizon(),
                figure={"figure_id": "FG-one"},
                liens=liens,
                noter=True,
            )
            self.assertEqual(first["mode"], "quantique")
            second = dossier.juger(
                quelle=_quelle(),
                temoin=_temoin(niveau="di", transcript_sha256=tr, chsh=2.5, figure_id="FG-two"),
                epsilon=_epsilon(),
                horizon=_horizon(),
                figure={"figure_id": "FG-two"},
                liens=liens,
            )
            self.assertEqual(second["mode"], "classique")
            self.assertTrue(any("monogamie" in r and "FG-one" in r for r in second["raisons"]))

    def test_juger_does_not_write_liens(self):
        with tempfile.TemporaryDirectory() as tmp:
            liens = Path(tmp) / "liens.json"
            dossier.juger(
                quelle=_quelle(),
                temoin=_temoin(niveau="di", transcript_sha256="c" * 64, chsh=2.5, figure_id="FG-one"),
                epsilon=_epsilon(),
                horizon=_horizon(),
                figure={"figure_id": "FG-one"},
                liens=liens,
                noter=False,
            )
            self.assertFalse(liens.exists())


class Interdit6NoTokenOrProductionBadge(unittest.TestCase):
    def test_juger_json_has_no_token_or_production_badge(self):
        dumped = _dump(dossier.juger())
        self.assertNotIn("token", dumped.lower())
        self.assertNotIn("badge production", dumped.lower())
        self.assertNotIn("Quantum Mode ON", dumped)
        self.assertNotIn("production badge", dumped.lower())

    def test_composer_json_has_no_token_or_production_badge(self):
        dumped = _dump(dossier.composer())
        self.assertNotIn("token", dumped.lower())
        self.assertNotIn("badge", dumped.lower())
        self.assertNotIn("QUANTUM", dumped)

    def test_example_has_no_token_or_production_badge(self):
        text = (ROOT / "examples" / "classique.dossier.json").read_text(encoding="utf-8")
        self.assertNotIn("token", text.lower())
        self.assertNotIn("badge", text.lower())
        self.assertNotIn("QUANTUM", text)


class Interdit7EpsilonOpenInterval(unittest.TestCase):
    def test_epsilon_zero_is_a_lie(self):
        jugement = _juger(epsilon=_epsilon(epsilon=0))
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("ε=0" in r or "mensonge" in r for r in jugement["raisons"]))

    def test_epsilon_one_is_not_a_bound(self):
        jugement = _juger(epsilon=_epsilon(epsilon=1))
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("(0, 1)" in r for r in jugement["raisons"]))
        self.assertFalse(any("(0, 1]" in r for r in jugement["raisons"]))

    def test_epsilon_one_float_refuses(self):
        jugement = _juger(epsilon=_epsilon(epsilon=1.0))
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("hors (0, 1)" in r for r in jugement["raisons"]))

    def test_epsilon_missing_is_absent_not_zero(self):
        carte = {"epsilon_id": "EP-missing", "modele": "composable"}
        jugement = _juger(epsilon=carte)
        self.assertEqual(jugement["mode"], "classique")
        self.assertIn("epsilon: ε absent", jugement["raisons"])
        self.assertFalse(any("ε=0" in r for r in jugement["raisons"]))

    def test_copy_has_no_closed_interval(self):
        for rel in ("README.md", "INTERDIT.md", "JUGE.md", "dossier.py"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("(0, 1]", text, msg=rel)


class Interdit8SimuleIsAPresentedClaim(unittest.TestCase):
    def test_no_cards_is_classique_and_not_a_simulation(self):
        jugement = dossier.juger()
        self.assertEqual(jugement["mode"], "classique")
        self.assertIs(jugement["simule"], False)

    def test_empty_composer_does_not_restamp_simule(self):
        carte = dossier.composer()
        self.assertEqual(carte["mode"], "classique")
        self.assertIs(carte["simule"], False)

    def test_epsilon_zero_refuse_is_not_a_simulation(self):
        jugement = _juger(epsilon=_epsilon(epsilon=0))
        self.assertEqual(jugement["mode"], "classique")
        self.assertIs(jugement["simule"], False)

    def test_quelle_simule_keeps_the_claim(self):
        jugement = _juger(quelle=_quelle(simule=True))
        self.assertEqual(jugement["mode"], "classique")
        self.assertIs(jugement["simule"], True)
        self.assertIn("quelle: simule", jugement["raisons"])

    def test_example_classique_card_is_not_a_simulation(self):
        carte = json.loads((ROOT / "examples" / "classique.dossier.json").read_text(encoding="utf-8"))
        self.assertEqual(carte["mode"], "classique")
        self.assertIs(carte["simule"], False)

    def test_cli_lier_empty_does_not_stamp_simule(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "vide.dossier.json"
            proc = _cli(["lier", "--vers", str(dest)], cwd=tmp)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertEqual(out["mode"], "classique")
            self.assertIs(out["simule"], False)


class Interdit9ChshOnlyViaTemoin(unittest.TestCase):
    def test_chsh_above_tsirelson_is_refused(self):
        jugement = _juger(temoin=_temoin(niveau="di", transcript_sha256="d" * 64, chsh=TSIRELSON + 0.1))
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("CHSH > 2√2" in r for r in jugement["raisons"]))

    def test_marge_comes_only_from_temoin(self):
        jugement = _juger(temoin=_temoin(niveau="di", transcript_sha256="e" * 64, chsh=2.5))
        self.assertAlmostEqual(jugement["marge"], TSIRELSON - 2.5)
        self.assertNotIn("chsh", jugement)

    def test_quelle_chsh_does_not_mint_a_channel(self):
        jugement = _juger(quelle=_quelle(chsh=2.7))
        self.assertIsNone(jugement["marge"])
        dumped = _dump(jugement)
        self.assertNotIn("photon", dumped.lower())
        self.assertNotIn("bell", dumped.lower())
        self.assertNotIn('"chsh"', dumped)

    def test_composer_does_not_mint_a_channel_field(self):
        carte = dossier.composer()
        self.assertNotIn("chsh", carte)
        self.assertNotIn("canal", carte)
        self.assertNotIn("photon", carte)
        self.assertIsNone(carte["marge"])


class Interdit10Ufhy1IsASuite(unittest.TestCase):
    def test_ufhy1_as_calendar_date_is_refused(self):
        jugement = _juger(horizon=_horizon(re_presser_avant="UFHY1"))
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("suite" in r and "date" in r for r in jugement["raisons"]))

    def test_missing_horizon_day_is_not_quantique(self):
        jugement = _juger(horizon=_horizon(re_presser_avant=None))
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("date" in r for r in jugement["raisons"]))

    def test_expired_horizon_day_is_not_quantique(self):
        jugement = _juger(horizon=_horizon(re_presser_avant="2020-01-01"))
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("date passée" in r or "date" in r for r in jugement["raisons"]))


class FourGatesMayBeQuantique(unittest.TestCase):
    def test_four_gates_with_epsilon_in_open_interval_is_quantique(self):
        jugement = _juger()
        self.assertEqual(jugement["mode"], "quantique")
        self.assertEqual(jugement["raisons"], [])
        self.assertIs(jugement["simule"], False)

    def test_cli_juger_with_four_gates_does_not_mint(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = []
            for nom, carte in (
                ("quelle", _quelle()),
                ("temoin", _temoin()),
                ("epsilon", _epsilon()),
                ("horizon", _horizon()),
            ):
                args.extend(["--" + nom, _write(tmp, nom + ".json", carte)])
            proc = _cli(["juger", *args])
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertEqual(out["mode"], "quantique")
            self.assertIsNone(out.get("dossier_id"))
            self.assertFalse((Path(tmp) / "carte.dossier.json").exists())


class CliSurfaceStays(unittest.TestCase):
    def test_help_keeps_lier_lire_juger(self):
        proc = _cli(["-h"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("lier", proc.stdout)
        self.assertIn("lire", proc.stdout)
        self.assertIn("juger", proc.stdout)

    def test_lire_example(self):
        proc = _cli(["lire", str(ROOT / "examples" / "classique.dossier.json")])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["dossier_id"], "DS-fictif-001")
        self.assertEqual(out["mode"], "classique")

    def test_juger_unknown_format_refuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = _write(tmp, "pas-dossier.json", {"format": "quelle.v0", "id": "QL-x"})
            proc = _cli(["juger", p])
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("dossier.v0", proc.stderr + proc.stdout)


class NoQuantumSealInJson(unittest.TestCase):
    def test_juger_json_is_not_a_quantum_seal(self):
        dumped = _dump(dossier.juger())
        self.assertNotIn("QUANTUM", dumped)
        self.assertNotIn("quantum seal", dumped.lower())
        self.assertNotIn("Imagine", dumped)

    def test_composer_json_is_not_a_quantum_seal(self):
        dumped = _dump(dossier.composer())
        self.assertNotIn("QUANTUM", dumped)
        self.assertNotIn("Imagine", dumped)
        self.assertEqual(json.loads(dumped)["mode"], "classique")

    def test_quantique_verdict_json_is_not_a_quantum_seal(self):
        dumped = _dump(_juger())
        self.assertEqual(json.loads(dumped)["mode"], "quantique")
        self.assertNotIn("QUANTUM", dumped)
        self.assertNotIn("Imagine", dumped)

    def test_cli_juger_example_is_not_a_quantum_seal(self):
        proc = _cli(["juger", str(ROOT / "examples" / "classique.dossier.json")])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn("QUANTUM", proc.stdout)
        self.assertNotIn("Imagine", proc.stdout)


class ReadmeDoorCopy(unittest.TestCase):
    def test_readme_has_no_imagine_word(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("Imagine", text)
        self.assertNotIn("imagine", text)

    def test_readme_does_not_claim_formal_verification(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("formally verified", text)
        self.assertNotIn("formally-verified", text)
        self.assertNotIn("formellement vérifié", text)

    def test_readme_leads_with_the_envelope(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Une enveloppe. MODE juge. Sans bornes = classique.", text)
        self.assertIn("python3 dossier.py lier", text)
        self.assertIn("python3 dossier.py lire", text)
        self.assertIn("python3 dossier.py juger", text)
        self.assertIn("(0, 1)", text)
        self.assertNotIn("(0, 1]", text)

    def test_readme_names_the_locks(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("INTERDIT 1", text)
        self.assertIn("INTERDIT 10", text)
        self.assertIn("FRAÎCHEUR", text)
        self.assertIn("MONOGAMIE", text)
        self.assertIn("Verified vs assumed", text)

    def test_copy_on_this_rail_has_no_imagine_word(self):
        for rel in ("README.md", "INTERDIT.md", "JUGE.md", "dossier.py"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("Imagine", text, msg=rel)

    def test_interdit_ritual_stays(self):
        text = (ROOT / "INTERDIT.md").read_text(encoding="utf-8")
        self.assertIn("`mode: quantique` parce que le dossier existe.", text)
        self.assertIn("Job IBM / QuNetSim / webcam comme borne.", text)
        self.assertIn("Token, badge production.", text)
        self.assertIn("ε=0 (mensonge). Intervalle (0, 1) exclusif. ε=1 comme borne.", text)
        self.assertIn("`simule=true` sans carte présentée.", text)
        self.assertIn("CHSH hors TÉMOIN. CHSH > Tsirelson. Canal inventé.", text)
        self.assertIn("UFHY1 est une suite, pas une date. Jour d'horizon passé ou absent.", text)
        self.assertIn("Le défaut est `classique`.", text)


class InterditRitualAgreesWithDoor(unittest.TestCase):
    """Door README and ritual INTERDIT.md must name the same numbered locks."""

    SHARED = {
        1: ("mode: quantique",),
        2: ("IBM", "QuNetSim", "webcam"),
        3: ("plafond",),
        4: ("QUELLE",),
        5: ("Bell", "FIGURE"),
        6: ("token", "badge"),
        7: ("ε=0", "(0, 1)"),
        8: ("simule",),
        9: ("CHSH", "TÉMOIN"),
        10: ("UFHY1",),
    }

    def _ritual_items(self, text):
        return {int(n): body.strip() for n, body in re.findall(r"^(\d+)\.\s+(.+)$", text, re.M)}

    def _door_locks(self, text):
        return {
            int(n): body.strip()
            for n, body in re.findall(r"\*\*INTERDIT (\d+)\.\*\*\s+(.+)", text)
        }

    def _v0_is_not(self, text):
        m = re.search(r"^## What v0 is not\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
        self.assertIsNotNone(m, "README missing ## What v0 is not")
        return {int(n): body.strip() for n, body in re.findall(r"^(\d+)\.\s+(.+)$", m.group(1), re.M)}

    def _has(self, haystack, needle):
        return needle.lower() in haystack.lower()

    def test_readme_and_interdit_share_numbers_1_to_10(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        ritual = (ROOT / "INTERDIT.md").read_text(encoding="utf-8")
        expected = list(range(1, 11))
        ritual_items = self._ritual_items(ritual)
        door_locks = self._door_locks(readme)
        v0_is_not = self._v0_is_not(readme)
        self.assertEqual(sorted(ritual_items), expected)
        self.assertEqual(sorted(door_locks), expected)
        self.assertEqual(sorted(v0_is_not), expected)

    def test_each_number_shares_the_door_lock_tokens(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        ritual = (ROOT / "INTERDIT.md").read_text(encoding="utf-8")
        ritual_items = self._ritual_items(ritual)
        door_locks = self._door_locks(readme)
        for n, tokens in self.SHARED.items():
            for token in tokens:
                self.assertTrue(
                    self._has(ritual_items[n], token),
                    f"INTERDIT.md #{n} missing {token!r}: {ritual_items[n]}",
                )
                self.assertTrue(
                    self._has(door_locks[n], token),
                    f"README INTERDIT {n} missing {token!r}: {door_locks[n]}",
                )

    def test_door_seven_to_ten_match_existing_physics(self):
        ritual = (ROOT / "INTERDIT.md").read_text(encoding="utf-8")
        items = self._ritual_items(ritual)
        self.assertIn("exclusif", items[7])
        self.assertIn("ε=1", items[7])
        self.assertNotIn("(0, 1]", items[7])
        self.assertIn("présentée", items[8])
        self.assertIn("Tsirelson", items[9])
        self.assertIn("Canal inventé", items[9])
        self.assertIn("suite", items[10])
        self.assertIn("date", items[10])
        self.assertIn("passé", items[10])
        self.assertIn("absent", items[10])


if __name__ == "__main__":
    unittest.main()
