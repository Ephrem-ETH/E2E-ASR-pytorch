#To prepare word map 
def phone_map_prep(file_path):
    word_map = " "
    with open(file_path, "r") as f:
        for line in f:
            line = line.split()
            word_map += str(line[0]) + " " + str(line[0]) + " " + str(line[0]) + "\n"
    return word_map
word_mapp = phone_map_prep("/home/emekonnen/mydata/E2E-ASR/mydata/data/local/lm/libri_lexicon.txt")

with open("/home/emekonnen/mydata/E2E-ASR/mydata/conf/word.200000.map","w") as f:
    f.write(word_mapp)