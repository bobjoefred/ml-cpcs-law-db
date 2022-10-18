# Project Outline for CPCS team

## _Yile Wang,  Aditya Pal, Ryan Hom, Wenhan Zhou  2022-October-5 v0.0.1-dev_

## Overview

CPCS is a state criminal justice agency that provides legal representation to indigent people for cases in which people have a constitutional or statutory right to counsel.  Our practice areas include public defense, juvenile delinquency, mental health commitments, and child/family law.

CPCS team is creating a standardized, statewide database of law enforcement misconduct and are seeking support for various components of the project.  The database already includes or will include a variety of data and records pertaining to law enforcement misconduct, including: civil suits, criminal cases, internal affairs investigations, traffic citations, Brady notices, search warrants, and media articles.

The final output will be several CSV or Excel spreadsheets matching the existing dataset (linked previously). 

1. Situation and current issues
	The existing project is trained to read lawsuits, specifically those filed against the MA police department. While the use case is similar (OCR), the specific application is different and will require model retraining at the very least. The dataset appears clean, but more pruning may be required to improve accuracy. Exploring new models if required.
2. Key Questions
What are the trends, patterns, and practices in law enforcement misconduct?
Which officers are involved, how often, and what are they doing?
What are the most common types of police misconduct that result in a lawsuit?
Which officers, units, or departments are most often subject to lawsuits?

3. Hypothesis: Overview of how it could be done
	Start by using the existing model and retraining it on the new dataset
	Reprune data if achieving poor accuracy
	Modify or entirely rewrite/change model for both accuracy and efficiency
4. Impact
For our client, they can better keep track and store police force related information like officers’ names and corresponding records. For the whole society, the public can get a chance to visualize police force related data more easily and extract more meaningful conclusions.


### A. Problem Statement: 

The goal of this project is to further improve upon the OCR architecture and extract key data fields from the ‘Brady notices’ dataset provided by the client. The extracted data needs to be standardized into a CSV format and should be easy to integrate into the CPCS database.


### B. Checklist for project completion


OCR Source Code
CSV file of extracted data that is standardized and can be integrated into client’s database.
The final deliverable CSV file should have the following fields-
Officer Name, Officer ID, Docket Number, Internal Investigation Number, Court, Department, etc.


### C. Provide a solution in terms of human actions to confirm if the task is within the scope of automation through AI. 


Open/Look at document
Read document and manually find and type the required information into a spreadsheet
Add any additional information that’s requested (such as attached files etc) 


### D. Outline a path to operationalization.

_Data Science Projects should have an operationalized end point in mind from the onset. Briefly describe how you see the tool
 produced by this project being used by the end user beyond a jupyter notebook or proof of concept. If possible, be specific and
 call out the relevant technologies_


Using OCR to extract key data from 'Brady notices' 
Standardizing the data into a format and file type that can be easily integrated into our database. 
The OCR will be deployed on BU Shared Computing Cluster and will be accessible for further extraction of datasets in the future.



## Resources

[Github link from last semester](https://drive.google.com/drive/folders/16RRbVDCfQVsVaPO2ziyq9P8vNa9SFthv)


### Data Sets


[Public Dataset 1 given by the Client](https://drive.google.com/open?id=1CSn0elzrWwjNfizDeEX2YxvQ6SN_IdBt)

[Public Dataset 2 given by the Client](https://drive.google.com/open?id=1CSn0elzrWwjNfizDeEX2YxvQ6SN_IdBt)



### References

[Lecture note 1 from Professors](https://drive.google.com/file/d/1zgT9zNjHc_1lCIG42XApGlgroMNv0ZW3/view)

[Lecture note 2 from Professors](https://docs.google.com/presentation/d/18Gxgi1ITVS6T-FU5RVQ463NQfA1b04tMZLd6XNPTKDk/edit)



## Weekly Meeting Updates

Our team has weekly meetings from 3:30pm to 4:15pm on Wednesdays. Might be changed later.
Bi-weekly meeting with client TBD

[Meeting notes](https://docs.google.com/document/d/1ccZFtlUd6iiBPOcO2sUgpn-_ya-qcng9ljRkd69B_1U/edit?pli=1)

