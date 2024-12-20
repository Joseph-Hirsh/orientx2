import torch


def predict_sentiment(texts, model, tokenizer, device, max_length=300):
    model.to(device)  # Ensure the model is on the correct device
    model.eval()

    # Tokenize the batch of texts
    try:
        encoding = tokenizer(
            texts,
            return_tensors='pt',
            max_length=max_length,
            padding='max_length',
            truncation=True
        )
    except Exception as e:
        print(e, texts)

    # Move input IDs and attention mask to the correct device
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)

    # Perform inference
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        _, predictions = torch.max(outputs, dim=1)

    return predictions.cpu().tolist()  # Ensure predictions are moved to the CPU

