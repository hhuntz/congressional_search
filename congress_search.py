import os
import pandas as pd
import numpy as np
import pyterrier as pt
from pyterrier.measures import *
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')

current_path = os.path.dirname(os.path.abspath(__file__))

def get_index():
    '''
    access or creates index
    returns pt index
    '''

    current_path = os.path.dirname(os.path.abspath(__file__))
    # start py-terrier
    if not pt.started():
        pt.init(logging = 'ERROR')

    bills_df = pd.read_csv(current_path + '/data/us_congress_bills_1993-2016.csv', index_col = 0)
    bills_df.columns = ['docno', 'text', 'summary', 'title'] 

    index_dir = current_path + '/congressional_search_index'
    iter_indexer = pt.IterDictIndexer(index_dir, overwrite=True)

    if not os.path.exists(index_dir + "/data.properties"):
        bills_dict = bills_df.to_dict(orient="records") 
        indexref = iter_indexer.index(bills_dict, fields=(['text']))    
    else:
        indexref = iter_indexer.index(index_dir)

    index = pt.IndexFactory.of(indexref)

    return index, bills_df

def train_model(index):
    '''
        takes in pt index object
        returns bm25 batchretrieve object for 1st-step query scoring
                and trained random forest model
    '''

    # get training data
    queries = pd.read_csv(current_path + '/data/sample_queries.csv', index_col = 0)
    annotations = pd.read_csv(current_path + '/data/congress_bills_annotations.csv')
    labels = annotations[['qid', 'docno', 'label']]
    labels['label'] = labels['label'].astype('int32')

    # get features
    bm25 = pt.BatchRetrieve(index, wmodel = 'BM25')
    tfidf = pt.BatchRetrieve(index, wmodel = 'TF_IDF')

    features_pipe = tfidf >> bm25
    topics = features_pipe.transform(queries)

    # set up random forest
    features = bm25 ** tfidf
    rf = RandomForestRegressor(n_estimators = 400, random_state = 42, n_jobs = 4)
    rf_pipe = features >> pt.ltr.apply_learned_model(rf)
    rf_pipe.fit(topics, labels)

    return bm25, rf_pipe

def get_results(query, bills_df, scorer, model):
    scores = scorer.search(query)
    results = model.transform(scores)
    res_bills = results.merge(bills_df).sort_values(['rank'])
    return res_bills

def search(bills, scorer, model, num_res = 5):
    # get query
    q = input('Enter a query or quit:\n')
    while q.strip().lower() != 'quit':
        # get results
        try:
            res = get_results(q, bills, scorer, model)
            print(f'Top {num_res} results for "{q}":')
            top_res = list(res.head(num_res).title)
            for i in range(len(top_res)):
                print(f'\t{i+1}: {top_res[i]}')
        except:
            print(f'No results for {q}')

        # get new query
        q = input('Enter a new query or quit:\n')

def main():
    # setup
    print('accessing index...')
    index, bills = get_index()

    print('training model...')
    bm25_scorer, rf_model = train_model(index)
    print('ready!\n')

    search(bills, bm25_scorer, rf_model)
    print('\ngoodbye!')


if __name__ == '__main__':
    main()