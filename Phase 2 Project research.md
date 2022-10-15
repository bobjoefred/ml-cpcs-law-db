Phase 2: 
# Research for CPCS team

## _Yile Wang,  Aditya Pal, Ryan Hom, Wenhan Zhou  2022-October-13 v0.0.1-dev_

Instructions:
Link your project research markdown file which outlines the papers and projects you explored and describes the methods you can employ here:

### Paper
Questions we want to answer: 
* Why we pick the paper？
* How is it relevant?
* What’s in the paper? 
* How can it help our project? 
* What method/pipeline/model are they using? 
* What dataset are they using? 

[Paper 1](https://arxiv.org/abs/1609.06423): OCR++: A Robust Framework For Information Extraction from Scholarly Articles
This paper described an open-source framework called OCR++ proposed in 2016 that helps to extract valuable information such as metadata including title, author names, affiliation and email from English-only PDF documents. Not only it could be used to extract good English information from our document, it can also extract the structure and the bibliography of the document including the section heading, body text, table, citation from the document. This is extremely useful for our project in the preprocessing steps. Our dataset is mostly PDF files with legal documents consisting of different titles and format, such as the “Brady v Maryland” in the headline. With a good extraction tool, we might be able to preprocess the legal documents with key information including name, rank, current status/former status, and department of the targeted officer, as well as information about the incident. Furthermore, according to the paper, this framework could improve the accuracy of 50% and a processing time of 52%. This will come in handy when we are training the model, as it will save us significant memory and training time. This paper also mentioned that the result of this framework will be exported into structured TEI-encoded documents. We could utilize the TEI-encoded documents and modify it to the csv file for post-processing. 

[Paper 2](https://arxiv.org/pdf/2208.11203.pdf): Graph Neural Networks and Representation Embedding for Table Extraction in PDF Documents
Our dataset contains tables which are difficult for traditional OCR tools to extract data from. The authors of the paper have used Graph Neural Networks. The model is evaluated on research papers and the dataset obtained by merging the information provided in
the PubLayNet and PubTables-1M datasets. The paper tackles the problem of identifying the table headers and other table elements by approaching it as a node classification problem.

[Paper 3](https://arxiv.org/pdf/2208.04011.pdf): Information Extraction from Scanned Invoice Images using Text Analysis and Layout Features
In our dataset, there are some scanned reports in different forms containing officer information and incident information. There are also various formats for invoice. While storing invoice content as metadata to avoid paper document processing may be the future trend, almost all of daily issued invoices are still printed on paper or generated in digital formats such as PDFs. In this paper, we introduce the OCRMiner system for information extraction from scanned document images which is based on text analysis techniques in combination with layout features to extract indexing metadata of (semi-)structured documents. This paper research on the system is designed to process the document in a similar way a human reader uses, i.e. to employ different layout and text attributes in a coordinated decision. The system consists of a set of interconnected modules that start with (possibly erroneous) character-based output from a standard OCR system and allow to apply different techniques and to expand the extracted knowledge at each step. Using an open source OCR, the system is able to recover the invoice data in 90% for English and in 88% for the Czech set.

(Add Paper 4 here)



### Our Project 

Each Brady disclosure contains a notice, a letter from the prosecution (Assistant District Attorneys and District Attorneys) explaining why a potential witness working in law enforcement has some potentially problematic things in their history. In a large proportion of disclosures, there’ll be a brief explanation of what happened in the notice itself. A smaller proportion will just throw to the attachments, which may take the form of several documents. We’d like to know what kinds of documents there are (usually they’re labeled) and, to the extent it’s reasonably possible, to have summaries for each.

##### Client Wish List #####
1. Break up the disclosure documents (presented in a PDF combining many documents) into constituent PDF documents, placed in directories based on the department of the officer (a directory for Boston Police Department, a directory for MA State Police, etc), with each file labeled with the name(s) of the officer(s) they discuss and the date
* Carrying forward both the notice and any attachments for each document
2. From each individual disclosure, in a spreadsheet:
* The filename and path of the document
* Basic info about officers
    * Name
    * Rank (Officer, Sergeant, Lieutenant, etc.)
    * Current/former status (‘former’, ‘retired’, etc.)
    * Department (name of municipality/State Police)
- Info about what happened
    * Which kind(s) of investigation(s) or issues?
        * Subject to an investigation by Internal Affairs, the Civil Service Commission, etc. (i.e. p1, p3, p21)
        * Faced criminal charges (i.e. p22, p26, p30, p86)
        * Found to have done improper things while serving as a witness/in filing reports (i.e. p20, p72, p226)
    * Identifying info about investigations if present
        * It may just say ‘an internal affairs investigation’ or something similar without identifying info
        * But please get docket numbers and court locations if it’s a criminal case
        * Dates whenever available
    * Which rules/laws they violated, or otherwise what did they do wrong?
        * In other words, what specifically did they do?
            * May be specific criminal charges
            * May just be names of rules they were found to have broken by internal affairs investigations or other processes like conduct unbecoming an officer
        * Dates for these actions whenever available
    * Outcome of investigation if present
        * Disposition (how did the investigation conclude?), e.g.
            * Sustained allegations if it’s an internal affairs investigation, or failure to sustain
            * Plea or guilty verdict in a court case, acquittal, etc.
    * Penalties/consequences, things like:
            * Could be nothing/no information provided
            * Written reprimand/warning
            * Suspension/administrative leave
            * Firing/Resignation/Retirement (important to know which)
            * Fines/restitution (dollar amount if available)
            * Probation
            * Prison sentence
- A list of attachments
    * What kinds of documents were there?
    * If any info from the above list is present only in the attachments, please pull it out as best as possible


### Relevant Open Source Projects

[EasyOCR](https://github.com/JaidedAI/EasyOCR) is the library used by the previous team and offers reliable image to text extraction based on their results. It can also be integrated with Hugging Face which provides a wide variety of ML models. The project is also updated regularly to make sure the libraries and dependencies are up to date.

[OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF) is the repository uses Tesseract OCR engine, is up to date and is tested on ‘millions’ of PDFs according to the repository owner. It also has community support for various operating systems.

[Previous Team Repository](https://github.com/BU-Spark/ml-cpcs-law-db) is the repository of source code of the previous team and contains a relevant pipeline. Our approach is to try and use this pipeline on our new dataset and refine it wherever necessary.

### Previous Project and Data

The previous group scraped a dataset of civil suites and produced a pipeline that extracts key information into a CSV file. It takes many hours to read every single document manually. 
The pipeline used by previous team is the following-
File Input –>OCR Extraction -> Simple Extraction -> ML Extraction -> File Output 
The OCR Extraction is done using [Easy OCR Library](https://github.com/JaidedAI/EasyOCR)
The Simple Extraction used for extracting data like Docket Number and is done using Regex expressions for pattern matching.
For ML Extraction, they employed 2 pre-trained ML model, specifically-
Google Pegasus - Summarization
Facebook (Meta) Bart-Large-MNLI- Zero-shot classification

(Add Data Availability table here)

