'''
This is a function used to prepare a lexicon file 
that maps word to a sequence of characters 
 '''
import argparse
parser = argparse.ArgumentParser(description="Transform word transcriptions to a sequence of characters with '>' at the end of each word")
parser.add_argument('--path', type=str, default='',help="path to the original lexicon file")

args = parser.parse_args()
lexicon_dict = {}
def lexicon_dic():
    with open(args.path + "/lexicon.txt","r") as f:
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
with open(args.path + "/m_lexicon.txt", "w") as wf:
    wf.write(trans)
    




        