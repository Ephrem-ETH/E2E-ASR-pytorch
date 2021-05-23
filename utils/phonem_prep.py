""" phonemes = []
with open("/home/emekonnen/kaldi/egs/librispeech/s5/data/local/lm/librispeech-lexicon.txt", "r") as f:
    for line in f:
        line = line.split()
        for phn in line[1:]:
            if phn not in phonemes:
            phonemes.append(phn)
   
print()
with open("phones.txt", "w") as fw:
    for phone in phonemes:
        fw.write(phone) """
# function to prepare phonemes from the lexicon file
def prepare_phones(file_path):
    phonemes = []
    count =0
    with open(file_path, "r") as f:
        for line in f:
            line = line.split()
            #for phn in line[1:]:
            if line[0] not in phonemes:
                   phonemes.append(line[0])
    #print(len(phonemes))
    # save the list into dictionary
    phone_dic = {}
    value = 1
    for phone in phonemes:
        #print(phone)
        phone_dic[phone] = value
        value +=1
    phones = " "

    for k in phone_dic:
        key = k
        num = phone_dic[k]
        phones += key + " " + str(num) +"\n"

    with open("/home/emekonnen/mydata/E2E-ASR/mydata/data/local/lm/words.txt","w") as fw:
        fw.write(phones)

# call the function to get executed 
prepare_phones("/home/emekonnen/mydata/E2E-ASR/mydata/data/local/lm/libri_lexicon.txt")


 