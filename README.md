# Projet de Compression de Données par Codage de Huffman ! 🎉

## Introduction
Ce projet implémente l'algorithme de compression de données par codage de Huffman. Le codage de Huffman est une technique de compression de données sans perte largement utilisée qui repose sur la construction d'un arbre binaire où les caractères les plus fréquents sont associés à des codes binaires plus courts, tandis que les caractères moins fréquents sont associés à des codes binaires plus longs.

## Décomposition Fonctionnelle du Programme
Le programme se compose des éléments fonctionnels suivants :

1. **Calcul des Fréquences**: La fonction `determiner_frequences` analyse le texte d'entrée pour déterminer la fréquence de chaque caractère.
2. **Construction de l'Arbre de Huffman**: La fonction `construire_arbre_huffman` construit un arbre binaire de Huffman en utilisant les fréquences des caractères, où les caractères les moins fréquents se trouvent aux feuilles de l'arbre.
3. **Codage des Données**: La fonction `generer_codes_huffman` génère les codes binaires correspondant à chaque caractère en parcourant l'arbre de Huffman de la racine aux feuilles.
4. **Stockage des Données Compressées**: La fonction `generer_fichier_compresse` stocke les codes binaires obtenus dans un fichier binaire compact.
5. **Génération d'Informations**: La fonction `generer_fichier_frequences` génère et sauvegarde dans un fichier texte des informations sur l'alphabet et les fréquences des caractères.

## Aspects Techniques
- **Langage de Programmation**: Le programme est écrit en Python.
- **Algorithmes Utilisés**: L'algorithme de codage de Huffman est implémenté pour la compression des données.
- **Structures de Données**: Une file de priorité est utilisée pour la construction de l'arbre de Huffman, et des dictionnaires sont employés pour stocker les fréquences des caractères et les correspondances entre les caractères et leurs codes binaires.
- **Manipulation de Fichiers**: Le programme lit le texte d'entrée à partir d'un fichier et stocke les données compressées dans un autre fichier.

## Mode d'Emploi
1. Clonez ce dépôt dans un dossier local sur votre machine.
2. Placez le fichier texte que vous souhaitez compresser dans le dossier `./input`.
3. Exécutez le fichier Python dans le terminal en utilisant la commande suivante :
   ```sh
   python codage.py
