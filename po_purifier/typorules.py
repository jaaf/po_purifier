#!/usr/bin/python
# coding: utf8 

locale='fr'
language ='fr_FR.UTF-8' # the language code for localization of the program
# trois croisillons indiquent une règle alternative non retenue
# explicitation des caractères invisibles pour expliquer la regex : n espace normale, i insécable f fine insécable
sr=[]
n1sp = r'([   \t]+ [   \t]*|[   \t]* [   \t]+|[  \t]*)'#n'est pas, une, et une seule, espace normale
n1fusp = r'([   \t]+ [   \t]*|[   \t]* [   \t]+|[  \t]*)'#n'est pas, une, et une seule, espace fine insécable normale (fine unbreakable space)
n1usp = r'([   \t]+ [   \t]*|[   \t]* [   \t]+|[  \t]*)'#n'est pas, une, et une seule, espace insécable  normale (unbreakable space)


sr.append([r'&nbsp;',r' ',r'remplace entité nbsp par une espace insécable'])
# pour besoin ponctuel                  
sr.append ([r'(?<=....http|...&nbsp|&PRODUCT|&PREVVER|&PRODVER|.....ftp)[   ]+([:;])',r'\1',r"pour corriger une introduction intempestive d'espaces"])
sr.append([r'([\w»)])(?<![&PRODUCT|&PREVVER|&PRODVER])([  ]*)([?!;])',r'\1 \3',r'place une espace fine insécable avant une ponctuation double sauf (:) (élimine les autres espaces)']) 

#le lookahead évite de trop s'arrêter sur des choses comme 23:67  ou 3:4:5 la règle est volontairement imparfaite pour ne par rater des cas valables
sr.append([r'([\w»)])'+n1usp+'(:)(?!//|\d\d|\d:)',r'\1 \3',r'place une espace  insécable avant  (:) (élimine les autres espaces)']) 

sr.append([r'([\w»)])([   ]+)([.,])',r'\1\3',r'élimine les espaces avant les ponctuations simples'])

sr.append([r'\.\.\.',r'…',r'remplace trois points par le caractère point de suspension'])

sr.append([r'(etc\.\.\.)',r'etc.',r'etc. et non pas etc...'])

sr.append([r'(etc…)',r'etc.',r'etc. et non pas etc…'])

sr.append ([r'([   ]+)(-)(?!-)',r'\2',r"aucune espace devant un trait d'union"])# le lookahead élimine le cas des options (ex: --help)

sr.append([r'(-)([   ]+)',r'\1',r"aucune espace après un trait d'union"])

sr.append([r'(\w)'+n1sp+'(–)',r'\1 \3',r'place une espace  sécable avant un tiret semi-cadratin'])#

# à revoir cas du début de ligne
sr.append([r'(–)'+n1sp+'(\w)',r'\1 \3',r'place une espace sécable après un tiret semi-cadratin'])

#les règles suivantes doivent s'appliquer dans cet ordre
sr.append([r'(«)'+n1usp+'(\w)',r'\1 \3',r'place une espace  insécable après un guillement ouvrant (élimine les autres espaces)'])
sr.append([r'(\w)'+n1usp+'(»)',r'\1 \3',r'place une espace  insécable avant un guillement fermant (élimine les autres espaces)'])
sr.append([r'([?.!])([   ]*)(»)([   ]*\.)',r'\1 \3',r"la chaîne [.?!] ». est incorrecte. Remplacer avec ([.?!] ») ? Sinon utiliser c|C pour changer "])

#sr.append([r'(\w)'+n1usp+'(—)',r'\1 \3',r'place une espace sécable avant un tiret cadratin '])

#sr.append([r'(—)'+n1usp+'(\w)',r'\1 \3',r'place une espace  sécable après un tiret cadratin'])

# pénalisant nombreux cas d'exception : à retravailler
#sr.append([r'(?<!<|>)(/)'+n1fusp+'(\w)',r'\1 \3',r'place une espace fine insécable après une barre de fraction  (élimine les autres espaces)'])

#sr.append([r'([^\W<])'+n1fusp+'(/)',r'\1 \3',r'place une espace fine insécable avant une barre de fraction (élimine les autres espaces)'])

sr.append([r'(\()([   ]+)(\w)',r'\1\3',r'élime toute espace  entre une parenthèse ouvrante et le texte']) 

sr.append([r'(\w)([   ]+)(\))',r'\1\3',r'élimine toute espace entre une parenthèse fermante et le texte inclus'])

sr.append([r'(\[)([   ]+)(\w)',r'\1\3',r'élime toute espace entre un crochet ouvrant et le texte']) 

sr.append([r'(\w)([  ]+)(\])',r'\1\3',r'élimine toute espace entre un crochet fermant et le texte inclus'])

sr.append([r'(\w)'+n1sp+'(\()(?!\))',r'\1 \3',r'insère une espace sécable avant une parenthèse ouvrante (remplace les espaces insécables)'])
# les cas où il s'agit d'une fonction sans paramètres est exclus

#on exclut ci-dessous le cas des ponctuations
sr.append([r'(\))'+n1sp+'([^\W.;,!?:])',r'\1 \3',r'insère une espace sécable après une parenthèse fermante (remplace les espaces insécables)']) 

# les règles qui suivent  doivent rester dans cet ordre
sr.append([r'(MB|MiB)(?= | | )',r'Mio',r'francisation des unités'])#remplacement de MB ou MiB par Mio si suivi d'une espace
sr.append([r'(\d+)'+n1fusp+r'([kio|Mio|Gio|Tio])',r'\1 \3',r"insère une espace fine insécable entre un nombre et l'unité (remplace les autres espaces)"])

#Règles relatives à l'écriture des nombres (à voir: trop simpliste)
#sr.append([r'(\d+)'+n1fusp+r'(\d{3})',r'\1 \3',r'le séparateur des milliers doit être une espace fine insécable'])



