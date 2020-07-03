import csv
import logging
import json


def generate_csv(regions):
    with open("evs-pricing.csv", "w", newline="") as csv_file:
        fieldnames = [
            "region",
            "productId",
            "resourceSpecCode",
            "volumeType",
            "iops",
            "amount",
        ]
        thewriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
        thewriter.writeheader()

        for region in regions:
            logging.warn(f"Writing EVS pricing data in {csv_file.name} for {region}")
            with open("evs-pricing_" + region + ".json", "r") as json_file:
                data = json.load(json_file)

            for resourceEVS in data["product"]["hws.resource.type.volume"]:
                logging.info(f"Found hws.resource.type.volume: {resourceEVS['spec']}")
                pricing_entry = {
                    "region": region,
                    "resourceSpecCode": resourceEVS["resourceSpecCode"],
                    "volumeType": resourceEVS["volumeType"],
                    "iops": resourceEVS.get("iops"),
                }
                for plan in resourceEVS["planList"]:
                    pricing_entry["productId"] = plan["productId"]
                    pricing_entry["amount"] = f'{plan["amount"]:.6f}'

                    thewriter.writerow(pricing_entry)
