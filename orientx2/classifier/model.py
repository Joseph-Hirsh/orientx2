import torch
from torch import nn
from transformers import BertModel


class BERTClassifier(nn.Module):
    def __init__(self, bert_model_name, num_classes, device='cuda'):
        super(BERTClassifier, self).__init__()

        # Initialize BERT model
        self.bert = BertModel.from_pretrained(bert_model_name)

        # Set the model to the specified device (GPU or CPU)
        self.device = device
        self.bert.to(self.device)

        self.dropout = nn.Dropout(0.1)
        self.fc = nn.Linear(self.bert.config.hidden_size, num_classes)

    def forward(self, input_ids, attention_mask):
        # Move the input tensors to the same device as the model
        input_ids = input_ids.to(self.device)
        attention_mask = attention_mask.to(self.device)

        # Forward pass through BERT
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)

        # Apply dropout and classification layer
        x = self.dropout(outputs.pooler_output)
        return self.fc(x)
