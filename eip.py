import csv
import logging
import json


def generate_csv(regions):
    with open("eip-pricing.csv", "w", newline="") as csv_file:
        fieldnames = [
            "region",
            "productId",
            "resourceType",
            "billingEvent",
            "resourceSpecCode",
            "amount",
        ]
        thewriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
        thewriter.writeheader()

        for region in regions:
            logging.warn(f"Writing EIP pricing data in {csv_file.name} for {region}")
            with open("eip-pricing_" + region + ".json", "r") as json_file:
                data = json.load(json_file)

            for resourceEIP in data["product"]["hws.resource.type.ip"]:
                logging.info(
                    f"Found hws.resource.type.ip: {resourceEIP['resourceSpecCode']}"
                )
                for plan in resourceEIP["planList"]:
                    pricing_entry = {}
                    pricing_entry["region"] = region
                    pricing_entry["resourceType"] = resourceEIP["resourceType"]
                    pricing_entry["resourceSpecCode"] = resourceEIP["resourceSpecCode"]
                    pricing_entry["productId"] = plan["productId"]
                    pricing_entry["billingEvent"] = plan["billingEvent"]
                    pricing_entry["amount"] = f'{plan["amount"]:.4f}'

                    if plan.get("billingMode") == "ONDEMAND":
                        thewriter.writerow(pricing_entry)

            for resourceBW in data["product"]["hws.resource.type.bandwidth"]:
                logging.info(
                    f"Found hws.resource.type.bandwidth: {resourceEIP['resourceSpecCode']}"
                )
                for plan in resourceBW["planList"]:
                    if plan["billingEvent"] == "event.type.bandwidthupflow":
                        pricing_entry = {}
                        pricing_entry["region"] = region
                        pricing_entry["resourceType"] = resourceBW["resourceType"]
                        pricing_entry["resourceSpecCode"] = resourceBW[
                            "resourceSpecCode"
                        ]
                        pricing_entry["productId"] = plan["productId"]
                        pricing_entry["billingEvent"] = plan["billingEvent"]
                        pricing_entry[
                            "amount"
                        ] = f'{plan["divisionList"][0]["amount"]:.4f}'

                        if plan.get("billingMode") == "ONDEMAND":
                            thewriter.writerow(pricing_entry)
