'''
This is a function used to prepare a lexicon file 
that maps word to a sequence of characters 
 '''
lexicon_dict = {}
def lexicon_dic():
    with open("/home/emekonnen/mydata/E2E-ASR/mydata/data/local/lm/libri_lexicon.txt","r") as f:
            for line in f:
                word = line.split()[0]
                characters = list(word)
                lexicon_dict[word] = characters
    return lexicon_dict
lexicon_dic()
#save the dictionary into text
trans = " "
for k in lexicon_dict:
    key =k
    transcript = lexicon_dict[k]
    #print(transcript)
    trans+=key + " " + " ".join(transcript) + "\n"
with open("lexicon.txt", "w") as wf:
    wf.write(trans)
    




        