#!/usr/bin/env python3

import json
import csv

import gzip
import urllib.request


region_list = [
    # "ap-southeast-1",
    # "ap-southeast-2",
    # "ap-southeast-3",
    # "af-south-1",
    "la-south-2",
    # "sa-chile-1",
    # "na-mexico-1",
    # "sa-brazil-1",
    # "sa-peru-1",
    # "sa-argentina-1",
    # "cn-north-1",
    # "cn-north-4",
    # "cn-east-3",
    # "cn-east-2",
    # "cn-south-1",
]


def download_json(region):

    api_url = (
        "https://portal-intl.huaweicloud.com/api/calculator/api/productALLInfo?urlPath=ecs&region="
        + region
    )

    request = urllib.request.Request(api_url)
    response = urllib.request.urlopen(request)
    result = gzip.decompress(response.read())
    with open("ecs-pricing_" + region + ".json", "wb") as writer:
        writer.write(result)


def generate_csv(region):
    with open("ecs-pricing_" + region + ".json", "r") as json_file:
        data = json.load(json_file)

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
                "RITime": resourceVM.get("RITime"),
            }
            for plan in resourceVM["planList"]:
                pricing_entry["amountType"] = plan.get("amountType")
                pricing_entry["paymentTypeKey"] = plan.get("paymentTypeKey")
                pricing_entry["productId"] = plan["productId"]
                pricing_entry["amount"] = plan["amount"]

                thewriter.writerow(pricing_entry)


if __name__ == "__main__":
    for region in region_list:
        print(region)
        download_json(region)
        generate_csv(region)
