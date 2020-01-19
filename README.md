# Amtenael Linux
Launcher pour le jeu Dark Age of Camelot (plus particulièrement, le serveur [Amtenael](https://amtenael.fr)) visant a imiter le fonctionnement de `Patcher.exe` (launcher officiel).

## Fonctionnement
- Avant toute choses, le logiciel vérifie la présence de `game.dll` qui témoigne d'une installation de DAoC pour eviter une execution n'importe ou,
- `CheckFiles()` vérifie le hash md5 des fichiers, et les re-télécharge si besoin,
- Une fois la vérification faite, `AmtenaelLauncher()` (la fenetre) se lance et nous affiche une interface de login très recherchée (non).

## Compilation
*Vous aurez besoin de `cython3` et `gcc`*
- `./configure`
- `make`
- `make clean`

## Pré-requis
- [Wine](https://winehq.org)
- Installation fonctionnelle de Dark Age of Camelot (via [Lutris](https://lutris.net/games/dark-age-of-camelot/) par exemple)
- `requests` (`pip install requests`)
- `tkinter` (différent selon les distributions)
- Python 3 ([Python 2 is dead](https://pythonclock.org/))