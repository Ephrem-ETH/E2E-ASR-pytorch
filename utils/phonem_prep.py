import argparse

parser = argparse.ArgumentParser(description="retrieve unique phones or characters from the lexicon")
parser.add_argument('--path', type=str, default='',help="path to the lexicon file")

args = parser.parse_args()
# function to prepare phonemes from the lexicon file
def prepare_phones(file_path):
    phonemes = []
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

    with open(args.path + "/phones.txt","w") as fw:
        fw.write(phones)

# call the function to get executed 
prepare_phones(args.path + "/libri_lexicon.txt")


 