# po_purifier
A phyton script to review typography in .po files 
(only French language at the moment but you can replace the typorules.py file 
with a file containing rules for your own language.)

The script parses the language (at the moment fr) directory open each files in 
turn and suggest changes to the translated messages the user can accept or 
refuse. 
Changes are suggested according to typographic rules defined in a sepate 
configuration file named typorules.py.

To get more information on how to use this program just use the following 
command:

python3 po_typo_purifier.py -i


