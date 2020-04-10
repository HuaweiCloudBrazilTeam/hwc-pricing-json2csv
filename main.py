#!/usr/bin/env python3

import json

# from urllib.request import urlopen
# import gzip
# api_url = "https://portal-intl.huaweicloud.com/api/calculator/api/productALLInfo?urlPath=ecs&region=sa-brazil-1"
# with urlopen(api_url) as response:
#     source = gzip.decompress(response.read())
# data = json.loads(source)

with open('ecs-pricing.json') as f:
    data = json.load(f)

print(type(data))
print(data)
