# Analyzing Historical Sentiments in American Newspapers
This project presents a methodological framework for analyzing historical sentiments and semantic shifts in American newspapers, utilizing Natural Language Processing (NLP) techniques. Originally applied to study American public sentiments towards the Japanese in the interwar period, this methodological framework offers a novel approach to historical analysis, providing researchers with the tools to delve into the nuanced shifts in public perception. Whether examining attitudes towards different ethnic groups, political ideologies, technological advancements, or cultural concepts, this NLP-based approach allows for a detailed and quantifiable exploration of historical narratives.

## Data
[Chronicling America](https://chroniclingamerica.loc.gov), a freely accessible online repository produced through the National Digital Newspaper Program (NPDP), a partnership between the National Endowment for the Humanities and the Library of Congress, archives over 21 million pages of U.S. newspapers published between 1777 and 1963. Encompassing national and local publications from all 50 states, this database offers a unique window into observing the shifting tides of American public sentiment. Its extensive archive amounts to over 2 terabytes of bulk data and 1 terabyte of text data, and keeps growing daily.

## Methodology

The jupyter notebook in this repo downloads historical newspapers pages containing your search terms, builds a word2vec model, lets you compare semantic shifts over time using anchor methods, and visualizes the findings.

### Download Data
Utilizing Chronicling America API's search fuction (https://chroniclingamerica.loc.gov/#tab=tab_advanced_search). `download.py` takes a search result url and downloads 2,000 text files of newspaper pages containing your search terms. The current set-up requires you to restrict the search date to one year and downloads up to 100 pages (2,000 items), but you can edit the download.py to change these parameters. `download.py` creates `searchterms.txt`, `metadata.csv`, and downloads text files in `\ocr_text`. `searchterms.txt` records which search terms were used and when the download took place.  `metadata.csv` saves metadata of textfiles in the csv format, which will be later used to create a Pandas dateframe.

### Word2Vec
Word2vec produces word embeddings, which are dense vector representations of words in a continuous vector space. Developed by a team of researchers at Google led by Tomas Mikolov, word2vec was groundbreaking because it enabled words with similar meanings to have similar representations, capturing a significant amount of syntactic and semantic information about words.

The key concepts behind word2vec are:
* Continuous Bag of Words (CBOW): In this model, word2vec predicts a target word based on its context. The context is defined as a window of surrounding words. The idea is to use the context to predict the word in the middle of this window.
* Skip-gram: This is the opposite of CBOW. Instead of predicting the target word from its context, it uses a target word to predict its surrounding context. This model is particularly effective for learning representations for infrequent words.

Both models are trained on large corpora of text and learn to place words with similar meanings close to each other in a high-dimensional space. This allows for operations like vector addition and subtraction to reveal semantic relationships between words. For example, the famous example "king - man + woman = queen" shows how relationships and analogies can be captured.

This project employs Gensim’s word2vec implementation with the Continuous Bag-of-Words (CBOW) architecture for training embeddings on the curated historical corpus. CBOW’s strength in accurately representing common words aligns well with the study’s objective. Additionally, negative sampling is chosen over hierarchical softmax for optimization. By transforming the prediction task into discerning whether random “negative” words (words not in the vicinity of the target word) appear alongside targets in training data, negative sampling focuses computations on critical binary classifications rather than exhaustively calculating probabilities across the entire vocabulary.

### Anchor Methods

Conventional diachronic analysis using word embedding techniques often spans decades, gauging semantic drift through cosine distances between vectors over 10-year intervals. However, this method is not suitable for this project due to the yearly variance in vector representations designed to capture annual contextual shifts. To address this, this study measures the cosine similarity of the target word to a set of anchor words that have relatively stable meanings over time, providing a year-by-year semantic trajectory. 

The target word in my study was *‘Japanese’* and the chosen anchor words were *‘enemy’*, *‘ally’*, *‘immigrant’*, which were consistent in definition and frequency, serving as reliable benchmarks. Cosine similarity, by quantifying the angular proximity between vectors from 1 to -1, illuminates semantic closeness or contextual overlap. Sharp rises or dips in cosine similarity scores signal fluctuations in how *‘Japanese’* appears contextually coupled to these indicators across decades of newspapers.

You will be able to choose your target word and anchor words in `word2vec.ipynb` and conduct your analysis.


## Coding Requirement & Time Committment

To run the files in this repository, you should have a basic knowledge of the command line interface and directory structure. For guidance, please consult the following tutorial: [Introduction to the Bash Command Line](https://programminghistorian.org/en/lessons/intro-to-bash).

This repository offers a streamlined, more accessible version of the project. Data download is efficient, typically requiring about 1 minute for every 1,000 entries, and operates in the background. Constructing a database from text files spanning approximately 50 years will take around 2 hours. The analysis phase is expected to last between 1 to 2 hours.

Should you have any inquiries or require further assistance, do not hesitate to contact me at jhahm@sas.upenn.edu.

## Dependency Management
To be updated.
* requirements.txt
* pip! install
* Instruction for creating a virtual env
* Dockerfile