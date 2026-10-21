"""Interface en ligne de commande : python -m outils_atelier <outil> ..."""

from __future__ import annotations

import argparse
import sys

from . import __version__, coupe, spc, trs


def _construire_parseur() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="outils_atelier", description=__doc__)
    p.add_argument("--version", action="version", version=__version__)
    sous = p.add_subparsers(dest="outil", required=True)

    c = sous.add_parser("coupe", help="vitesse de broche, avance, temps, Ra théorique")
    c.add_argument("--vc", type=float, required=True, help="vitesse de coupe (m/min)")
    c.add_argument("--diametre", type=float, required=True, help="diamètre (mm)")
    c.add_argument("--avance-tr", type=float, help="avance par tour f (mm/tr)")
    c.add_argument("--fz", type=float, help="avance par dent fz (mm/dent), fraisage")
    c.add_argument("--dents", type=int, help="nombre de dents, fraisage")
    c.add_argument("--longueur", type=float, help="longueur à usiner (mm)")
    c.add_argument("--rayon-bec", type=float, help="rayon de bec (mm), pour le Ra théorique")

    t = sous.add_parser("trs", help="taux de rendement synthétique (OEE)")
    t.add_argument("--temps-requis", type=float, required=True, help="minutes")
    t.add_argument("--arrets", type=float, required=True, help="minutes d'arrêt")
    t.add_argument("--cycle", type=float, required=True, help="cycle théorique (s/pièce)")
    t.add_argument("--produites", type=int, required=True)
    t.add_argument("--bonnes", type=int, required=True)

    s = sous.add_parser("capabilite", help="Cp / Cpk depuis un CSV de mesures")
    s.add_argument("fichier", help="CSV avec une colonne de mesures")
    s.add_argument("--colonne", default="mesure")
    s.add_argument("--lsi", type=float, required=True, help="limite inférieure de tolérance")
    s.add_argument("--lss", type=float, required=True, help="limite supérieure de tolérance")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _construire_parseur().parse_args(argv)
    try:
        if args.outil == "coupe":
            n = coupe.vitesse_broche(args.vc, args.diametre)
            print(f"Fréquence de rotation N : {n:.0f} tr/min")
            vf = None
            if args.avance_tr:
                vf = coupe.avance_tournage(n, args.avance_tr)
            elif args.fz and args.dents:
                vf = coupe.avance_fraisage(n, args.fz, args.dents)
            if vf:
                print(f"Vitesse d'avance Vf : {vf:.0f} mm/min")
                if args.longueur:
                    print(f"Temps d'usinage : {coupe.temps_usinage(args.longueur, vf):.1f} s")
            if args.avance_tr and args.rayon_bec:
                ra = coupe.rugosite_theorique_ra_um(args.avance_tr, args.rayon_bec)
                print(f"Ra théorique : {ra:.2f} µm (indicatif, à valider par mesure)")
        elif args.outil == "trs":
            r = trs.calculer_trs(args.temps_requis, args.arrets, args.cycle, args.produites, args.bonnes)
            for cle, val in r.en_pourcent().items():
                print(f"{cle:>13} : {val} %")
        else:
            mesures = spc.lire_mesures_csv(args.fichier, args.colonne)
            r = spc.capabilite(mesures, args.lsi, args.lss)
            print(f"n = {r.n}  moyenne = {r.moyenne:.4f}  écart-type = {r.ecart_type:.4f}")
            print(f"Cp = {r.cp:.2f}   Cpk = {r.cpk:.2f}")
            print(f"Limites 3 sigma : {r.lcl:.4f} ... {r.ucl:.4f}")
            for a in r.avertissements:
                print(f"Attention : {a}")
    except (ValueError, OSError) as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
