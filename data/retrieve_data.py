import argparse
import pandas
from Bio import Entrez

parser = argparse.ArgumentParser(description='Download pubmed articles.')
parser.add_argument('category', type=str,
                    help='give a category to download (approved or terminated)')

# fetch the articles of the given pmids list
def fetch_details(id_list):
    if type(id_list) is list:
        ids = ','.join(id_list)
    else:
        ids = id_list
    Entrez.email = 'your@email'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results


def retrieve_abstracts(fetch_type):
    if fetch_type == 'approved':
        df_data = pandas.read_csv('approved_interventions_studies.csv')
        pmids_to_fetch = list(df_data['pmid'])
    elif fetch_type == 'terminated':
        df_data = pandas.read_csv('terminated_interventions_studies.csv')
        pmids_to_fetch = list(df_data['pmid'])
    else:
        print('The fetch type is not supported. Please try again.')
        return

    pmid_abstracts ={}
    pmid_pubdates = {}
    for i, pmid in enumerate(pmids_to_fetch):
        try:
            pubmed_papers = fetch_details(pmid)
            abstract_texts = pubmed_papers['PubmedArticle'][0]['MedlineCitation']['Article']['Abstract']['AbstractText']
            abstract_j = " ".join(abstract_texts)
            pmid_abstracts[pmid] = abstract_j
            # find the publication date
            pub_date = pubmed_papers['PubmedArticle'][0]['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']
            if 'MedlineDate' in pub_date.keys():
                pdate = pub_date['MedlineDate']
            elif 'Month' in pub_date.keys():
                pdate = pub_date['Month']+" "+pub_date['Year']
            else:
                pdate = pub_date['Year']
            pmid_pubdates[pmid] = pdate
        except:
            print('Error for pmid: ', pmid)

        if i%100 == 0:
            print('Already fetched %.2f%% of the abstracts. Please wait...' % (i/len(pmids_to_fetch)*100))
    # map abstracts to the correct pmid in df
    df_data['abstract'] = df_data['pmid'].map(pmid_abstracts)
    # map dates to the correct pmid in df
    df_data['pub_date'] = df_data['pmid'].map(pmid_pubdates)
    # save to csv file
    header = ["intervention", "phase", "ct_id", "pmid", "pub_date", "abstract"]
    df_data.to_csv(fetch_type+'_interventions_with_abstracts.csv', columns = header)

    print('!!Finished!!')

if __name__ == '__main__':
    args = parser.parse_args()
    retrieve_abstracts(args.category)
