from os import listdir, path
from os.path import isfile, join
from operator import attrgetter

def determiner_frequences(texte):
    """
    Détermine la fréquence de chaque caractère dans le texte.

    Args:
    - texte (str): Le texte à analyser.

    Returns:
    - dict: Un dictionnaire contenant les caractères et leurs fréquences respectives.
    """
    dictionnaire_frequences = {}
    for char in texte:
        if char in dictionnaire_frequences:
            dictionnaire_frequences[char] += 1
        else:
            dictionnaire_frequences[char] = 1
    dictionnaire_frequences = dict(sorted(dictionnaire_frequences.items(), key=lambda x: (x[1], x[0])))
    return dictionnaire_frequences

class Noeud:
    """
    Classe représentant un noeud dans l'arbre de Huffman.

    Attributes:
    - etiquette (str): Le caractère associé au noeud (None pour les noeuds internes).
    - frequence (int): La fréquence du caractère dans le texte.
    - gauche (Noeud): Le noeud fils gauche.
    - droite (Noeud): Le noeud fils droit.
    """

    def __init__(self, etiquette, frequence, gauche=None, droite=None):
        """
        Initialise un objet Noeud avec un caractère et une fréquence.

        Args:
        - etiquette (str): Le caractère associé au noeud.
        - frequence (int): La fréquence du caractère dans le texte.
        - gauche (Noeud): Le noeud fils gauche.
        - droite (Noeud): Le noeud fils droit.
        """
        self.etiquette = etiquette
        self.frequence = frequence
        self.gauche = gauche
        self.droite = droite
        self.bord = ''

    def obtenirFrequence(self):
        """
        Obtient la fréquence du noeud.

        Returns:
        - int: La fréquence du noeud.
        """
        return self.frequence

    def definirBord(self, valeur):
        """
        Définit la valeur de bord pour le noeud (0 pour gauche, 1 pour droite).

        Args:
        - valeur (str): La valeur de bord ('0' ou '1').
        """
        self.bord = valeur

    def __str__(self):
        return f'{self.etiquette} {self.bord} [{self.gauche},{self.droite}]'

def construire_arbre_huffman(dictionnaire_frequences):
    """
    Construit l'arbre de Huffman à partir du dictionnaire de fréquences.

    Args:
    - dictionnaire_frequences (dict): Un dictionnaire contenant les caractères et leurs fréquences respectives.

    Returns:
    - Noeud: La racine de l'arbre de Huffman.
    """
    noeuds = []
    for char in dictionnaire_frequences:
        noeuds.append(Noeud(char, dictionnaire_frequences[char]))

    while len(noeuds) > 1:
        noeuds.sort(key=attrgetter('frequence', 'etiquette'))
        gauche = noeuds[0]
        gauche.definirBord('0')
        droite = noeuds[1]
        droite.definirBord('1')
        somme = gauche.obtenirFrequence() + droite.obtenirFrequence()
        noeud = Noeud(str(somme), somme, gauche, droite)
        noeuds.remove(gauche)
        noeuds.remove(droite)
        noeuds.append(noeud)
    
    arbre_huffman = noeuds[0]
    return arbre_huffman

def generer_codes_huffman(noeud, valeur, dictionnaire_codes):
    """
    Génère les codes de Huffman pour chaque caractère en parcourant l'arbre.

    Args:
    - noeud (Noeud): Le noeud actuel de l'arbre.
    - valeur (str): Le code binaire actuel.
    - dictionnaire_codes (dict): Le dictionnaire des codes de Huffman.

    Returns:
    - dict: Un dictionnaire contenant les caractères et leurs codes de Huffman respectifs.
    """
    nouvelleValeur = valeur + noeud.bord
    if noeud.gauche is not None:
        generer_codes_huffman(noeud.gauche, nouvelleValeur, dictionnaire_codes)
    if noeud.droite is not None:
        generer_codes_huffman(noeud.droite, nouvelleValeur, dictionnaire_codes)
    if noeud.gauche is None and noeud.droite is None:
        dictionnaire_codes[noeud.etiquette] = nouvelleValeur
    return dictionnaire_codes

