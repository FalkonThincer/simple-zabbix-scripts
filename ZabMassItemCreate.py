import requests
import json
import os
from customModules.ZabAuth import GetAuthKey

url = 'https://some-zab-serv.local/zabbix/api_jsonrpc.php'
certPath = os.path.dirname(os.path.realpath(__file__)) + '/files/SomeCert.crt'
authKey = GetAuthKey(url,certPath)

zabItemsFilePath = os.path.dirname(os.path.realpath(__file__)) + '/files/ZabItems.json'
with open(zabItemsFilePath) as zabItemsFile:
    zabItemsDict = json.load(zabItemsFile)

for host in zabItemsDict:
    hostID = host["hostID"]
    for item in host["items"]:
        zabItemCreateData = '{"jsonrpc":"2.0","method":"item.create","auth":"' + authKey + '","id":1,"params":{"hostid":"'+ hostID +'",'
        for itemParam in item["params"].keys():
            zabItemCreateData = zabItemCreateData + '"' + itemParam + '":"' + item["params"][itemParam] + '",'
        zabItemCreateData = zabItemCreateData + '"preprocessing": [{'
        for itemPreprocessingParam in item["preprocessing"].keys():
            zabItemCreateData = zabItemCreateData + '"' + itemPreprocessingParam + '":"' + str(item["preprocessing"][itemPreprocessingParam]) + '",'
        zabItemCreateData = zabItemCreateData.removesuffix(',') 
        zabItemCreateData = zabItemCreateData + '}]}}'
        zabItemCreateReq = requests.post(url, headers = {"Content-Type": "application/json-rpc"}, data = zabItemCreateData, verify=certPath).json()
        try:
            print(zabItemCreateReq['result'])
        except:
            print("Tne next request incorrect: " + zabItemCreateReq)
