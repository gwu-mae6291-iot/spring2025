# wordtool.py
#
# Needs wordsWithPOS.txt, an edited
# version of the Moby project, using only words from the Unix
# dictionary, about 20,000 words.
#
# Authors: Sam Gassman & Rahul Simha
# July 2020

import random
import re

wordfile = 'wordsWithPOS.txt'

allWords = []
nouns = []
pluralNouns = []
verbs = []
adverbs = []
transVerbs = []
inTransVerbs = []
adjectives = []
conjunctives = []
prepositions = []
pronouns = []
klingon_words = []

__charIdx = 0
__charCopy = None
__f = None
__occurrences = dict()


singlequotelist = [ "‘", "’", "‚", "‛",  "‹", "›", "⍘", "⍞", "❛", "❜",  "❮", "❯" ]
doublequotelist = ["«","»","“", "”", "„", "‟","❝", "❞","〝", "〞", "〟", "＂"]

def classifyWord(word, desc):
    if desc.find('N') >= 0:
        nouns.append(word)
    if desc.find('p') >= 0:
        pluralNouns.append(word)
    if desc.find('V') >= 0:
        verbs.append(word)
    if desc.find('t') >= 0:
        transVerbs.append(word)
    if desc.find('i') >= 0:
        inTransVerbs.append(word)
    if desc.find('v') >= 0:
        adverbs.append(word)
    if desc.find('A') >= 0:
        adjectives.append(word)
    if desc.find('C') >= 0:
        conjunctives.append(word)
    if desc.find('P') >= 0:
        prepositions.append(word)
    if desc.find('r') >= 0:
        pronouns.append(word)

def readWords():
    lines = [line.strip() for line in open(wordfile,'r')]
    for line in lines:
        posIndex = line.index('-')
        pronIndex = line.index('+')
        word = line[0:posIndex].lower()
        if len(word) <= 1:
            continue
        desc = line[posIndex+1:pronIndex]
        pron = line[pronIndex+1:len(line)]
        classifyWord(word, desc)
        ## NOTE: one can add pronunciations here too.
        allWords.append(word)

def get_all_words():
    return allWords

def get_nouns():
    return nouns

def get_plural_nouns():
    return pluralNouns

def get_verbs():
    return verbs

def get_trans_verbs():
    return transVerbs

def get_adverbs():
    return adverbs

def get_adjectives():
    return adjectives

def get_conjunctives():
    return conjunctives

def get_prepositions():
    return prepositions

def get_pronouns():
    return pronouns

def get_klingon_words():
    if len(klingon_words) == 0:
        print('NEED TO IMPLEMENT: klingon words')
        exit(0)
    return klingon_words

def get_random_letter():
    return random.choice(list('abcdefghijklmnopqrstuvwxyz'))

def get_random_word():
    return random.choice(allWords)

def get_random_noun():
    return random.choice(nouns)

def get_random_plural_noun():
    return random.choice(pluralNouns)

def get_random_verb():
    return random.choice(verbs)

def get_random_adverb():
    return random.choice(adverbs)

def get_random_adjective():
    return random.choice(adjectives)

def get_random_conjunctive():
    return random.choice(conjunctives)

def get_random_preposition():
    return random.choice(prepositions)

def get_random_pronoun():
    return random.choice(pronouns)

def open_file_bychar(filename):
    global __charCopy
    global __charIdx
    global __f
    __f = open(filename, 'r', encoding='utf8')
    __charCopy = __f.read()
    for x in singlequotelist:
        __charCopy = __charCopy.replace(x, "'")
    for x in doublequotelist:
        __charCopy = __charCopy.replace(x, '"')
    __charIdx = 0

def open_file_byword(filename):
    open_file_bychar(filename)
    

def open_file_bysentence(filename):
    open_file_bychar(filename)
    
    
def close_file_byword():
    __close_file()
    
def close_file_bychar():
    __close_file()
    
