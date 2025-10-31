# VOC Gloss Explorer

### Introduction
The VOC Gloss Explorer is a streamlit-based application. A live version of it is currently available on [Streamlit Cloud](https://voc-gloss-explorer.streamlit.app/). It allows the user to search through possible 'glosses', explanations of words within a text, from the VOC Archives. The way the data is processed for the app is based on a conference abstract available [here](**Pepping, K. (2024). (https://doi.org/10.5281/zenodo.11455556)) using code available [here](https://github.com/KayWP/GLOBALISE-glossfinder). The data itself is based on the GLOBALISE transcriptions of the *Overgekomen brieven en papieren* of the Dutch East India Company available [here](https://datasets.iisg.amsterdam/dataset.xhtml?persistentId=hdl:10622/LVXSBW). It could easily be changed to use other corpora.

### Relevant publications
Pepping, K. (2024). *Not something to gloss over: identifying foreign loanwords and their understood meaning in the corpus of the Dutch East India Company.* Paper presented at Digital Humanities in the Benelux 2024 Conference, Leuven, Belgium.  
[https://doi.org/10.5281/zenodo.11455556](https://doi.org/10.5281/zenodo.11455556)

GLOBALISE project (2024). _VOC transcriptions v2 - GLOBALISE_. IISH Data Collection, V1. [https://hdl.handle.net/10622/LVXSBW](https://hdl.handle.net/10622/LVXSBW)

### Deploying

#### Requirements
```
streamlit
st-annotated-text
```

The code expects a SQLite3 database

#### Folder structure
```
pages/Alphabetical List of Terms.py
pages/Search.py
Hello.py
glosses.db
requirements.txt
```
#### Running the code
```
streamlit run Hello.py
```

#### Other files in the repo

| File name                 | Explanation                                                                                                                             |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| data preprocessing..ipynb | A Jupyter Notebook that preprocesses the output of the [glossfinder script](https://github.com/KayWP/GLOBALISE-glossfinder)             |
| preprocessed_csv.csv      | The output of data preprocessing.ipynb                                                                                                  |
| schema.sql                | A file explaining the schema of the database, including import statements used to import the CSV data into the database by using .read. |

### Explanation of the code
#### Hello.py
Shows introductory text and loads a few statistics.

#### Search.py
##### write_result()
Determines how the results are written, using annotated text

##### bag_words()
Puts all the words in the results into a bag, filters out common stop words.

##### parse_page_info()
Parses the page part of the gloss info into proper source references + a link to the GLOBALISE transcription viewer

##### get_similar_terms()
Returns 10 most similar terms with a threshold of 0.6

##### rest of the page
When you give it a search term, it checks if there are similar terms and if the top ten of those includes the exact searched for string. If not, it will go with a similar term. It then fetches the results and prints those.

#### Alphabetical list of terms.py
Does the same as Search.py but without getting similar terms and instead offering a letter + select method to pick a term. No fuzzy matching involved.