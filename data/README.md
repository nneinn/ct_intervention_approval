
## Download data

Each intervention (approved or terminated) is associated with a set of Clinical Trials identifiers (NCTid) and pmids (PubMed artciles). These associations were extracted from clinicaltrials.gov and PubMed during May-June 2021 and may not reflect the most current/accurate data available from these sources (clinicaltrials.gov and PubMed(NLM)).

### Prerequisites

- python >= 3.7
- pandas
- biopython


### Data

The dataset can be downloaded using the python script `retrieve_data.py`. Run the script:

```
python3 retrieve_data.py approved
```
or
```
python3 retrieve_data.py terminated
```

to download the respective set.

Please make sure that you replace the Entrez.email with your email inside the script.
