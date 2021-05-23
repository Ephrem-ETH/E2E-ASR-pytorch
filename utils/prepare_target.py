
# This program takes the word transcrption and transforms to sequence of characters
#  by adding addional character (">") at the end of each word
#  in the coorsponding transcription of each utterence


from utils.word_to_characters import lexicon_dic
final_target = {}
def replace_word_by_letters(file_path):
    lexicon_dict = lexicon_dic()
    with open(file_path,"r") as rf:
        for line in rf:
            line = line.split()
            final_target[line[0]]= " ".join([" ".join(lexicon_dict[word]) + " " + ">" if lexicon_dict.get(word) is not None else '' for word in line[1:] ])
            

replace_word_by_letters("/home/emekonnen/mydata/amharic_data/AMHARIC/data/train/text")
trans = " "
# save the dictionary into text file for later use
for k in final_target:
    key = k
    transcript = final_target[k]
    trans += key + " " + transcript + "\n"

with open("/home/emekonnen/mydata/amharic_data/AMHARIC/data/train_text","w") as wf:
    wf.write(trans);
