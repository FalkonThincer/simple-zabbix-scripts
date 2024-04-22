import sys
from requests import post
from getpass import getpass

def GetAuthKey(url,certPath):
    ZabUsername = input("Enter username for zabbix authentication: ")
    ZabPassword = getpass("Enter password for zabbix user "+ ZabUsername + ": ")
    ZabAuthData = '{"jsonrpc":"2.0","method":"user.login","params":{"username":"'+ ZabUsername +'","password":"' + ZabPassword + '"},"id":1}'
    ZabAuthReq = post(url, headers = {"Content-Type": "application/json-rpc"}, data = ZabAuthData, verify = certPath).json()
    try:
        AuthKey = ZabAuthReq['result']
    except:
        print("Password or login incorrect, the script stopped")
        sys.exit()
    return AuthKey