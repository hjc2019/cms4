import json
def returnResult(code,msg,data=""):
    returndata={
        "code": code,
        "msg": msg,
        "data": data
    }
    returndata1=json.dumps(returndata)
    return returndata1