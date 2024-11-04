import pandas as pd
import re
import os
from num2words import num2words

# File paths
splits = {
    'train': 'data/train-00000-of-00001.parquet', 
    'validate': 'data/validate-00000-of-00001.parquet', 
    'test': 'data/test-00000-of-00001.parquet'
}

# Quechua number mapping
units = {
    0: 'ch\'usaq', 1: 'juk', 2: 'iskay', 3: 'kimsa', 4: 'tawa', 5: 'phichqa', 
    6: 'suqta', 7: 'qanchis', 8: 'pusaq', 9: 'jisq\'un'
}
basic_terms = {10: 'chunka', 100: 'pachak', 1000: 'waranqa'}
vowels = ['a', 'e', 'i', 'o', 'u']

# Loads data from a parquet file into a DataFrame.
def load_data(filepath):
    try:
        return pd.read_parquet(filepath)
    except Exception as e:
        print(f"Error loading file {filepath}: {e}")
        return None

# Data cleaning and normalization functions
def to_lowercase(text):
    return text.lower()

def remove_special_characters(text):
    pattern = r"^\s+|[#\-–&$\*\+\[\]\<\>\\=_\*•—]+"
    return re.sub(pattern, "", text)

def remove_enumeration(text):
    pattern = r"^\d+|\(?[a-zA-Z]\)"
    return re.sub(pattern, "", text)

def remove_extra_spaces(text):
    pattern = r"\s+"
    return re.sub(pattern, " ", text)

def remove_biblical_references(text):
    pattern = r"\(.+:.*\)"
    return re.sub(pattern, "", text)

# Applies all normalization functions to the text.
def normalize_text(text):
    text = str(text)
    text = remove_enumeration(text)
    text = remove_biblical_references(text)
    text = to_lowercase(text)
    text = remove_special_characters(text)
    text = remove_extra_spaces(text)
    return text

# Number conversion functions
def add_suffix(word):
    if word.split()[-1] in units.values():
        return word + ('yuq' if word[-1] in vowels else 'niyuq')
    return word

# Converts numbers to Quechua representation.
def get_quz_number(num):
    if num == 0:
        return units[0]
    result = []
    if num >= 100000:
        thousands_place = num // 1000
        result.append(get_quz_number(thousands_place))
        result.append(basic_terms[1000])
        num %= 1000
    if num >= 10000:
        thousands_place = num // 1000
        result.append(get_quz_number(thousands_place))
        result.append(basic_terms[1000])
        num %= 1000
    if num >= 1000:
        thousands_place = num // 1000
        result.append(units[thousands_place] if thousands_place > 1 else '')
        result.append(basic_terms[1000])
        num %= 1000
    if num >= 100:
        hundreds_place = num // 100
        result.append(units[hundreds_place] if hundreds_place > 1 else '')
        result.append(basic_terms[100])
        num %= 100
    if num >= 10:
        tens_place = num // 10
        result.append(units[tens_place] if tens_place > 1 else '')
        result.append(basic_terms[10])
        num %= 10
    if num > 0:
        result.append(units[num])
    return " ".join(filter(None, result))

def replace_quechua_numbers(text):
    return re.sub(r'\b\d+\b', lambda match: add_suffix(get_quz_number(int(match.group()))), text)

def replace_spanish_numbers(text):
    return re.sub(r'\b\d+\b', lambda match: num2words(int(match.group()), lang='es'), text)

# Process DataFrame
def preprocess_dataframe(df):
    if df is None:
        print("DataFrame is empty. Skipping processing.")
        return None
    for i, row in df.iterrows():
        df.at[i, 'spa'] = replace_spanish_numbers(row['spa'])
        df.at[i, 'quz'] = replace_quechua_numbers(row['quz'])
    for col in df.columns:
        df[col] = df[col].apply(normalize_text)
    return df

# Generate conversation dataset for LLM training
def generate_llm_dataset(df):
    dataset = {"conversations": [], "labels": []}
    for _, row in df.iterrows():
        spa_text = f"Please translate this text from Spanish to Quechua: '{row['spa']}'"
        quz_text = f"Here is the Quechua translation: '{row['quz']}'"
        dataset["conversations"].append([{"role": "user", "content": spa_text},
                                         {"role": "assistant", "content": quz_text}])
        dataset["labels"].append(quz_text)
    return Dataset.from_dict(dataset)

# Splits and saves dataset to train, test, and validation sets.
def save_dataset_splits(dataset, train_size=0.8, file_prefix="dataset"):
    split_data = dataset.train_test_split(train_size=train_size)
    train_set = split_data["train"]
    test_validation_set = split_data["test"].train_test_split(train_size=0.5)
    test_set = test_validation_set["test"]
    validation_set = test_validation_set["train"]

    train_set.to_csv(f'{file_prefix}_train.csv', index=False)
    test_set.to_csv(f'{file_prefix}_test.csv', index=False)
    validation_set.to_csv(f'{file_prefix}_validation.csv', index=False)
    return train_set, test_set, validation_set

# Main processing flow
if __name__ == "__main__":
    df = load_data("hf://datasets/pollitoconpapass/cuzco-quechua-translation-spanish/" + splits["train"])
    if df is not None:
        print("Initial data preview:", df.head(5))
    
        df = preprocess_dataframe(df)