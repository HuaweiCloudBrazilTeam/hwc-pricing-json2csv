#!/usr/bin/env python3

import logging

import urllib.request
import gzip

from regions import regions
import ecs

services = ["ecs", "bms", "sfs", "evs", "cce", "obs", "vpc", "vpn", "rds", "kms"]


def download_json(regions, services):
    for region in regions:
        for service in services:
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


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    download_json(regions, services)
    ecs.generate_csv(regions)
