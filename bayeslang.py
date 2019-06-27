import re
import collections
import os
import io

path = input()
bayespath = input()

# path = "C:\\Users\\pajse\\Desktop\\public\\set\\1\\corpus"
# bayespath = "C:\\Users\\pajse\\Desktop\\public\\set\\1\\sequences.txt"

os.chdir(path)

def normalize(probs):
    if sum(probs)!=0:
        prob_factor = 1 / sum(probs)
        return [prob_factor * p for p in probs]
    else:
        return[0 for p in probs]

languages = os.listdir(path)
languages.sort()

#files
languages_dirs = []
for x in languages:
    languages_dirs.append(os.path.join(path, x))

language_map = []
maps = []
counters=[]
for path in languages_dirs:
    cnt=0
    digram_map = {}
    lang = path[-2:]

    files = []
    for root, dirs, filenames in os.walk(path, topdown=False):
        for name in filenames:
            files.append(os.path.join(root, name))

    digram_map[lang] = collections.Counter()

    for filepath in files:
        cnt+=1
        f = io.open(filepath,'r',encoding = 'utf8')
        for line in f:
            words = re.findall(r'(?=([^\n^\r]{2}))', line.lower())
            digram_map[lang].update(words)

        f.close()
    listica = sorted(dict(digram_map[lang]).items(),key=lambda kv: (-kv[1], kv[0]))
    for i in range(5):
        print(lang+","+ str(listica[i][0]) + ',' + str(listica[i][1]))

    maps.append(digram_map)

    counters.append(cnt)


probmap = {}
for x in maps:
    cnt = 0.
    c = list(x.values())[0]
    lang = list(x.keys())[0]
    
    probmap[lang] = {}
    alloccurances = sum(c.values())
    uniquenum = len(c)
    for k,v in c.items():
        temp=v/(alloccurances+0)
        probmap[lang].update({k:temp})
        
    

f = io.open(bayespath,'r',encoding = 'utf8')
for line in f:
    words = re.findall(r'(?=([^\n^\r]{2}))', line.lower())
    i=0
    probs = []
    langs=[]

    for lang,x in probmap.items():
        textfileprob = counters[i]/sum(counters)
        prob = textfileprob
        for bigram in words:
            if bigram in x:
                prob*=x[bigram]
                
            else:
                prob*=0.
        i+=1

        probs.append(prob)
        langs.append(lang)

    probs = normalize(probs)
    for j in range(i):
        print(langs[j] + ',' + str(probs[j]))