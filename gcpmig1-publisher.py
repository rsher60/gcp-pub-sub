import os
from google.cloud import pubsub_v1
import requests
import json
import datetime
import time
from urllib.request import urlopen as uReq
import xml.etree.ElementTree as ET


credential_path = "C:\\Users\\rsher\\OneDrive\\Desktop\\fog-computing-1989965d0de1.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
project_id = "fog-computing-239019"
topic_name = "mig1"

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_name}`
topic_path = publisher.topic_path(project_id, topic_name)

 #main body of the code -- original commit on 9/17/2019


url ="https://smstestbed.nist.gov/vds/current"
web = uReq(url)

page = web.read()
web.close()

tree = ET.fromstring(page)
root = tree.getchildren()
streams = root[1].getchildren()

# Main Function
def get_data(stream):
    start_time = time.time()
    
    main = list()
    
    for child in stream:
        
        machine = child.attrib['name']
        dc = {"Machine": machine}
        
        for childA in child:
            
            dc_a = dc.copy()
            component = childA.attrib['component'] + ": " + childA.attrib['name']
            dc_a.update({"Division": component})
            
            for childB in childA:
                
                dc_b = dc_a.copy()
                evnt = childB.tag.partition("}")[2]
                dc_b.update({"TypeofEvent": evnt})
                
                for childC in childB:
                    
                    dc_c = dc_b.copy()
                    dc_c.update(childC.attrib)                
                    main.append(dc_c)
                    
    return main


main = get_data(streams)
print(main)



for items in main:
    s=json.dumps(items)
    d = str.encode(s)
    #print(type(s))
    future = publisher.publish(topic_path, d)
    print(future.result())



print(datetime.datetime.now())


print('Published messages.')
