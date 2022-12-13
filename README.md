# Congressional Search 

The goal of this project is to use state of the art Learn to Rank methods to develop a better search engine for bills proposed to the US Congress. This solution does more than 3 times as well at retrieving relevant sources for short text queries (measured by normalized discount cumulative gain (nDCG) on test data manually annotated for relevance) than does the search function at [Congress.gov](https://www.congress.gov/). It uses a random forest model to rank documents after they are indexed by Py-Terrier and scored with the BM25 algorithm. See the included paper, Congressional Search, for more details and context.

So far, it has been implemented on a limited course of about 20% of the bills introduced between 1993 and 2018. Credit for arranging this corpus goes to Anastassia Kornilova, who developed this collection for this paper on automatic summarization and generously made it available via [github](https://github.com/FiscalNote/BillSum) and [Kaggle](https://www.kaggle.com/datasets/akornilo/billsum).

I have not yet created a frontend application to deliver this search. The <em>congress_search.py</em> implements this search engine for interaction via the terminal; the notebook file <em>developing_search.ipynb</em> demonstrates the process by which it was developed.
