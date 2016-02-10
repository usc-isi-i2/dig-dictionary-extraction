from nltk.util import ngrams
import singleheap
import json
import sys


def run(dictfile, inputfile, configfile="sampleconfig.json"):
    config = json.loads(open(configfile).read())
    n = config["token_size"]
    threshold = config["threshold"]
    dictfileds = config["dictionary"]["value_attribute"]
    docfileds = config["document"]["value_attribute"]

    inverted_list = {}
    inverted_index = []
    entity_tokennum = {}
    inverted_list_len = {}
    entity_realid = {}
    entity_real = {}
    i = 0
    maxenl = 0
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
            token = str(token)
            try:
                inverted_list[token].append(i)
                inverted_list_len[token] += 1
            except KeyError:
                inverted_list[token] = []
                inverted_list[token].append(i)
                inverted_list_len[token] = 1
        i += 1

    for line in open(inputfile):
        line = json.loads(line)
        documentId = line[config["document"]["id_attribute"]]
        document_real = line[docfileds[0]]
        for filed in docfileds[1:]:
            document_real += " " + line[filed]
            # tokenize document, add inverted list(empty) of new tokens in document
        document = document_real.lower().strip()
        jsonline = {}
        jsonline["document"] = {}
        jsonline["document"]["id"] = documentId
        jsonline["document"]["value"] = document_real
        jsonline["entities"] = {}
        tokens = list(ngrams(document, n))
        heap = []
        keys = []
        los = len(tokens)
        # build the heap
        for i, token in enumerate(tokens):
            key = str(token)
            keys.append(key)
            try:
                heap.append([inverted_list[key][0], i])
            except KeyError:
                pass
        if heap:
            returnValuesFromC = singleheap.getcandidates(heap, entity_tokennum, inverted_list_len, inverted_index,
                                                         inverted_list, keys, los, maxenl, threshold)
            for value in returnValuesFromC:
                temp = {}
                temp["start"] = value[1]
                temp["end"] = value[2]
                temp["score"] = value[3]
                try:
                    jsonline["entities"][entity_realid[value[0]]]["candwins"].append(temp)
                except KeyError:
                    jsonline["entities"][entity_realid[value[0]]] = {}
                    jsonline["entities"][entity_realid[value[0]]]["value"] = entity_real[value[0]]
                    jsonline["entities"][entity_realid[value[0]]]["candwins"] = [temp]
        print json.dumps(jsonline)

def consolerun():
    if len(sys.argv) != 4:
        print len(sys.argv)
        print "Wrong Argv num"
        return 0
    run(sys.argv[1], sys.argv[2], sys.argv[3])