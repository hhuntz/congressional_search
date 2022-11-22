# Congressional Search 

Corpus credit to Anastassia Kornilova, who developed this collection for [this paper]([url](https://arxiv.org/abs/1910.00523)) on automatic summarization and generously made it available via [github]([url](https://github.com/FiscalNote/BillSum)) and [kaggle]([url](https://www.kaggle.com/datasets/akornilo/billsum)). This corpus includes the full text, summaries, and titles of bills introduced to the US Congress from 1993-2016. 

I have combined her test/train sets to do my own splitting. She used another [github-hosted]([url](https://github.com/unitedstates/congress)) project simply called Congress to get bill data. You can find my own attempt at gathering similar data for more recent congressional sessions in the get_congress_corpus.ipynb file here; it technically works, but it takes a spectacularly long time and so does not provide a reasonable solution for scraping full text, summaries, and titles of congressional bills. 

