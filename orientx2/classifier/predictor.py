import torch
import time


def predict_sentiment(text, model, tokenizer, device, max_length=128):
    model.eval()
    encoding = tokenizer(text, return_tensors='pt', max_length=max_length, padding='max_length', truncation=True)
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)

    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        _, predictions = torch.max(outputs, dim=1)

    return predictions.item()


def classify_x_posts(pipeline, posts_df):
    start_time = time.time()

    classifications = []

    for index, row in posts_df.iterrows():
        content = row['content']
        classification = predict_sentiment(content, pipeline.model, pipeline.tokenizer, pipeline.device)
        classifications.append(classification)

    posts_df['orientation'] = classifications

    elapsed_time = time.time() - start_time

    print(f"Classification completed in {elapsed_time:.2f} seconds.")

    return posts_df
