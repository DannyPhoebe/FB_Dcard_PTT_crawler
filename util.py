from Dcard_config import header,default_len,forum,until
from numpy import argmax


def lencheck(api_res):
    if api_res[-1]['createdAt'][0:10]>=until:
        return default_len
    else:        
        return argmax(list(map(lambda x:x['createdAt'][0:10]<until,api_res)))

def page_load(url,end = default_len):
    res = requests.get(url,headers=header)
    return  json.loads(res.text)[0:end]