def close_file_bysentence():
    __close_file()
    
def __close_file():
    global __f
    __f.close()
    


def next_char():
    global __charCopy
    global __charIdx
    if(__charCopy == None):
        print("""Please use 'open_file_bychar()' before calling this function
              The required string variable which should hold the file contents
              was empty. The file may also be empty.""")
        exit()
    if(len(__charCopy) > __charIdx):
        toreturn = __charCopy[__charIdx]
        __charIdx+=1
        return toreturn
    else:
        return None


def next_word():
    global __charCopy
    global __charIdx
    if(__charCopy == None):
        print("""Please use 'open_file_byword()' before calling this function
              The required string variable which should hold the file contents
              was empty. The file may also be empty.""")
        exit()
    char = next_char()
    if(char == None):
        return None
    while(not char.isalnum() and not char == '_' and not char == '-' and not char == "'"):
        if(__charIdx == len(__charCopy)):
            return None
        char = next_char()
    
    string = ""
    while(char != None):
        if(not char.isalnum() and not char == '_' and not char == '-' and not char == "'"):
            break
        else:
            string +=char
        char = next_char()
        
    if(string == ""):
        return None
    if(re.match("(\-|_)+", string)):
        return next_word()
    return string
    
        
    
    
def next_sentence():
    global __charCopy
    global __charIdx
    if(__charCopy == None):
        print("""Please use 'open_file_bychar()' before calling this function
              The required string variable which should hold the file contents
              was empty. The file may also be empty.""")
        exit()
    char = next_char()
    string = ""
    #for searching for quotes. canbreak == True means no quotes located
    #canbreak = True
    while(char != None):
        
        #letter is punctuation:
        if((char == '.' or char == '?' or char == ';' or char == '!')):
            string += char
            char = next_char()
            if(char == None):
                return process(string)
            while(char.isspace() or char == '.' or char == '?' or char == ';' or char == '!' or char == '"' or char == ']'):
                string += char
                char=next_char()
                if(char == None):
                    return process(string)
            __charIdx-=1
            break

        #letter is not punctuation (excluding quotes)
        else:
            string +=char
        char = next_char()

    
    if(string == ""):
        return None
    return process(string.strip())



def next_sentence_as_list():
    string = next_sentence()
    if(string == None):
        return None
    string = string.replace('"', "").replace('.','').replace('!','').replace('?','').replace(',','').replace('-','').replace('\n','').strip()
    string =string.split(" ")
    
    return [x for x in string if x]


def get_sentences_from_textfile(filename):
    open_file_bysentence(filename)
    sentences = []
    s = next_sentence()
    while s != None:
        sentences.append(s)
        s = next_sentence()
    return sentences


def process(string):
    if(string.count('"')>0):
        string = string.replace('"',"")
    return string.strip()

        
def make_counter(string):
    if string in __occurrences:
        print("make_counter: String '",string,  "' already has a counter stored. Please call incr_counter('",string,"') or decr_counter('",string,"') instead.", sep="")
        return
    
    
    __occurrences[string] = 1
    
def has_counter(string):
    if string in __occurrences:
        return True
    return False

def incr_counter(string):
    if string in __occurrences:
        __occurrences[string] +=1
        return
    print("incr_counter: String '", string, "' does not have a counter set up yet. Please call make_counter('",string,"') first", sep="")
    
def decr_counter(string):
    if string in __occurrences and __occurrences[string]>0:
        __occurrences[string] -=1
        return True
    elif string in __occurrences and __occurrences[string] == 0:
        return False
    print("decr_counter: String '", string, "' does not have a counter set up yet. Please call make_counter('",string,"') first", sep="")
    

def get_counter(string):
    if string in __occurrences:
        return __occurrences[string]
    print("get_counter: String '", string, "' does not have a counter set up yet. Please call make_counter('",string,"') first", sep="")

def get_counter_strings():
    return list(__occurrences.keys())


readWords()


