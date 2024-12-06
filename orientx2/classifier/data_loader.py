import torch
import csv
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset


def load_data(filepath, test_size=0.15, shuffle=True):
    texts, labels = [], []

    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if len(row) < 2:
                continue
            try:
                label, text = int(row[0]), row[1]
                labels.append(label)
                texts.append(text)
            except ValueError:
                print("ValueError")

    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, test_size=float(test_size), random_state=42, shuffle=shuffle, stratify=labels
    )

    return (train_texts, train_labels), (val_texts, val_labels)


class TextClassificationDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        encoding = self.tokenizer(
            text,
            return_tensors='pt',
            max_length=self.max_length,
            padding='max_length',
            truncation=True
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }
