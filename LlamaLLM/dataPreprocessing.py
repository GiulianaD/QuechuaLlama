import pandas as pd
import re
import os
from num2words import num2words
from datasets import load_dataset, Dataset
from unsloth.chat_templates import get_chat_template

# Load the data

splits = {'train': 'data/train-00000-of-00001.parquet', 'validate': 'data/validate-00000-of-00001.parquet', 'test': 'data/test-00000-of-00001.parquet'}
df = pd.read_parquet("hf://datasets/pollitoconpapass/cuzco-quechua-translation-spanish/" + splits["train"])

units = {
    0: 'ch\'usaq', 1: 'juk', 2: 'iskay', 3: 'kimsa', 4: 'tawa', 5: 'phichqa.', 6: 'suqta', 7: 'qanchis', 8: 'pusaq', 9: 'jisq\'un'
}

basic_terms = {
    10: 'chunka', 100: 'pachak', 1000: 'waranqa'
}

vowels = ['a', 'e', 'i', 'o', 'u']

#Inspect the data
print(df.head(5))
print(df.info())
print(df.shape)

def toLowerCase(input):
    return input.lower()

def removeSpecialCharacters(input):
    pattern = r"^\s+|[#\-–&$\*\+\[\]\<\>\\=_\*•—]+"
    return re.sub(pattern, "", input)

def removeEnumeration(input):
    pattern =  r"^\d+|\(?[a-zA-Z]\)"

    return re.sub(pattern, "", input)

def removeExtraSpaces(input):
    pattern = r"\s+"
    return re.sub(pattern, " ", input)

def removeBiblicalReferences(input):
    pattern = r"\(.+:.*\)"
    return re.sub(pattern, "", input)

def normalize(input):
    input = str(input)
    input = removeEnumeration(input)
    input = removeBiblicalReferences(input)
    input = toLowerCase(input)
    input = removeSpecialCharacters(input)
    input = removeExtraSpaces(input)
    return input

# Numbers to Text
def add_suffix(word):
    print("WORD: ", word)

    if word.split()[-1] in units.values():
        if word[-1] in vowels:
            return word + 'yuq'
        else:
            return word + 'niyuq'
            
    return word

def get_quz_number(num):
    if num == 0:
        return units[0] 

    result = []

    if num >= 100000:
        thousands_place = num // 1000
        if thousands_place > 100:
            result.append(get_quz_number(thousands_place))
        else:
            result.append(basic_terms[thousands_place])
        result.append(basic_terms[1000])
        num %= 1000

    if num >= 10000:
        thousands_place = num // 1000
        if thousands_place > 10:
            result.append(get_quz_number(thousands_place))
        else:
            result.append(basic_terms[thousands_place])
        result.append(basic_terms[1000])
        num %= 1000

    if num >= 1000:
        thousands_place = num // 1000
        if thousands_place > 1:
            result.append(units[thousands_place])
        result.append(basic_terms[1000])
        num %= 1000

    if num >= 100:
        hundreds_place = num // 100
        if hundreds_place > 1:
            result.append(units[hundreds_place])
        result.append(basic_terms[100])
        num %= 100

    if num >= 10:
        tens_place = num // 10
        if tens_place > 1:
            result.append(units[tens_place])
        result.append(basic_terms[10])
        num %= 10 

    if num > 0:
        if result == []:
            result.append(units[num])
        else:
            result.append(units[num])
    
    return " ".join(result)

def replace_quechua_numbers_to_text(text):
    return re.sub(r'\b\d+\b', lambda match: add_suffix(get_quz_number(int(match.group()))), text)

def replace_spanish_numbers_to_text(text):
    return re.sub(r'\b\d+\b', lambda match: num2words(int(match.group()), lang='es'), text)

for i, row in df.iterrows():
    print(f"I: {i}, ROW: {i}", i, row)
    df.at[i, 'spa'] = replace_spanish_numbers_to_text(row['spa'])
    df.at[i, 'quz'] = replace_quechua_numbers_to_text(row['quz'])

for col in df.columns:
  df[col] = df[col].apply(normalize)

df = pd.read_csv('/content/spa_quz_normalized_2000.csv')

df.head(5)
dataset = {"conversations":[], "labels": []}

for i, row in df.iterrows():
    spa_text = f"Please translate this text from spanish to quechua: '{row['spa']}'"
    quz_text = f"Here is the quechua translation: '{row['quz']}'"
    dataset["conversations"].append([{"role": "user", "content": spa_text},{"role": "assistant", "content": quz_text}])
    dataset["labels"].append([quz_text])

dataset = Dataset.from_dict(dataset)
train_test_split = dataset.train_test_split(train_size=0.8)
train_set = train_test_split["train"]
test_validation_set= train_test_split["test"].train_test_split(train_size=0.5)
test_set = test_validation_set["test"]
validation_set = test_validation_set["train"]
validation_set .to_csv('validation2k.csv', index=False)