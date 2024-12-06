import torch
from torch import nn
from torch.utils.data import DataLoader
from transformers import BertTokenizer, get_linear_schedule_with_warmup, get_scheduler
from sklearn.metrics import accuracy_score, classification_report
from .data_loader import TextClassificationDataset
from .model import BERTClassifier

# num_classes=3, max_length=300, batch_size=6, lr=3e-5, epochs=5 - 84%
# try doing 6 epochs and seeing if it does even better
# make testing dataset
# get the balance correct by sampling 300 tweets, classifying, determining what the ratio is
# then


class ClassificationPipeline:
    def __init__(self, model_name="bert-base-uncased", num_classes=3, max_length=300, batch_size=6, lr=3e-5, epochs=7):
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
        scheduler = get_scheduler(
            "linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=len(self.train_loader) * self.epochs
        )
        loss_fn = nn.CrossEntropyLoss()

        for epoch in range(self.epochs):
            self.model.train()
            total_loss = 0

            for batch in self.train_loader:
                optimizer.zero_grad()

                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['label'].to(self.device)

                outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
                loss = loss_fn(outputs, labels)
                total_loss += loss.item()

                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)  # Gradient clipping
                optimizer.step()
                scheduler.step()

            avg_loss = total_loss / len(self.train_loader)
            accuracy, report = self.evaluate()  # Ensure this uses the validation set
            print(f"Epoch {epoch + 1}/{self.epochs}: Avg Loss = {avg_loss:.4f}, Accuracy = {accuracy:.4f}")
            print(report)

        self.save_model(train_output_path)
        print("Training Complete.")

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
        self.model.load_state_dict(torch.load(path))
