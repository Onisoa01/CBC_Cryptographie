import random

def texte_vers_binaire(texte):
    """Convertit un texte en une chaîne binaire."""
    return ''.join(format(ord(c), '08b') for c in texte)

def binaire_vers_texte(binaire_texte):
    """Convertit une chaîne binaire en texte."""
    octets = [binaire_texte[i:i + 8] for i in range(0, len(binaire_texte), 8)]
    return ''.join(chr(int(octet, 2)) for octet in octets)

def decoupage_et_remplissage(binaire_texte, taille_bloc):
    """Découpe une chaîne binaire en blocs et remplit avec des zéros."""
    blocs = []
    for i in range(0, len(binaire_texte), taille_bloc):
        bloc = binaire_texte[i:i + taille_bloc]
        bloc = bloc.ljust(taille_bloc, '0')
        blocs.append(bloc)
    return blocs

def permutation(bloc, permutation_table):
    """Effectue une permutation des bits du bloc."""
    permuted_bloc = ''.join(bloc[i] for i in permutation_table)
    return permuted_bloc

def inversion_permutation(bloc, permutation_table):
    """Inverse la permutation des bits du bloc."""
    inverse_permutation_table = [0] * len(permutation_table)
    for i, j in enumerate(permutation_table):
        inverse_permutation_table[j] = i
    return permutation(bloc, inverse_permutation_table)

def chiffrement_xor(bloc, cle_binaire):
    """Chiffre un bloc binaire avec XOR."""
    resultat = ''
    for i in range(len(bloc)):
        resultat += str(int(bloc[i]) ^ int(cle_binaire[i % len(cle_binaire)]))
    return resultat

def dechiffrement_xor(bloc_chiffre, cle_binaire):
    """Déchiffre un bloc binaire chiffré avec XOR."""
    return chiffrement_xor(bloc_chiffre, cle_binaire)

def generer_cle_aleatoire(taille_cle):
    """Génère une clé binaire aléatoire."""
    return ''.join(random.choice(['0', '1']) for _ in range(taille_cle))

def generer_permutation_table(taille_bloc):
    """Génère une table de permutation aléatoire."""
    table = list(range(taille_bloc))
    random.shuffle(table)
    return table

def xor(bloc1, bloc2):
    """Effectue un XOR entre deux blocs binaires."""
    resultat = ''
    for i in range(len(bloc1)):
        resultat += str(int(bloc1[i]) ^ int(bloc2[i]))
    return resultat

def chiffrement_cbc(blocs, cle_binaire, iv, permutation_table):
    """Chiffre des blocs binaires en mode CBC."""
    blocs_chiffres = []
    bloc_precedent = iv
    for bloc in blocs:
        bloc_permute = permutation(bloc, permutation_table)
        bloc_xor = xor(bloc_permute, bloc_precedent)
        bloc_chiffre = chiffrement_xor(bloc_xor, cle_binaire)
        blocs_chiffres.append(bloc_chiffre)
        bloc_precedent = bloc_chiffre
    return blocs_chiffres

def dechiffrement_cbc(blocs_chiffres, cle_binaire, iv, permutation_table):
    """Déchiffre des blocs binaires chiffrés en mode CBC."""
    blocs_dechiffres = []
    bloc_precedent = iv
    for bloc_chiffre in blocs_chiffres:
        bloc_xor = dechiffrement_xor(bloc_chiffre, cle_binaire)
        bloc_dechiffre = xor(bloc_xor, bloc_precedent)
        bloc_inverse_permutation = inversion_permutation(bloc_dechiffre, permutation_table)
        blocs_dechiffres.append(bloc_inverse_permutation)
        bloc_precedent = bloc_chiffre
    return blocs_dechiffres

def generer_iv_aleatoire(taille_iv):
    """Génère un IV binaire aléatoire."""
    return ''.join(random.choice(['0', '1']) for _ in range(taille_iv))

# 1. Saisie et conversion en binaire
texte_utilisateur = input("Entrez le texte à chiffrer : ")
binaire_texte = texte_vers_binaire(texte_utilisateur)
print("Texte en binaire :", binaire_texte)

# 2. Choix de la taille des blocs
taille_bloc = int(input("Entrez la taille des blocs (128 ou 256) : "))

# 3. Découpage et remplissage
blocs_binaires = decoupage_et_remplissage(binaire_texte, taille_bloc)
print("Blocs binaires :", blocs_binaires)

# 4. Génération de la table de permutation
permutation_table = generer_permutation_table(taille_bloc)
print("Table de permutation :", permutation_table)

# 5. Saisie de la clé et conversion en binaire
cle_utilisateur = input("Entrez la clé (lettres) : ")
cle_binaire = texte_vers_binaire(cle_utilisateur)
print("Clé binaire :", cle_binaire)

# 6. Génération de l'IV aléatoire
iv_binaire = generer_iv_aleatoire(taille_bloc)
print("IV binaire aléatoire :", iv_binaire)

# 7. Chiffrement CBC
blocs_chiffres = chiffrement_cbc(blocs_binaires, cle_binaire, iv_binaire, permutation_table)
print("Blocs chiffrés (CBC) :")
for bloc in blocs_chiffres:
    print(bloc)

# 8. Déchiffrement CBC
blocs_dechiffres = dechiffrement_cbc(blocs_chiffres, cle_binaire, iv_binaire, permutation_table)
print("Blocs déchiffrés (CBC) :")
for bloc in blocs_dechiffres:
    print(bloc)

# 9. Conversion binaire vers texte
binaire_texte_dechiffre = ''.join(blocs_dechiffres)
texte_dechiffre = binaire_vers_texte(binaire_texte_dechiffre.rstrip('0'))
print("Texte déchiffré :", texte_dechiffre)