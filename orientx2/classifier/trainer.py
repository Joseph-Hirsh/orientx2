import torch
from torch import nn
from torch.utils.data import DataLoader
from transformers import BertTokenizer, get_linear_schedule_with_warmup
from sklearn.metrics import accuracy_score, classification_report
from .data_loader import TextClassificationDataset
from .model import BERTClassifier


class ClassificationPipeline:
    def __init__(self, model_name="bert-base-uncased", num_classes=3, max_length=128, batch_size=16, lr=2e-5, epochs=5):
        self.model_name = model_name
        self.num_classes = num_classes
        self.max_length = max_length
        self.batch_size = batch_size
        self.lr = lr
        self.epochs = epochs

        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = BERTClassifier(model_name, num_classes).to(self.device)

        self.train_loader = None
        self.val_loader = None

    def prepare_data(self, train_texts, train_labels, val_texts, val_labels):
        train_dataset = TextClassificationDataset(train_texts, train_labels, self.tokenizer, self.max_length)
        val_dataset = TextClassificationDataset(val_texts, val_labels, self.tokenizer, self.max_length)

        self.train_loader = DataLoader(train_dataset, batch_size=self.batch_size, shuffle=True)
        self.val_loader = DataLoader(val_dataset, batch_size=self.batch_size)

    def train(self, train_output_path):
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=self.lr)
        total_steps = len(self.train_loader) * self.epochs
        scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)

        for epoch in range(self.epochs):
            self.model.train()

            loss = None

            for batch in self.train_loader:
                optimizer.zero_grad()
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['label'].to(self.device)
                outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
                loss = nn.CrossEntropyLoss()(outputs, labels)
                loss.backward()
                optimizer.step()
                scheduler.step()

        self.save_model(train_output_path)
        accuracy, report = self.evaluate()
        print(report)

    def evaluate(self):
        self.model.eval()
        predictions, actual_labels = [], []

        with torch.no_grad():
            for batch in self.val_loader:
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['label'].to(self.device)
                outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
                _, preds = torch.max(outputs, dim=1)
                predictions.extend(preds.cpu().tolist())
                actual_labels.extend(labels.cpu().tolist())

        accuracy = accuracy_score(actual_labels, predictions)
        report = classification_report(actual_labels, predictions)

        return accuracy, report

    def save_model(self, path="assets/model.pth"):
        torch.save(self.model.state_dict(), path)

    def load_model(self, path="assets/model.pth"):
        self.model.load_state_dict(torch.load(path, weights_only=True))
