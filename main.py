#!/usr/bin/env python3

import json
import csv

# from urllib.request import urlopen
# import gzip
# api_url = "https://portal-intl.huaweicloud.com/api/calculator/api/productALLInfo?urlPath=ecs&region=sa-brazil-1"
# with urlopen(api_url) as response:
#     source = gzip.decompress(response.read())
# data = json.loads(source)

with open("ecs-pricing.json") as json_file:
    data = json.load(json_file)

region = "sa-brazil-1"

with open("ecs-pricing.csv", "w", newline="") as csv_file:
    fieldnames = [
        "region",
        "generation",
        "spec",
        "specSize",
        "performType",
        "cpu",
        "ram",
        "resourceSpecCode",
        "image",
        "imageSpec",
        "chargeMode",
        "productId",
        "planListLength",
        "paymentTypeKey",
        "RITime",
        "amountType",
        "amount",
    ]
    thewriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
    thewriter.writeheader()

    for resourceVM in data["product"]["hws.resource.type.vm"]:
        pricing_entry = {
            "region": region,
            "generation": resourceVM["generation"].lower(),
            "spec": resourceVM["spec"],
            "specSize": resourceVM["spec"].split(".", 1)[1],
            "resourceSpecCode": resourceVM["resourceSpecCode"],
            "image": resourceVM["image"],
            "imageSpec": resourceVM["imageSpec"],
            "performType": resourceVM["performType"],
            "cpu": resourceVM["cpu"].split()[0],
            "ram": resourceVM["mem"].split()[0],
            "planListLength": len(resourceVM["planList"]),
            "chargeMode": resourceVM["chargeMode"][0],
            "RITime" : resourceVM.get("RITime")
        }
        for plan in resourceVM["planList"]:
            pricing_entry["amountType"] = plan.get("amountType")
            pricing_entry["paymentTypeKey"] = plan.get("paymentTypeKey")
            pricing_entry["productId"] = plan["productId"]
            pricing_entry["amount"] = plan["amount"]

            thewriter.writerow(pricing_entry)
