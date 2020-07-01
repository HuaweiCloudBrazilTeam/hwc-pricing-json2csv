import csv
import logging
import json
import datainfo

def generate_csv(regions):
    with open("ecs-pricing.csv", "w", newline="") as csv_file:
        fieldnames = [
            "region",
            "arch",
            "vmType",
            "generationLevel",
            "generation",
            "generationTypeMap",
            "spec",
            "performType",
            "cpu",
            "ram",
            "resourceSpecCode",
            "imageSpec",
            "productId",
            "paymentTypeKey",
            "RITime",
            "amount",
            "amountPerVcpu",
            "amountType",
        ]
        thewriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
        thewriter.writeheader()

        for region in regions:
            logging.warn(f"Writing data for {region} in {csv_file.name}")
            with open("ecs-pricing_" + region + ".json", "r") as json_file:
                data = json.load(json_file)

            for resourceVM in data["product"]["hws.resource.type.vm"]:
                logging.info(f"Found hws.resource.type.vm: {resourceVM['spec']}")
                pricing_entry = {
                    "region": region,
                    "arch": datainfo.ecs[resourceVM["arch"]],
                    "vmType": datainfo.ecs.get(  # UGLY! Defaults to original value if dictionary convertion fails
                        resourceVM.get("vmType", ""), resourceVM.get("vmType", ""),
                    ),
                    "generationTypeMap": datainfo.ecs.get(  # UGLY! Defaults to original value if dictionary convertion fails
                        resourceVM.get("generationTypeMap", ""),
                        resourceVM.get("generationTypeMap", ""),
                    ),
                    "generationLevel": resourceVM["generation"].split(".")[0][-1:],
                    "generation": resourceVM["generation"].lower(),
                    "spec": resourceVM["spec"],
                    "resourceSpecCode": resourceVM["resourceSpecCode"],
                    "imageSpec": resourceVM["imageSpec"],
                    "performType": resourceVM["performType"],
                    "cpu": resourceVM["cpu"].split()[0],
                    "ram": resourceVM["mem"].split()[0],
                    "RITime": resourceVM.get("RITime", "..ONDEMAND")
                    .split(".")[2]
                    .split("_")[0],
                }
                for plan in resourceVM["planList"]:
                    pricing_entry["amountType"] = plan.get("amountType")
                    pricing_entry["paymentTypeKey"] = plan.get("paymentTypeKey")
                    pricing_entry["productId"] = plan["productId"]
                    pricing_entry["amount"] = plan["amount"]
                    pricing_entry["amountPerVcpu"] = round(
                        float(plan["amount"]) / int(resourceVM["cpu"].split()[0]), 4
                    )

                    if (
                        plan.get("billingMode") == "ONDEMAND"
                        or plan.get("amountType")
                        == "framework.node.RILang.perEffectivePrice"
                    ):
                        thewriter.writerow(pricing_entry)
