#!/usr/bin/env python3

import logging

import urllib.request
import gzip

from regions import regions
import ecs
import evs
import eip

services = ["cce", "ecs", "evs", "eip"]



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
            logging.warn(f'Content-Encoding: {response.info().get("Content-Encoding")}')
            if response.info().get("Content-Encoding") == "gzip":
                result = gzip.decompress(response.read())
            elif response.info().get("Content-Encoding") == "deflate":
                result = response.read()
            elif response.info().get("Content-Encoding"):
                logging.error("Encoding type unknown")
            else:
                result = response.read()

            with open(service + "-pricing_" + region + ".json", "wb") as writer:
                writer.write(result)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    download_json(regions, services)
    ecs.generate_csv(regions)
    evs.generate_csv(regions)
    eip.generate_csv(regions)
