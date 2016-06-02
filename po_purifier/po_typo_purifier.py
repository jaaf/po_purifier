#!/usr/bin/python3.4
# coding: utf8 
from os import listdir
from os import mkdir
import re
import gettext 
import textwrap
from subprocess import call
import string
import chardet
import gettext
#-----------------------------------------
#CONFIGURATION PART








import typorules # import typo rules


target_dir = 'purified' # the dir where to place the purified files
locale=typorules.locale
language=typorules.language # the language code used for program localization
debug=False
with_pause = False
rulenum=""
pat = []
cpt_msg="0"
fichier=""
target=""
tr_dir="" # the translation dir, where .po files lay

#Be aware we are speaking of translation of the program hereafter
#fr= gettext.translation('po_typo_purifier', localedir='locale', 
                        # languages=['fr_FR.UTF-8'])
fr= gettext.translation('po_typo_purifier', localedir='locale', 
                         languages=[language])
fr.install()

infoText = _("""

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
""")
dialog_accept=_('y') # accept proposal of change
dialog_change=_('c') # make a prior change
dialog_skip= _('s') # skip this message

class col:
    MAUVE = '\033[95m'
    BLUE = '\033[94m'
    OK= '\033[92m'
    PROMPT= '\033[93m'#yellow
    FAILED = '\033[91m'#red
    END = '\033[0m'# end color
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class bkgcol:
    GREEN = '\033[42m'
    END ='\033[40m'
    SP  ='\033[47m'
    NBSP='\033[46m'
    NNBSP='\033[44m'
    NSP='\033[41m'

#----------------------------------------------------
def colorize_spaces(text,includeNormal):
    #display a legend

    print (_('%s %s non-breakable space') %(bkgcol.NBSP,bkgcol.END))
    print (_('%s %s narrow non-breakable space') % (bkgcol.NNBSP, bkgcol.END))
    print (_('%s %s narrow breakable space') % (bkgcol.NSP, bkgcol.END))
  
    coltext=text
    if includeNormal == True: #for cases where colorizing normal spaces may help
        print (_('%s %s normal space') % (bkgcol.SP, bkgcol.END))  
        coltext=coltext.replace(' ',bkgcol.SP+' '+bkgcol.END)
    coltext=coltext.replace(' ',bkgcol.NBSP+' '+bkgcol.END)
    coltext=coltext.replace(' ',bkgcol.NNBSP+' '+bkgcol.END)
    coltext=coltext.replace(' ',bkgcol.NSP+' '+bkgcol.END)
    print (coltext)

################################################################################
################################################################################

