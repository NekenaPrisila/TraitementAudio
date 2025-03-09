# TODO: Traitement de son en Python (Approche Orientée Objet)

## 1. Structure du projet
- [ ] Classe `AudioProcessor` pour gérer le son.
- [ ] Lire/écrire des fichiers audio en manipulant les bits (sans bibliothèques externes).
- [ ] Convertir un fichier audio en tableau de bits et inversement.

## 2. Amplification
- [ ] Méthode `amplify` pour amplifier le signal audio.
- [ ] Multiplier les échantillons par un facteur donné.
- [ ] Gérer les dépassements (clip/normalisation).
- [ ] Tester avec un fichier audio.

## 3. Anti-distortion
- [ ] Méthode `anti_distortion` pour limiter la distorsion.
- [ ] Implémenter "soft clipping" ou "hard clipping".
- [ ] Tester avec des signaux à fort volume.

## 4. Anti-bruit
- [ ] Méthode `noise_reduction` pour filtrer le bruit.
- [ ] Filtrage fréquentiel manuel.
- [ ] Soustraction de spectre pour enlever un son spécifique.
- [ ] Tester avec des fichiers audio bruités.

## 5. Interface Graphique (GUI)
- [ ] Interface avec `tkinter` ou `PyQt`.
- [ ] Boutons : charger, amplifier, anti-distortion, anti-bruit, sauvegarde.
- [ ] Visualisation du signal audio avant/après traitement.

## 6. Tests et Optimisation
- [ ] Tester chaque méthode avec différents fichiers.
- [ ] Vérifier la qualité audio après traitement.
- [ ] Optimiser les performances (éviter les boucles lentes).
- [ ] Documenter le code.

## 7. Documentation et Finalisation
- [ ] Docstrings pour chaque méthode.
- [ ] `README.md` avec guide d'utilisation.
- [ ] Exemples de fichiers audio pour tests.
