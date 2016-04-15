from nltk.util import ngrams
import singleheap
import json
import sys


def readDict(dictfile,config):
    inverted_list = {}
    inverted_index = []
    entity_tokennum = {}
    inverted_list_len = {}
    entity_realid = {}
    entity_real = {}
    maxenl = 0
    dictfileds = config["dictionary"]["value_attribute"]
    n = config["token_size"]

    i = 0
    for line in open(dictfile):
        line = json.loads(line)
        entity_realid[i] = line[config["dictionary"]["id_attribute"]]
        entity_real[i] = line[dictfileds[0]]
        for filed in dictfileds[1:]:
            entity_real[i] += " " + line[filed]
        entity = entity_real[i].lower().strip()
        inverted_index.append(entity)  # record each entity and its id
        tokens = list(ngrams(entity, n))
        entity_tokennum[entity] = len(tokens)  # record each entity's token number
        if maxenl < len(tokens):
            maxenl = len(tokens)
        # build inverted lists for tokens
        tokens = list(set(tokens))
        for token in tokens:
            token_n = "".join(token)
            try:
                inverted_list[token_n].append(i)
                inverted_list_len[token_n] += 1
            except KeyError:
                inverted_list[token_n] = []
                inverted_list[token_n].append(i)
                inverted_list_len[token_n] = 1
        i += 1
    return inverted_list,inverted_index,entity_tokennum,inverted_list_len,entity_realid,entity_real,maxenl

def get_tokens(entity, n):
    return ngrams(entity, n)

def processDoc(line,dicts,config=json.loads(open("sampleconfig.json") .read())):
    inverted_list = dicts[0]
    inverted_index = dicts[1]
    entity_tokennum = dicts[2]
    inverted_list_len = dicts[3]
    entity_realid = dicts[4]
    entity_real = dicts[5]
    maxenl = dicts[6]

    threshold = config["threshold"]
    docfileds = config["document"]["value_attribute"]
    n = config["token_size"]

    documentId = line[config["document"]["id_attribute"]]
    document_real = line[docfileds[0]]
    for filed in docfileds[1:]:
        document_real += " " + line[filed]

    jsonline = {}
    document = document_real.lower().strip()
    tokens = list(ngrams(document, n))
    heap = []
    keys = []
    los = len(tokens)
    # build the heap
    for i, token in enumerate(tokens):
        key = "".join(token)
        keys.append(key)
        try:
            heap.append([inverted_list[key][0], i])
        except KeyError:
            pass
    if heap:
            returnValuesFromC = singleheap.getcandidates(heap, entity_tokennum, inverted_list_len, inverted_index,
                                                             inverted_list, keys, los, maxenl, threshold)
            jsonline["document"] = {}
            jsonline["document"]["id"] = documentId
            jsonline["document"]["value"] = document_real
            jsonline["entities"] = {}
            for value in returnValuesFromC:

                temp = {}
                temp["start"] = value[1]
                temp["end"] = value[2]
                temp["score"] = value[3]
                value_o = str(value[0])
                try:
                    jsonline["entities"][entity_realid[value_o]]["candwins"].append(temp)
                except KeyError:
                    try:
                        entity_id = entity_realid[value_o]
                    except KeyError:
                        value_o = value[0]
                        entity_id = entity_realid[value_o]
                    jsonline["entities"][entity_id] = {}
                    jsonline["entities"][entity_id]["value"] = entity_real[value_o]
                    jsonline["entities"][entity_id]["candwins"] = [temp]
    else:
        print 'heap is empty'
        print document_real

    return jsonline

def readDictlist(dictlist,n):
    inverted_list = {}
    inverted_index = []
    entity_tokennum = {}
    inverted_list_len = {}
    entity_realid = {}
    entity_real = {}
    maxenl = 0


    i = 0
    for line in dictlist:
        print dictlist[line]["name"]
        names = []
        if type(dictlist[line]["name"]) == list:
            names = dictlist[line]["name"]
        else:
            names.append(dictlist[line]["name"])

        print names
        for name in names:
            entity_realid[i] = line
            entity_real[i] = name
            entity = entity_real[i].lower().strip().replace(" ","")
            inverted_index.append(entity)  # record each entity and its id
            tokens = list(ngrams(entity, n))
            entity_tokennum[entity] = len(tokens)  # record each entity's token number
            if maxenl < len(tokens):
                maxenl = len(tokens)
            # build inverted lists for tokens
            tokens = list(set(tokens))
            for token in tokens:
                token_n = "".join(token)
                try:
                    inverted_list[token_n].append(i)
                    inverted_list_len[token_n] += 1
                except KeyError:
                    inverted_list[token_n] = []
                    inverted_list[token_n].append(i)
                    inverted_list_len[token_n] = 1
            i += 1
    return [inverted_list, inverted_index, entity_tokennum, inverted_list_len, entity_realid, entity_real, maxenl]

def run(dictfile, inputfile, configfile):
    config = json.loads(open(configfile) .read())
    dicts = readDict(dictfile,config)
    for line in open(inputfile):
        line = json.loads(line)
        print processDoc(line,dicts,config)

def consolerun():
    if len(sys.argv) == 4:
        run(sys.argv[1], sys.argv[2], sys.argv[3]) 
    else:
        print "Wrong Arguments Number"
        sys.exit()
# run("sampledictionary.json","sampledocuments.json","sampleconfig.json")