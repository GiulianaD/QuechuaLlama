import pandas as pd
import re
import nltk
from langdetect import detect

nltk.download('punkt')

# Load the data

splits = {'train': 'data/train-00000-of-00001.parquet', 'validate': 'data/validate-00000-of-00001.parquet', 'test': 'data/test-00000-of-00001.parquet'}
df = pd.read_parquet("hf://datasets/pollitoconpapass/cuzco-quechua-translation-spanish/" + splits["train"])

#Inspect the data

print(df.head(5))
print(df.info())
print(df.shape)

def toLowerCase(input):
    return input.lower()

def removeSpecialCharacters(input):
    pattern = r"^\s+|[#\-&$\*\+\[\]\<\>\\=_\*]+"
    return re.sub(pattern, "", input)

def removeExtraSpaces(input):
    pattern = r"\s+"
    return re.sub(pattern, " ", input)

def removeBiblicalReferences(input):
    pattern = r"\(.+:.*\)"
    return re.sub(pattern, "", input)

def normalize(input):
    input = toLowerCase(input)
    input = removeSpecialCharacters(input)
    input = removeExtraSpaces(input)
    input = removeBiblicalReferences(input)
    return input

def split_sentences(text):
        return nltk.sent_tokenize(text, language='english')

# Split text into sentences and save it as a new dataframe.
# If the orignal text doesn´t match its translation regarding the number of sentences, then it is discarted.

new_data = []

for i, row in df.iterrows():
    spanish_sentences = split_sentences(row['spa'])
    quechua_sentences = split_sentences(row['quz'])

    # Ensure that both sentence lists are of the same length (alignment)
    if len(spanish_sentences) == len(quechua_sentences):
        for s_sent, q_sent in zip(spanish_sentences, quechua_sentences):
            new_data.append({'spanish_sentence': s_sent, 'quechua_sentence': q_sent})
    else:
        print(f"Row {i} has misaligned sentences. You may need to handle this case.")

# Create a new DataFrame with the sentence-level data
# Verify that the spanish column has spanish text and that the 
# quechua column doesn't have spanish text within it. If so, it is discarted.

df_sentences = pd.DataFrame(new_data)
indexes2delete = []

for i, row in df_sentences.iterrows():
    try:
      lang_sp = detect(row['spanish_sentence'])
      lang_q = detect(row['quechua_sentence'])

      if lang_sp != 'es' or lang_q == 'es' :
          indexes2delete.append(i)
    except:
      indexes2delete.append(i)

df_sentences.drop(indexes2delete, inplace=True)

# Add new data to the dataset
df2 = pd.read_csv('./Dataset/EspQuechua.csv')
df_sentences = pd.concat([df_sentences, df2[['Español', 'Quechua']].rename(columns={'Español': 'spanish_sentence', 'Quechua': 'quechua_sentence'})], ignore_index=True)
print(df2.shape)