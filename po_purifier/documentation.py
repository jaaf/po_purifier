#!/usr/bin/python
# coding: utf8 
infoText = _("""
Le dossier contenant le programme (typo_purifier) doit être placé à coté du 
dossier qui contient les traductions (fichier .po) . Le plus souvent il 
s'agit du dossier <locale> où<locale> représente votre locale (p. ex. fr, ou 
fr_FR.UTF-8). Parfois il s'agit d'un dossier appelé "locale". 
S

Les règles de typographie sont dans le fichier typorules.py dans le même
dossier que le programme.
(Pour le moment les règles sont très approximatives car elles détectent beaucoup
de faux positifs, à cause du mélange texte normal + texte informatique)

On lance le programme depuis ce dossier par la commande suivante :

  python3 po_typo_purifier.py

Sans option, le programme recherche les traduction dans votre dossier <locale>.
La valeur de <locale> correspond à celle que retourne la commande 'echo $LANG'.

Si les traductions se trouvent dans un autre dossier et que vous ne voulez pas
le renommer d'après votre locale, vous pouvez l'indiquer au programme avec l'option 
-t (--trans-dir), p. ex. : 

 pyton3 po_typo_purifier.py -t "locale/pot"

Un dossier "purified" (ce nom est placé dans la variable "target") est crée à 
côté du dossier 'typo_purifier'. C'est lui qui reçoit les nouveaux fichiers.
Il faudra qu'il remplace le dossier initial des traductions si tout s'est bien
passé. 
Le dossier d'origine  quant à lui n'est pas touché mais devra soit être déplacé, 
soit être supprimé, soit être renommé avant le push sur zanata.

NOTE IMPORTANTE: il est prudent de le sauvegarder au préalable car si quelque chose 
se passe mal lors du push sur Zanata, on aura toujours l'original

Le programme établit la liste des fichiers présents dans le dossier des traductions.
Pour chacun des fichiers, il passe en revue les messages. Les messages en 
anglais sont recopiés ligne pour ligne dans le fichier target/<nom_du_fichier>

Les lignes des messages en français sont d'abord agglutinées pour former une 
chaîne unique, puis les règles de substitution lui sont appliquées une à une.
Compte tenu de la variété des cas, et de la très forte possibilité de faux positifs,
toutes les modifications demande une confirmation de l'utilisateur. 

Le message est d'abord affiché avec les espaces, autres que normales, colorisées.
Puis le message est réaffiché avec seulement la modification suggérée 
surlignée en vert. 

L'utilisateur dispose de plusieurs choix :
  — o oui : accepte la modification telle que proposée. Dans ce cas le texte écrit dans 
   le fichier target est affiché (couleur bleu pâle) avec le découpage en ligne utilisé  

  — c changer: dans ce cas l'utilisateur peut effectuer un changement dans la chaîne 
   trouvée et reprendre.
   Cela est intéressant par exemple, si un trait d'union a été utilisé à la place 
   d'un tiret semi-cadration (celui qui joue le rôle de parenthèse) et que la règle 
   du trait d'union est de supprimer les espaces devant et derrière. Remplacer le 
   trait d'union par un tiret semi-cadratin dans ce cas, permet de ne pas supprimer
   les espaces et de faire la correction des tirets du même coup.


  — Toute autre chose : refuse la modification. 

Une fois le message corrigé (ou pas), il est recomposé en lignes de 80 caractères maximum. 
Les lignes sont ensuite écrites dans le fichier cible.

Puis on passe au message suivant, jusqu'à épuiser le fichier avant de passer au suivant.

""")
