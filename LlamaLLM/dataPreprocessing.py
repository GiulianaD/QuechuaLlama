import pandas as pd
import re
import os

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
