#!/usr/bin/env python3

import logging

import json
import csv

import gzip
import urllib.request


regions = [
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "af-south-1",
    "la-south-2",
    "sa-chile-1",
    "na-mexico-1",
    "sa-brazil-1",
    "sa-peru-1",
    "sa-argentina-1",
    "cn-north-1",
    "cn-north-4",
    "cn-east-3",
    "cn-east-2",
    "cn-south-1",
]

services = ["ecs", "bms", "sfs", "evs", "cce", "obs", "vpc", "vpn", "rds", "kms"]

# Sources from https://portal-intl.huaweicloud.com/api/calculator/api/productALLInfo/config?urlPath=ecs&sign=common&language=en-us
ecs_datainfo = {
    "": "",
    "dataInfo_1_": "General computing",
    "dataInfo_2_": "General Network-optimized",
    "dataInfo_3_": "General computing-plus",
    "dataInfo_4_": "General Network Enhancement",
    "dataInfo_5_": "General entry",
    "dataInfo_6_": "Memory-optimized",
    "dataInfo_7_": "Memory Network Enhancement",
    "dataInfo_8_": "Large-memory",
    "dataInfo_9_": "GPU-accelerated",
    "dataInfo_10_": "High-performance computing",
    "dataInfo_11_": "Disk-intensive",
    "dataInfo_12_": "FPGA-accelerated",
    "dataInfo_13_": "Ultra-high I/O",
    "dataInfo_14_": "Dynamic BGP",
    "dataInfo_15_": "Static BGP",
    "dataInfo_16_": "Exclusive",
    "dataInfo_17_": "Shared",
    "dataInfo_18_": "Bandwidth",
    "dataInfo_19_": "Traffic",
    "dataInfo_20_": "ECS with 4 or less vCPUs",
    "dataInfo_21_": "ECS with more than 4 vCPUs",
    "dataInfo_22_": "EVS disks",
    "dataInfo_23_": "Common I/O",
    "dataInfo_24_": "High I/O",
    "dataInfo_25_": "Ultra-high I/O",
    "dataInfo_26_": "Linear calculation",
    "dataInfo_27_": "1 GB",
    "dataInfo_28_": "Shared bandwidth",
    "dataInfo_29_": "By Traffic",
    "dataInfo_30_": "BGP IP",
    "dataInfo_31_": "5 Mbit/s or higher",
    "dataInfo_32_": "x86",
    "dataInfo_33_": "Kunpeng",
    "dataInfo_34_": "Kunpeng general computing-plus",
    "dataInfo_35_": "Kunpeng memory-optimized",
    "dataInfo_36_": "vCPUs",
    "dataInfo_37_": "Windows SQL Server Enterprise",
    "dataInfo_38_": "Windows SQL Server Standard",
    "dataInfo_39_": "Windows SQL Server Web",
    "dataInfo_40_": "Windows SQL Server Express",
    "dataInfo_41_": "AI-accelerated",
    "dataInfo_42_": "Kunpeng ultra-high I/O",
    "calc_1_": "Billing Mode",
    "calc_2_": "Type",
    "calc_3_": "Selected specifications ",
    "calc_4_": "Image",
    "calc_5_": "EIP",
    "calc_6_": "EIP Type",
    "calc_7_": "Bandwidth Type",
    "calc_8_": "Billed By",
    "calc_9_": "Bandwidth",
    "calc_10_": "Traffic",
    "calc_11_": "System Disk",
    "calc_12_": "Data Disk",
    "calc_14_": "Automatically assign",
    "calc_15_": "Not required",
    "calc_16_": "No images available",
    "calc_17_": "Add Data Disk",
    "calc_18_": "You can attach ",
    "calc_19_": " more disks.",
    "calc_20_": "paymentType",
    "calc_21_": "Required Duration",
    "calc_22_": "No Upfront",
    "calc_23_": "Partial Upfront",
    "calc_24_": "All Upfront",
    "calc_25_": "CPU Architecture",
    "calc_26_": "X86 uses Complex Instruction Set Computing (CISC). Kunpeng uses Reduced Instruction Set Computing (RISC).",
    "calc_27_": "If a pay-per-use EIP is bound to an ECS, BMS, load balancer, or NAT gateway, you will not be billed for its retention.",
    "calc_28_": "Exclusive bandwidth: Bandwidth is only used by one EIP.",
    "calc_29_": "ECS",
    "calc_30_": "ECSs",
    "detail_0_": "An ECS can be billed on only a hourly basis.The ECS pricing below includes the cost of CPU, memory, and the associated operating system image.",
    "detail_1_": "An ECS can be billed on a yearly/monthly, pay-per-use, or spot price basis. The ECS pricing below includes the cost of vCPUs and memory in the first two billing modes. For the cost of disks and bandwidth, see pricing details for EVS disk and bandwidth on this page.",
    "detail_2_": "Specifications Price",
    "detail_3_": "Type",
    "detail_4_": "Image",
    "detail_5_": "Type",
    "detail_6_": "vCPUs",
    "detail_7_": "Memory",
    "detail_8_": "Hourly",
    "detail_9_": "Monthly",
    "detail_10_": "1 Year",
    "detail_13_": "Currency",
    "detail_14_": "USD",
    "detail_15_": "Image Price",
    "detail_16_": "Images with Red Hat Linux are charged.",
    "detail_17_": "OS Type",
    "detail_18_": "ECS Specification",
    "detail_21_": "Disk Price",
    "detail_22_": "Billing Item",
    "detail_23_": "Disk Type",
    "detail_24_": "Description",
    "detail_25_": "Increment",
    "detail_26_": "Price per GB",
    "detail_27_": "Bandwidth Price",
    "detail_28_": "By Bandwidth",
    "detail_29_": "Type",
    "detail_30_": "Pricing Tier",
    "detail_31_": "Price per Mbit/s",
    "detail_32_": "Pricing Details",
    "detail_34_": "By Traffic",
    "detail_35_": "Type",
    "detail_36_": "Billed By",
    "detail_37_": "Price",
    "detail_38_": "Price per GB",
    "detail_39_": "IP",
    "detail_40_": "Type",
    "detail_41_": "Price per EIP",
    "detail_45_": "Monthly Usage",
    "detail_46_": "See the pricing specified in your contract",
    "detail_47_": "Pricing Basis (USD)",
    "detail_48_": "RI",
    "detail_49_": "Offering Class",
    "detail_50_": "Special Discount",
    "detail_51_": "",
}


def download_json(regions, service):

    for region in regions:
        api_url = (
            "https://portal-intl.huaweicloud.com/api/calculator/api/productALLInfo?urlPath="
            + service
            + "&region="
            + region
        )
        logging.warn(f"Downloading data from {api_url}")

        request = urllib.request.Request(api_url)
        response = urllib.request.urlopen(request)
        result = gzip.decompress(response.read())
        with open(service + "-pricing_" + region + ".json", "wb") as writer:
            writer.write(result)


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
                    "arch": ecs_datainfo[resourceVM["arch"]],
                    "vmType": ecs_datainfo.get(  # UGLY! Defaults to original value if dictionary convertion fails
                        resourceVM.get("vmType", ""), resourceVM.get("vmType", ""),
                    ),
                    "generationTypeMap": ecs_datainfo.get(  # UGLY! Defaults to original value if dictionary convertion fails
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


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    for service in services:
        download_json(regions, service)

    generate_csv(regions)