# the purifying function itself: applies regex search and replace defined 
#in typorules.py     
def purify(message, b_first):#b_first = True if it is a first line
    global cpt_msg
    global fichier
    global target
    global dialog_change
    global dialog_accept
    global locale

    # to be able in the end to know if message has been modified        
    memcontent = message 
    content=message
    # we start purification on the concatenated message
    skip_message=False
    for p in pat:    
        if (skip_message == True):
            break # the user asked to skip the message
        try:
           #we execute the search and replace and save the result
           newcontent=p[0].subn(p[1],content,count=1) 
        except :
            if debug == True:
                print (_('%s Error while applying the following rule:%s %s') 
                % (col.FAILED, col.END, P[2]))
                userinput =""
                while userinput !="k":
                   userinput = input (_('k + return pour continuer'))
        # the variable inside which we place the parsed beginning of the line
        preservedcontent =""           
        while newcontent[1]== 1:               
            match= p[0].search(content)
            if  match:
                # a match is found, need to alert 
                #display the message with spaces colorized except normal spaces
                colorize_spaces(content, False)
                sp=match.span()                   
                #colorise the change to be made
                tail=content[sp[1]:]
                colorcontent = content[0:sp[1]]+bkgcol.END+tail
                tail=colorcontent[sp[0]:]
                colorcontent = colorcontent[0:sp[0]]+bkgcol.GREEN+tail
                print ('----------------------------------------------------')
                print  (_('%s Change suggested in message %d of the %s file; \
Rule: %s %s') 
                          % (col.OK, cpt_msg, fichier, p[2], col.END))
                print (colorcontent)
                # ask user confirmation             
                confirm = input(
                              _('%s Do you confirm this change? (\
%s %s %s for yes, %s %s %s for prior change,%s %s %s to skip this message, %s \
any thing else – like return – \
%s for no)%s')
                                % (col.PROMPT, col.FAILED,dialog_accept,
col.PROMPT,col.FAILED,dialog_change,col.PROMPT,col.FAILED,dialog_skip,
col.PROMPT,col.FAILED,col.PROMPT,col.END)) 
                        
                if (confirm == dialog_accept):# or confirm == 'O'):
                   print (_('%sChange accepted %s') %(col.OK,col.END))
                   # we keep the substitution
                   if content == newcontent[0]:
                       #the substitution doesn't change the message, we risk
                       # an infinite loop
                       print ( _('%s Warning: application of the rule doesn\'t \
change the message at all. %s\n') %(col.FAILED,col.END))
                       # to avoid the loop remove the beginning of the message,
                       # preserve it and add to previous preservation
                       preservedcontent += content[0:sp[1]]
                       # we keep only the tail to search on
                       content = content[sp[1]:] 
                   else:
                       content = newcontent[0] # we keep substitution

                elif (confirm == dialog_skip):
                    skip_message = True
                    break # we want to skip this message definitely 

                elif (confirm == dialog_change): 
                    oldcontent = content
                    # rebuild the content including previous substitutions
                    content=preservedcontent+content 
                    print()
                    print ( _(
                           '%s You asked for a prior change into the found  \
matching string %s') % (col.MAUVE, col.END))
                    searchstr = input ( _('%s Please enter the part of the \
maching string to be replaced %s') % (col.PROMPT,col.END))
                    replstr   =input ( _(
                                   '%s Please enter the substitute string %s') 
                                   % (col.PROMPT, col.END))
                    nhead = content[0:sp[0]]
                    ntail = content[sp[1]:]
                    between = content[sp[0]:sp[1]]
                    between = between.replace (searchstr,replstr,1)
                    print ( _('%s New content %s') % (col.MAUVE, col.END))
                    content = nhead+between+ntail
                    if content == oldcontent: #the change was effectless
                        print (_('%sNothing can be changed! Please try again.%s')
                                 %(col.FAILED, col.END))
                        input (_('%s Press any key to continue%s')
                                 % (col.PROMPT, col.END))
                        
                    else: 
                        print (content)
                        undo = input ( _('%s Do you confirm this prior change? \
(%s %s %s for yes, %s anything else %s for no)%s') 
                                  %(col.PROMPT, col.FAILED,dialog_accept, 
                                    col.PROMPT,col.FAILED,col.PROMPT,col.END))
                    
                        if undo == dialog_accept:
                            print  ( _('%s change confirmed %s') 
                                       % (col.OK,col.END))
                        else: 
                            content = oldcontent #we undo the  prior change 

                    newcontent=p[0].subn(p[1],content,count=1)
                    continue # we restart the substitution trial
                                                 
                else:
                    #the user refuses the change: remove the beginning of 
                    #the message, preserve it and add to previous preservation
                    print ( _('%s change discarded %s') % (col.OK, col.END))
                    preservedcontent += content[0:sp[1]]
                    content = content[sp[1]:]#we keep only the tail to search on
            else:
                # normally we should never pass here
                print ('Breaking the loop! How strange!')
                break                 
            #continue search in the remaining part of the message                                      
            newcontent=p[0].subn(p[1],content,count=1)
                
        # rebuild modified full content for next rule application
        content = preservedcontent+content
    if (b_first == False) :                 
        wrp= textwrap.TextWrapper(width=80,break_long_words=False,
                              replace_whitespace=False, drop_whitespace=False)
        lineList=wrp.wrap(content)
    #we write the splitted message to target
           
        modified = memcontent != content
    #print info for messages with no matches and messages with discarded matches 
        if not modified:
            print ( _('%s body of message %d of %s file, not changed %s') 
                      %(col.OK,cpt_msg,fichier,col.END))
        else:
            print ( _('%s body of message %d of %s file has been changed as \
follows: %s')
                       %(col.OK,cpt_msg, fichier, col.END))
            for element in lineList:
                print(col.BLUE+'"'+element+'"'+col.END)     
            if with_pause == True:
                input (_('%s Press any key to continue%s')
                                 % (col.PROMPT, col.END))

        for element in lineList:     
            target.write('"'+element+'"\n')
           
   
        target.write('\n')  
    
    else:
        modified = memcontent != content
        if not modified:
            print ( _('%s first line of message %d of %s file, not changed %s') 
                      %(col.OK,cpt_msg,fichier,col.END))
        else:
            print ( _('%s first line of message %d of %s file has been changed \
as follows: %s')
                       %(col.OK,cpt_msg, fichier, col.END)) 
            print (col.BLUE+ 'msgstr "'+content+'"'+col.END)
            if with_pause == True:
                print (col.FAILED+'this is a first line'+col.END)
                input (_('%s Press any key to continue%s')
                                 % (col.PROMPT, col.END))
        target.write('msgstr "'+content+'"')
        target.write('\n')  

