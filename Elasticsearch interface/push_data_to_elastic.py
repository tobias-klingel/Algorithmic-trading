from elasticsearch import Elasticsearch
from datetime import datetime

#Connect to the elastic
es=Elasticsearch([{'host':'XXX.XXX.XXX.XXX','port':9200}])


################################################################################################
#Create document

#Puts all the data togehter and sends it to elastic
def createAndSaveDocument(periode, usedTicksSet, initialCash, finalValue, profit, index, docType):
    backtesting = {
        'usedTicksSet': usedTicksSet,
        'initialCash': initialCash,
        'finalValue': finalValue,
        'profit': profit,
        'periode': periode,
        'buyDecisions': buyDecisions,
        'sellDecisions': sellDecisions,
        'timestamp': datetime.now(),
    }
    result = appendDataInElastic(index=index,docType=docType, document=backtesting)


################################################################################################
#Add data
def appendDataInElastic(index, docType, document):
    res = es.index(index=index, doc_type=docType, body=document)
    print(res['result'])
    return res['result']

def sendDataToElastic(index, docType, body, id):
    res = es.index(index=index, doc_type=docType, id=id, body=body)
    return res['result']
    return res['result']

###############################################################
#Get Data
def getDataFromElastic():
    res = es.get(index="test-index", doc_type='backtest', id=1)
    print(res['_source'])
    return res['_source']

###############################################################
#Search data
def searchOnElastic(index):
    es.indices.refresh(index=index)
    res = es.search(index=index, body={"query": {"match_all": {}}})
    print("Found %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
    return res['hits']['hits']

################################################################################################
#Call functions

#result = (searchOnElastic(index="test-index"))
#print(result)
#print(appendDataInElastic(index="test-index",docType='tweet', body=documentExample))