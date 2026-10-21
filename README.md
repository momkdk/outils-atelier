# outils-atelier

🔗 **Essayer en ligne, gratuitement : [momkdk.github.io/outils-atelier](https://momkdk.github.io/outils-atelier/)**

Petits outils de calcul open source (licence MIT) pour les ateliers d'usinage et de décolletage.
Python pur, aucune dépendance, utilisable en ligne de commande, comme bibliothèque, ou directement dans le navigateur via la page ci-dessus.

Objectif : des calculs simples, vérifiables et testés, que n'importe quel atelier peut lire, adapter et brancher à ses propres fichiers.

## Les outils

| Outil | Ce qu'il fait |
|---|---|
| `coupe` | Fréquence de broche (tr/min) depuis Vc et le diamètre, vitesse d'avance en tournage ou fraisage, temps d'usinage, Ra théorique |
| `trs` | Taux de rendement synthétique (OEE) : disponibilité x performance x qualité |
| `capabilite` | Cp, Cpk et limites 3 sigma depuis un fichier CSV de mesures |

## Utilisation

```
python -m outils_atelier coupe --vc 100 --diametre 20 --avance-tr 0.1 --longueur 50 --rayon-bec 0.4
python -m outils_atelier trs --temps-requis 480 --arrets 60 --cycle 30 --produites 700 --bonnes 679
python -m outils_atelier capabilite exemples/mesures-fictives.csv --lsi 9.95 --lss 10.05
```

Dans le code :

```python
from outils_atelier import coupe, trs, spc

n = coupe.vitesse_broche(vc_m_min=100, diametre_mm=20)
r = trs.calculer_trs(480, 60, 30, 700, 679)
res = spc.capabilite(mesures, lsi=9.95, lss=10.05)
```

## Limites à connaître

- Le **Ra théorique** est une valeur indicative (f² / 32r). L'état de surface réel dépend de l'outil, de la matière, des vibrations et de la lubrification : il se valide par une mesure sur pièce.
- **Cp / Cpk** : calcul avec l'écart-type d'échantillon. Fiables avec au moins 25 mesures et un procédé stable. L'outil avertit sinon. Ce n'est pas une étude de capabilité complète.
- Le fichier `exemples/mesures-fictives.csv` contient des **données inventées** pour la démonstration. Il ne représente aucune pièce ni aucun atelier réel.
- Ces outils aident au calcul, ils ne remplacent ni les données constructeur ni la validation par une personne compétente.

## Tests

```
python -m unittest discover -s tests -v
```

## Contribuer

Les retours d'ateliers sont les bienvenus : un calcul qui manque, une unité qui prête à confusion, un cas réel mal géré. Ouvrez une issue ou une proposition de modification.

## Auteur

Mohamed Ali El Amri, développeur freelance Python et IA, Cluses (Haute-Savoie). Outils sur mesure et formation des équipes pour l'industrie.

Licence MIT.
