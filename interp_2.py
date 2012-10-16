"""
python drocta ~ATH interpreter
It interprets things written in drocta ~ATH
and is written in python.
Really, I thought the name was fairly self explanatory.
Build number:7
"""

import bif
import re
import pdb


def bifurcate(valueA,valueB=False):
    if(valueB):
        return bif.unbifurcate(valueA, valueB)
    else:
        return bif.bifurcate(valueA)

##def matchParens(text,start,openStr,closeStr):
##    count=1
##    start=start+1
##    searchChar=text.find(openStr,start)
##    while(count>0):
##        nextOpen=text.find(openStr,searchChar)
##        nextClose=text.find(closeStr,searchChar)
##        if(nextClose==-1):
##            return searchChar
##        if(nextOpen==-1):
##            nextOpen=nextClose+1
##        if(nextClose<=nextOpen):
##            count-=1
##            searchChar=nextClose+1
##            #print "close"
##        else:#nextClose>nextOpen
##            count+=1
##            searchChar=nextOpen+1
##            #print "open"+str(count)+"searchChar:"+str(searchChar)
##    return searchChar

def matchParens(text,start,openStr,closeStr):
    count=0
    charNum=start
    firstChar=True
    while(count>0 or firstChar):
        if(charNum>=len(text)):
            #print "err:could not find match!"
            return -1
        elif(text[charNum]==closeStr):
            count=count-1
            #print "close at "+str(charNum)
        elif(text[charNum]==openStr):
            count=count+1
            #print "open at "+str(charNum)
            if(firstChar):
                firstChar=False
        charNum=charNum+1
    return charNum-1

def textToNextSemicolon(text,start=0):
    semicolonOffset=text.find(';',start)
    return text[start:semicolonOffset]

charObjs={}
def getCharObj(theChar):
    if(theChar in charObjs):
        return charObjs[theChar]
    else:
        theCharObj=bif.value_obj()
        charObjs[theChar]=theCharObj
        return theCharObj
def getStrObj(theStr):
    if(len(theStr)==0):
        return NULL_obj
    else:
        return bifurcate(getCharObj(theStr[0]),getStrObj(theStr[1:]))



ATHVars={}
THIS=bif.value_obj()
ATHVars['THIS']=THIS
NULL_obj=bif.value_obj()
NULL_obj.DIE()
ATHVars['NULL']=NULL_obj
filename=raw_input()
filelink=open(filename,'r')
script=filelink.read(-1)

"""
lines=script.explode("\n")
lineCount=len(lines)
lineNum=0
"""

charNum=0

execStack=[]

while(THIS.living):
    if(False):
        pass
    elif(script.startswith('import ',charNum)):
        semicolonOffset=script[charNum:].index(';')
        importStatementStr=script[charNum:charNum+semicolonOffset]
        importStatementList=importStatementStr.split(' ')
        if(importStatementList[-1] not in ATHVars):
            ATHVars[importStatementList[-1]]=bif.value_obj()
        charNum+=semicolonOffset
    elif(script.startswith('~ATH(',charNum)):
        closeparenOffset=script[charNum:].index(')')
        loopVar=script[charNum+5:charNum+closeparenOffset]
        loopVar=loopVar.strip(' \t\n\r')
        #print "reached ~ATH command, loopVar is "+loopVar
        if(loopVar in ATHVars):
            if(ATHVars[loopVar].living):
                execStack.append((charNum,'{'))
                charNum+=closeparenOffset
                #print "loop on "+loopVar
            else:
                #print "parenmatch jump from "+str(charNum)
                charNum=matchParens(script,charNum,'{','}')+2
                #print "parenmatch jumped to char:"+str(charNum)+" which was"+script[charNum]
                #print "loopVar was "+loopVar
        else:
            print('warning/error: \"{0}\" is undefined'.format(loopVar))
    elif(script.startswith('}',charNum)):
        openingTuple=execStack.pop()
        if(openingTuple[1]=='{'):
            charNum=openingTuple[0]
        else:
            print('what are you trying to do? \"(...}\" error')
    elif(script.startswith('print ',charNum)):
        #print "print..."
        semicolonOffset=script[charNum:].index(';')
        print(script[charNum+6:charNum+semicolonOffset])
        charNum+=semicolonOffset#+6
    elif(script.startswith('INPUT',charNum)):
        semicolonOffset=script[charNum:].index(';')
        varname=script[charNum+6:charNum+semicolonOffset]
        print 'INPUT varname was "'+varname+'"'
        ATHVars[varname]=getStrObj(raw_input(':'))
        charNum+=semicolonOffset
    elif(script.startswith('BIFURCATE ',charNum)):
        charNum+=10
        semicolonOffset=script[charNum:].index(';')
        openSquareOffset=script[charNum:].index('[')
        closeSquareOffset=script[charNum:].index(']')
        commaOffset=script[charNum:].index(',')
        syntacticallyCorrect=True
        for offset in [openSquareOffset,closeSquareOffset,commaOffset]:
            if((offset==-1) or (offset>semicolonOffset)):
                print("Bifurcate command malformed, char:"+str(charNum))
                syntacticallyCorrect=False
                break
        if(syntacticallyCorrect):
            if(openSquareOffset==0):
                leftHalf=script[charNum+openSquareOffset+1:charNum+commaOffset]
                rightHalf=script[charNum+commaOffset+1:charNum+closeSquareOffset]
                combinedName=script[charNum+closeSquareOffset+1:charNum+semicolonOffset]
                ATHVars[combinedName]=bifurcate(ATHVars[leftHalf],ATHVars[rightHalf])
            else:
                toSplitName=script[charNum:charNum+openSquareOffset]
                leftHalf=script[charNum+openSquareOffset+1:charNum+commaOffset]
                rightHalf=script[charNum+commaOffset+1:charNum+closeSquareOffset]
                (ATHVars[leftHalf],ATHVars[rightHalf])=bifurcate(ATHVars[toSplitName])
    elif(re.match(r'([a-zA-Z]+)\.DIE\(\);',script[charNum:])!=None):#script[charNum:script[charNum:].find(';')].endswith('.DIE()')):
        varname=re.match(r'([a-zA-Z]+)\.DIE\(\);',script[charNum:]).group(1)
        #print "found .DIE(); statement! Variable name is "+varname
##        varname=textToNextSemicolon(script,charNum)#script[charNum:script[charNum:].find(';')]
##        varname=varname[:-6]
##        varname=varname.split(' ')[-1]
##        varname=varname.split('\n')[-1]
        ATHVars[varname].DIE()
        charNum=script.find(';',charNum)
        #print varname+"killed"
    elif(script.startswith('DEBUG',charNum)):
        pdb.set_trace()
        charNum+=5
    else:
         charNum+=1
         if(charNum > len(script)):
             THIS.DIE()
    #print script[charNum]
raw_input("press enter to close")             
         
         
        
            
        
        
        
        
