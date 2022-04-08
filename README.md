# CPCS Law Databse Parser


### Introduction
This repository contains code to **parse** and **extract** information from public lawsuites of civil complaints against police departments.

### Tech stack
We use OCR, text parsing and machine learning technologies to identify important fields within each lawsuit and provide a simple to read interface that is ready to be read by databases. This enables non-technical individuals to lookup important information without having to manually go through all the files, which can be hundreds of pages of legal proceedings.

The current setup is a data extraction pipeline that is deployed on the **BU Shared Compute Cluster**, and do not feature frontend support (as there is no need for this feature).

### Usage
1. Launch a BU SCC cluster with some sort of GPU capabilities.
2. Download this repo, as git is included by default in all instances.
3. Execute the `init_scc.sh` script, which loads in the nessesary modules and installs any dependencies the Python program requires.
4. Execute `python3 src/main.py` to parse the document information. Output file is stored to `output.csv`.