def usage():
   print (_("""po_typo_purifier.py [OPTIONS]
   OPTIONS:
      -h --help : display this help 
      -i --info : give info about how the program works
      -o --one-only =<rule num> : apply only this rule (not used at the moment)
      -t --trans-dir=<trans-dir> : indicate translation directory  
      -d --debug : execute program in debug mode
      -p : mark a pause after a change in a message
   """))

###############################################################################
###############################################################################
def main(argv):  
    global cpt_msg  
    global rulenum
    global debug   
    global fichier  
    global target  
    global infoText    
    global tr_dir 
    global with_pause
    global locale
    
    tr_dir=locale         
                     
    try:                                
        opts, args = getopt.getopt(argv, "hiot:dp", ["help", "info", "one-only=",
                                         "trans-dir="]) 
    except getopt.GetoptError:           
        usage()                          
        sys.exit(2)  
     
    for opt, arg in opts:                
        if opt in ("-h", "--help"):      
            usage()                     
            sys.exit()  
  
        elif opt in ("-i", "--info--"):
            print (infoText)
            sys.exit()
             
        elif opt == '-d':                                         
            debug = True   
               
        elif opt in ("-o", "--one-only"): 
            rulenum = arg  

        elif opt in ("-t", "--trans-dir"):
            tr_dir= arg 
            print ('tr_dir juste au début'+tr_dir)

        elif opt == ("-p"):
            with_pause = True                        
           
    print ('debug = '+str(debug))
    print ('rulenum = ' +str(rulenum))
    re.LOCALE


    mkdir ('../'+target_dir)
    print (col.END) # force reinitialize color

    # create the compiled pattern objects
    # pat[n][0] the compiled pattern, pat[n][1] the replacement string,
    # pat[n][1] the type of replacement  
    for elem in typorules.sr:
        if debug==True:    
            #print ('Compilation des règles à appliquer: '+elem[2])
            print ( _('Compiling typo rule: %s') % (elem[2]))

        pat.append([re.compile(elem[0]),elem[1], elem[2]])

        if debug==True:    
            print ( _('The rule has been compiled') )
                          

    for fichier in listdir('../'+tr_dir+'/'):
        cpt_msg=0
        print ('Nouveau message,la trans dir est : '+tr_dir)
        print ('../'+tr_dir+'/'+fichier,'r')
        source=open('../'+tr_dir+'/'+fichier,'r')
        target=open('../'+target_dir+'/'+fichier,'a')
        intro=True # brute copy of lines while still in introduction
        # brute copy of lines while searching for the next translated part
        findMessage = True 
        messageFirst = ""

        for line in source:
   
            if intro:
                if  line.startswith('msgstr'):
                    # intro is considered over when
                    cpt_msg+=1 
                    intro = False
                target.write(line)
                continue
    
            if line.startswith('msgstr'):
                findMessage = False

            if findMessage:
                target.write(line)
                continue
    
            # we have found a new translated message and are going 
            # to concatenate the lines -first is treated specifically
            if line.startswith('msgstr'):
                cpt_msg+=1
                pos = line.index('"')
                # we keep what is inside double quotes only (may be empty)
                messageFirst = line[pos+1:-2] 
                messageBody = "" # we reinitialize the body of the message
                continue

            if line.startswith('"'): # we are still in the body of the message
                pos=line.index('"')
                # we concatenate the body lines except double quotes & linefeed
                messageBody = messageBody + line[pos+1:-2] 
                continue
            else:
                #we are no longer in the message body
                findMessage = True # reset the search for a new message
                #target.write('msgstr "'+messageFirst+'"\n')
                purify(messageFirst, True)
                purify(messageBody,False)# include the writting of the message

        #we should not forget the last message
        #target.write('msgstr "'+messageFirst+'"\n')
        purify(messageFirst, True)
        purify(messageBody,False)# include the writting of the message

        source.close()
        target.close()
    
if __name__ == "__main__":
    import sys, getopt
    main(sys.argv[1:])
  
  
