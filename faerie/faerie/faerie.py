from nltk.util import ngrams
import singleheap
import json
import sys
import os
import sys
import re
import json



os.environ['PYSPARK_PYTHON'] = "python2.7"
os.environ['PYSPARK_DRIVER_PYTHON'] = "python2.7"
os.environ['SPARK_HOME'] = "/Users/karma/Documents/spark-1.6.0/"
os.environ['_JAVA_OPTIONS'] =  "-Xmx12288m"
sys.path.append("/Users/karma/Documents/spark-1.6.0/python/")
sys.path.append("/Users/karma/Documents/spark-1.6.0/python/lib/py4j-0.9-src.zip")

try:
    from pyspark import SparkContext
    from pyspark import SQLContext
    from pyspark import SparkConf
    from pyspark.sql import Row



except ImportError as e:
    print ("Error importing Spark Modules", e)
    sys.exit(1)

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
            token = str(token)
            try:
                inverted_list[token].append(i)
                inverted_list_len[token] += 1
            except KeyError:
                inverted_list[token] = []
                inverted_list[token].append(i)
                inverted_list_len[token] = 1
        i += 1
    return inverted_list,inverted_index,entity_tokennum,inverted_list_len,entity_realid,entity_real,maxenl

def processDoc(line,config,dicts,runtype):
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

    if runtype == 1:
        line = json.loads(line)
    documentId = line[config["document"]["id_attribute"]]
    document_real = line[docfileds[0]]
    for filed in docfileds[1:]:
        document_real += " " + line[filed]

    document = document_real.lower().strip()
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
        if runtype == 2: 
            jsent = []
            for value in returnValuesFromC:
                temp = Row(id=entity_realid[value[0]],value=entity_real[value[0]],start=value[1],end=value[2],score=value[3])
                jsent.append(temp)
            jsdoc = Row(id=documentId,value=document_real)
            jsonline = Row(document=jsdoc,entities=jsent)
            return jsonline
            
        else:
            jsonline = {}
            jsonline["document"] = {}
            jsonline["document"]["id"] = documentId
            jsonline["document"]["value"] = document_real
            jsonline["entities"] = {}
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

def run(dictfile, inputfile, configfile):
    config = json.loads(open(configfile) .read())
    dicts = readDict(dictfile,config)
    for line in open(inputfile):
        processDoc(line,config,dicts,1)

def runOnSpark(dictfile, inputfile, configfile,runtype):
    config = json.loads(open(configfile).read())
    dicts = readDict(dictfile,config)
    sc = SparkContext(appName="DIG-DICEX")
    if runtype == 1:
        sqlContext = SQLContext(sc)
        lines = sqlContext.read.json(inputfile)
    else:
        lines = inputfile
    sc.broadcast(dicts)
    sc.broadcast(config)
    candidates = lines.map(lambda line : processDoc(line,config,dicts,2))
    candidates.saveAsTextFile("test")
    sc.stop()
    return candidates

def consolerun():
    if sys.argv[1].startswith('-') and len(sys.argv) == 5:
        option = sys.argv[1][1:]  
        if option == "spark":
            runOnSpark(sys.argv[2], sys.argv[3], sys.argv[4],1)
        elif option == 'text':
            run(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print 'Unknown option.' 
            sys.exit()  
    else:
        print "Wrong Arguments Number"
        sys.exit()  
# runOnSpark("sampledictionary.json","sampledocuments.json","sampleconfig.json",1)