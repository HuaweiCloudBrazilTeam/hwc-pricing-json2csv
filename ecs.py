import csv
import logging
import json
import datainfo


def generate_csv(regions):
    with open("ecs-pricing.csv", "w", newline="") as csv_file:
        fieldnames = [
            "region",
            "productId",
            "RITime",
            "arch",
            "vmType",
            "generationLevel",
            "generation",
            "generationTypeMap",
            "resourceSpecCode",
            "spec",
            "imageSpec",
            "cpu",
            "ram",
            "amount",
            "amountPerVcpu",
        ]
        thewriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
        thewriter.writeheader()

        for region in regions:
            logging.warn(f"Writing ECS pricing data in {csv_file.name} for {region}")
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
                    # FIXME: generationLevel should be just the numerical digit, but method below doesn't work with composite generations (eg: c3ne)
                    "generationLevel": resourceVM["generation"].split(".")[0][-1:],
                    "generation": resourceVM["generation"].lower(),
                    "spec": resourceVM["spec"],
                    "resourceSpecCode": resourceVM["resourceSpecCode"],
                    "imageSpec": resourceVM["imageSpec"],
                    "cpu": resourceVM["cpu"].split()[0],
                    "ram": resourceVM["mem"].split()[0],
                    "RITime": resourceVM.get("RITime", "..ONDEMAND")
                    .split(".")[2]
                    .split("_")[0],  # Replacing empty RITime with "ONDEMAND",
                }
                for plan in resourceVM["planList"]:
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
