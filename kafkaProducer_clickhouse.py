import json
import datetime
import numpy as np
import sys
import time
from kafka import KafkaProducer
from collections import OrderedDict

producer = KafkaProducer(bootstrap_servers = ['localhost:9092'],value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def genDict(): 
    randList = np.random.dirichlet(np.ones(5),size=1)[0]
    maxList = [0]*5
    maxInd = np.argmin(randList)
    maxList[maxInd] = 1
    today = datetime.datetime.now()
    time = today.strftime("%Y-%m-%d %H:%M:%S")
    
    maxList.insert(0, str(time))
    
    events = ["time", "sports", "crime", "covid", "Business", "Political"]
    eventDict = dict(zip(events, maxList))
    # print(eventDict)
    # time.sleep(1)
    return eventDict




while True:
    response = genDict()
    producer.send('testPK', value = response)
    print(response)
    time.sleep(1)