#!/usr/bin/env python3

import json
import csv

# from urllib.request import urlopen
# import gzip
# api_url = "https://portal-intl.huaweicloud.com/api/calculator/api/productALLInfo?urlPath=ecs&region=sa-brazil-1"
# with urlopen(api_url) as response:
#     source = gzip.decompress(response.read())
# data = json.loads(source)

with open('ecs-pricing.json') as json_file:
    data = json.load(json_file)

region = 'sa-brazil-1'

with open('ecs-pricing.csv', 'w', newline='') as csv_file:
    fieldnames = [
        'region',
        'spec',
        'cpu',
        'ram',
        'resourceSpecCode',
        'image',
        'imageSpec',
        'chargeMode',
        'productId',
        'planListLength',
        'amount'
        ]
    thewriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
    thewriter.writeheader()
    
    
    for resourceVM in data['product']['hws.resource.type.vm']:
        thewriter.writerow({
            'region' : region,
            'spec' : resourceVM['spec'],
            'resourceSpecCode' : resourceVM['resourceSpecCode'],
            'image' : resourceVM['image'],
            'imageSpec' : resourceVM['imageSpec'],            
            'cpu' : resourceVM['cpu'],
            'ram' : resourceVM['mem'],
            'chargeMode' : resourceVM['chargeMode'][0],
            'planListLength' : len(resourceVM['planList']),
            'productId' : resourceVM['planList'][0]['productId'],
            'amount' : resourceVM['planList'][0]['amount']
            })