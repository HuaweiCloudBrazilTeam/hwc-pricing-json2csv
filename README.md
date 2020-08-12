# Huawei Cloud Pricing: JSON to CSV convertion tool

This Python script does the following tasks:
1. Downloads the respective JSON pricing data from each Region and Service combination in HuaweiCloud, saving in the current folder
1. Processes the set of JSON files for each Service, generating an CSV file including Pricing information from all Regions

The end result is a set of CSV files that can be more easily used for Price Analysis in tools such as MS Excel.

All the consumed APIs are public and don't require authentication. The Pricing information is the same as readily available at Huawei Cloud Pricing Calculator.

All the ECS pricing information is expressed as USD/Hour, even in the Reserved Instances purchase model.

One way to facilitate the usage of the generated CSVs is to upload them to a public OBS bucket, and use the URL to import them back in Excel. That way, you can share the analysis spreadsheet without breaking the update mechanism.

## Requirements

The script was developed and manually tested in Ubuntu 18.04 with Python 3.6.9

* Python 3 without additional dependencies


## Running the tool


```bash
./main.py
```

The progress of download and convertion steps will be shown in the console as logging output.