def calculer_taux_compression(nom_fichier):
    """
    Calcule le taux de compression obtenu après la compression du fichier.

    Args:
    - nom_fichier (str): Le nom du fichier original.

    Returns:
    - float: Le taux de compression en pourcentage.
    """
    taille_initiale = path.getsize(nom_fichier)
    nom_fichier = nom_fichier.removeprefix('./input/').removesuffix('.txt')
    nom_fichier = f'./output/{nom_fichier}_comp.bin'
    taille_finale = path.getsize(nom_fichier)
    taux = 1 - (taille_finale / taille_initiale)
    taux = round(taux, 4)
    taux *= 100
    return taux

def calculer_bits_moyens(dictionnaire_codes):
    """
    Calcule le nombre moyen de bits nécessaires pour coder chaque caractère.

    Args:
    - dictionnaire_codes (dict): Le dictionnaire des codes de Huffman.

    Returns:
    - float: Le nombre moyen de bits par caractère.
    """
    valeurs = dictionnaire_codes.values()
    res = 0
    for valeur in valeurs:
        res += len(valeur)
    res /= len(valeurs)
    res = round(res, 4)
    return res

def taille_alphabet(dictionnaire_frequences):
    """
    Détermine la taille de l'alphabet (nombre de caractères distincts).

    Args:
    - dictionnaire_frequences (dict): Le dictionnaire des fréquences des caractères.

    Returns:
    - str: La taille de l'alphabet.
    """
    return str(len(dictionnaire_frequences))

def generer_fichier_frequences(nom_fichier, dictionnaire_frequences):
    """
    Génère un fichier contenant les fréquences des caractères.

    Args:
    - nom_fichier (str): Le nom du fichier original.
    - dictionnaire_frequences (dict): Le dictionnaire des fréquences des caractères.
    """
    f = open(f'./output/{nom_fichier}_freq.txt', 'w')
    f.write(f'{taille_alphabet(dictionnaire_frequences)}\n')
    for char in dictionnaire_frequences:
        if char != '\n':
            f.write(f'{char} {str(dictionnaire_frequences[char])}\n')
        else:
            f.write(f'\\n {str(dictionnaire_frequences[char])}\n')
    f.close()
    print(f'Fichier de fréquences pour {nom_fichier} généré avec succès')

def generer_fichier_compresse(nom_fichier, bin):
    """
    Génère un fichier binaire contenant le texte compressé.

    Args:
    - nom_fichier (str): Le nom du fichier original.
    - bin (bytes): Le contenu binaire compressé.
    """
    f = open(f'./output/{nom_fichier}_comp.bin', 'wb')
    f.write(bin)
    f.close()
    print(f'Fichier compressé pour {nom_fichier} généré avec succès')

fichiers = [f for f in listdir('./input') if isfile(join('./input', f))]
for f in fichiers:
    fichier = open(f'./input/{f}', 'r')
    texte_fichier = fichier.read()
    dictionnaire_frequences = determiner_frequences(texte_fichier)
    arbre = construire_arbre_huffman(dictionnaire_frequences)
    codes = generer_codes_huffman(arbre, valeur='', dictionnaire_codes={})
    chaine_binaire = ''
    for char in texte_fichier:
        chaine_binaire += codes[char]
    bin = int(chaine_binaire, base=2).to_bytes((len(chaine_binaire) + 7) // 8, byteorder='big')
    nom_fichier = fichier.name.removeprefix('./input/').removesuffix('.txt')
    print(f'\nRésultats pour {nom_fichier} :')
    generer_fichier_compresse(nom_fichier, bin)
    generer_fichier_frequences(nom_fichier, dictionnaire_frequences)
    print(f'Taux de compression : {calculer_taux_compression(fichier.name)}%')
    print(f'Nombre moyen de bits par caractère : {calculer_bits_moyens(codes)}')
