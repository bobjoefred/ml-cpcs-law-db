# CPCS Law Database Parser


### Introduction
This repository contains code to **parse** and **extract** information from public lawsuits of civil complaints against police departments.

### Tech stack
We use OCR, text parsing and machine learning technologies to identify important fields within each lawsuit and provide a simple to read interface that is ready to be read by databases. This enables non-technical individuals to lookup important information without having to manually go through all the files, which can be hundreds of pages of legal proceedings.

The current setup is a data extraction pipeline that is deployed on the **BU Shared Compute Cluster**, and do not feature frontend support (as there is no need for this feature).

We use two machine learning models to extract important information from the lawsuits.

1. Google Pegasus
2. Facebook Bart MNLI large

### Usage locally
1. Ensure that Python is installed and it's version is at least 3.8.10
2. Run the `load_env.sh` script to install all the dependencies, or run `pip3 install -r requirements.txt` to install all the dependencies.
3. Place any lawsuit to extract within the `input` folder. Please name the folders as the lawsuit name.
4. Navigate to the src folder, and run the `python3 main.py` command.
5. An output csv file should be produced at the root of the project.

### Known issues
- The settlement amount field is missing. See issue #32 for more details.