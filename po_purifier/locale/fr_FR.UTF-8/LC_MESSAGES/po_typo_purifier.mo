��            )   �      �    �     �  =   �  �   �  U   �  0   �       @     (   `     �  J   �  B   �  @   6  0   w     �     �  F   �  6        T  -   i     �     �  "   �     �          '  �  A     �  �  �  �  �     �+  I   �+  �   	,  }   �,  )   P-     z-  J   �-  *   �-  2   .  M   9.  W   �.  I   �.  1   )/     [/     v/  T   �/  <   �/     #0  =   =0     {0     �0     �0  ,   �0     �0     1  �  51     3                                                 	          
                                                                               

po_typo_purifier : A script to detect typo errors (and more ) in translated 
files.

USAGE:  popurifier.py [OPTIONS]
   
   OPTIONS:
      -h --help : display help 
      -i --info : give the present info about how the program works
      -o --one-only =<rule num> : apply only this rule (not used at the moment)
      -t --trans-dir=<trans-dir> : indicate translation directory  
      -d --debug : execute program in debug mode
      -p : mark a pause after a change in a message
   

The folder that contains the program must be placed aside the folder containing 
the translations (.po files) or its parents. Most often, it is a folder named
after your locale e.g. fr, or fr_FR.UTF-8. 
Sometimes it is a folder named "locale"

The typographic rules lay in the typorules.py file in the same folder as 
the program.

The folder structure looks like the following:
 
     --- --po_purifier ----- po_typo_purifier (prog)
        |               |
        |               |--- typorules.py 
        |
   this |-- [locale] --- pot (.po files)
        |
    or  |-- <your locale> (.po files)
        |
    or  |-- anything  -- anything (.po files)

The program can be launched from the typo_purifier folder with the following
 command :

     python3 po_typo_purifier.py
 
Without any option, the program search for translation files (.po) in the 
<locale> folder, where <locale> is you locale 
(output by the 'echo $LANG' command). 

Whenever translated files (.po) are located elsewhere, use the 

     -t (--trans-dir) option 

to tell the program where to find them, e.g.:"

      python3 po_typo_purifier.py --trans-dir "locale/pot"

A folder, named "purified" (this name is placed in the target variable) is 
created aside the "po_purifier" folder. It receives the new files. You need to 
use this folder to replace the initial translation folder, if  everything went 
well.The original folder, should be renamed or moved before pushing onto zanata.

IMPORTANT NOTE: you should always make a backup of the original folder to 
be able to recover from something wrong happening while pushing onto zanata.

The program establishes the list of the files that lay into the translation 
folder. For each of them it reviews all the messages. The source messages (EN) 
are copied line for line into the target file.

The lines of the translated messages are concatenated to form a unique string, 
then rules are applied in turn. Taking into account the possibility 
of a lot of false positives, all the modifications need a confirmation from the 
user.

The message is displayed, first with colorized spaces, then with proposed
change over a green background.

The user has several choices:

     - y for yes: to accept the proposed change. In this case the message that 
     will be written in the target file is displayed (light blue color) with the 
     splitting in line used.

     -c for change: to ask for a prior change into the rule matching string and 
     the resume. This may be useful in certain circumstances such as a short 
     dash used in place of a long dash that plays the role of parenthesis and 
     to prevent rule from deleting spaces before and after.
     Changing the short dash with a long dash in this case, allows to keep the 
     spaces and to  correct the fault in one shot.

     - s to skip the message. This is useful when the message contains command 
     output  or command with many options that cannot be considered as target 
     language text and that triggers a lot of artificial typographic faults

     - anything else: to refuse the proposal.

Once the message has been corrected (or not), it is split in 80 char lines 
anew. Then the lines are written in the target file.

After that, the program passes to the next message until it reaches the end 
of the file and passes to the next file.
 %s %s normal space %s Change suggested in message %d of the %s file; Rule: %s %s %s Do you confirm this change? (%s %s %s for yes, %s %s %s for prior change,%s %s %s to skip this message, %s any thing else – like return – %s for no)%s %s Do you confirm this prior change? (%s %s %s for yes, %s anything else %s for no)%s %s Error while applying the following rule:%s %s %s New content %s %s Please enter the part of the maching string to be replaced %s %s Please enter the substitute string %s %s Press any key to continue%s %s Warning: application of the rule doesn't change the message at all. %s
 %s You asked for a prior change into the found  matching string %s %s body of message %d of %s file has been changed as follows: %s %s body of message %d of %s file, not changed %s %s change confirmed %s %s change discarded %s %s first line of message %d of %s file has been changed as follows: %s %s first line of message %d of %s file, not changed %s %sChange accepted %s %sNothing can be changed! Please try again.%s %s %s non-breakable space %s %s narrow breakable space %s %s narrow non-breakable space Compiling typo rule: %s The rule has been compiled k + return pour continuer po_typo_purifier.py [OPTIONS]
   OPTIONS:
      -h --help : display this help 
      -i --info : give info about how the program works
      -o --one-only =<rule num> : apply only this rule (not used at the moment)
      -t --trans-dir=<trans-dir> : indicate translation directory  
      -d --debug : execute program in debug mode
      -p : mark a pause after a change in a message
    y Project-Id-Version: po_typo_purifier
POT-Creation-Date: 2016-06-02 06:53+0200
PO-Revision-Date: 2016-06-02 07:06+0200
Last-Translator: José Fournier <jaaf64@zoraldia.com>
Language-Team: 
Language: fr
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Generated-By: pygettext.py 1.5
X-Generator: Poedit 1.8.7.1
Plural-Forms: nplurals=2; plural=(n > 1);
X-Poedit-SourceCharset: UTF-8
X-Poedit-Basepath: ../../..
X-Poedit-SearchPath-0: po_typo_purifier.pot
 

po_typo_purifier : un script pour détecter les erreurs typographiques (et plus
encore) dans les fichiers traduits. 

USAGE:  popurifier.py [OPTIONS]
   
   OPTIONS:
      -h --help : affiche l'aide 
      -i --info : affiche le présent texte sur la manière dont le programme 
                  fonctionne.
      -o --one-only =<rule num> : applique seulement cette règle (Hors service)
      -t --trans-dir=<trans-dir> : précise le dossier des traductions.  
      -d --debug : exécute le programme en mode débogage
      -p : marque une pause lorsqu'un message a été changé et demande 
           une relance de l'opérateur.


Le dossier « typo_purifier » contenant le programme doit être placé à coté 
du dossier qui contient les traductions (fichier .po) . Le plus souvent il 
s'agit du dossier <locale> où<locale> représente votre locale (p. ex. fr, 
ou fr_FR.UTF-8). Parfois il s'agit d'un dossier appelé \"locale\". 

Les règles de typographie sont dans le fichier typorules.py dans le même
dossier que le programme.
(Pour le moment les règles sont très approximatives car elles détectent 
"beaucoup de faux positifs, à cause du mélange texte normal + texte informatique)

  La structure des dossiers ressemble à ceci :
 
     --- --po_purifier ----- po_typo_purifier (prog)
        |               |
        |               |--- typorules.py 
        |
     ça |-- [locale] --- pot (.po files)
        |
     ou |-- <your locale> (.po files)
        |
     ou |-- anything  -- anything (.po files)


On lance le programme depuis ce dossier par la commande suivante :

 python3 po_typo_purifier.py

Sans option, le programme recherche les traduction dans votre dossier "<locale>"

La valeur de <locale> correspond à celle que retourne la commande 'echo $LANG'.

Si les traductions se trouvent dans un autre dossier et que vous ne voulez pas
le renommer d'après votre locale, vous pouvez l'indiquer au programme avec 
l'option  -t (--trans-dir), p. ex. : 

      pyton3 po_typo_purifier.py -t \"locale/pot

Un dossier \"purified\" (ce nom est placé dans la variable \"target\") est créé
 à côté du dossier 'typo_purifier'. C'est lui qui reçoit les nouveaux fichiers.
Il faudra qu'il remplace le dossier initial des traductions si tout s'est bien 
passé. Le dossier initial devra être renommé ou déplacé avant le push sur zanata.

NOTE IMPORTANTE: il est prudent de le sauvegarder au préalable car si quelque 
chose se passe mal lors du push sur Zanata, on aura toujours l'original.

Le programme établit la liste des fichiers présents dans le dossier des 
traductions.
Pour chacun des fichiers, il passe en revue les messages. Les messages en 
anglais sont recopiés ligne pour ligne dans le fichier "target/<nom_du_fichier>"

Les lignes des messages en français sont d'abord agglutinées pour former 
une chaîne unique, puis les règles de substitution lui sont appliquées une à une.
Compte tenu de la variété des cas, et de la très forte possibilité de faux 
positifs, toutes les modifications demande une confirmation de l'utilisateur. 

Le message est d'abord affiché avec les espaces, autres que normales colorisées.
Puis le message est réaffiché avec seulement la modification suggérée surlignée
 en vert. 

L'utilisateur dispose de plusieurs choix :
    — o oui : accepte la modification telle que proposée. Dans ce cas le texte 
écrit dans le fichier target est affiché (couleur bleu pâle) avec le découpage 
en lignes utilisé  

   — c changer: dans ce cas l'utilisateur peut effectuer un changement dans la 
chaîne trouvée et reprendre.
Cela est intéressant par exemple, si un trait d'union a été utilisé à la place 
d'un tiret semi-cadratin (celui qui joue le rôle de parenthèse) et que la règle
 du trait d'union est de supprimer les espaces devant et derrière. "Remplacer 
le trait d'union par un tiret semi-cadratin dans ce cas, permet de ne pas 
supprimer les espaces et de faire la correction des tirets du même coup.

  – s pour sauter le message. Cela est utile lorsqu'il s'agit d'une sortie de 
  commande ou d'une commande avec des tas d'options et qui n'est pas un
  véritable texte dans la langue cible. Cela évite des détections sur des fautes 
  typographiques artificielles.

  — Toute autre chose : refuse la modification.  
Une fois le message corrigé (ou pas), il est recomposé en lignes de 
80 caractères maximum.
Les lignes sont ensuite écrites dans le fichier cible.
Puis on passe au message suivant, jusqu'à épuiser le fichier avant de passer 
au suivant.
 %s %s espace normale %s Changement proposé dans le message  %d du fichier %s; Règle: %s %s %s Acceptez-vous ce changement ? (%s %s %s pour oui, %s %s %s pour un changement préalable,%s %s %s pour sauter ce message, %s toute  autre chose – un simple Entrée par exemple – %s pour non)%s %s Confirmez-vous ce changement préalable ? (%s %s %s pour oui, %s toute autre chose – comme Entrée –  %s pour non)%s %s Erreur lors de l'application de :%s %s %s Nouveau contenu %s %s Saisissez la partie de la chaîne trouvée que vous voulez remplacer %s %s Saisissez la chaîne de remplacement %s %s Pressez une touche quelconque pour continuer.%s %s Attention ! L'application de la règle n'a pas modifié le message. %s
 %s Vous avez demandé à effectuer un changement préalable dans la chaîne trouvée %s %s le corps du message %d du fichier %s a été modifié comme suit : %s %scorps du message  %d du fichier %s inchangé %s %s changement confirmé %s %s changement abandonné%s %s la première ligne du message %d du fichier %s a été modifiée comme suit : %s %s première ligne du message %d du fichier %s inchangée %s %s Changement accepté %s %sAucun changement n'a pu être opéré ! Essayer encore.%s %s %s espace insécable %s %s espace fine sécable %s %s espace fine insécable Compilation de la règle typographique : %s La règle a été compilée k + Entrée pour poursuivre po_typo_purifier.py [OPTIONS]
   OPTIONS:
      -h --help : pour afficher cette aide 
      -i --info : pour des explications sur le fonctionnement du programme
      -o --one-only =<rule num> : n'utiliser que cette seule règle (pas encore en service)
      -t --trans-dir=<trans-dir> : précise le dossier des traductions depuis l'emplacement du programme  
      -d --debug : exécute le programme en mode debug
      -p : marque une pause après la modification d'un message
    o 