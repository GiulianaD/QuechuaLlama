import pandas as pd

splits = {'train': 'data/train-00000-of-00001.parquet', 'validate': 'data/validate-00000-of-00001.parquet', 'test': 'data/test-00000-of-00001.parquet'}
df = pd.read_parquet("hf://datasets/pollitoconpapass/cuzco-quechua-translation-spanish/" + splits["train"])

print(df.head(5))