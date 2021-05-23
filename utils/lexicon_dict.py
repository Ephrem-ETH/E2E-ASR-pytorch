import json
lexicon = {}
with open("lexicon.txt",'r') as f:
    line = f.split()
    key = line[1:]
    value = line[0]
    lexicon[tuple(key)] = value
with open("lexicon_data.json",'W', encoding = 'utf-8') as f:
    json.dumps(lexicon_data, lexicon, ensure_ascii=False, indent = 4)

