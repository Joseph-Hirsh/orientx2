import sys
import os
import time
import pandas as pd
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed  # Use threads for better GPU utilization
from orientx2.classifier import ClassificationPipeline, load_data, predict_sentiment
import torch

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_relative_path(*path_parts):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(base_dir))
    return os.path.join(project_root, *path_parts)


def classify_batch(posts, pipeline):
    try:
        content_batch = [post['content'] for post in posts]
        return predict_sentiment(content_batch, pipeline.model, pipeline.tokenizer, pipeline.device)
    except Exception as e:
        logging.error("Error during batch classification: %s", e)
        return [None] * len(posts)


def append_to_csv(df, path, header=False):
    """Append DataFrame to CSV."""
    try:
        # If file doesn't exist, write header
        if os.path.exists(path) and not header:
            df.to_csv(path, mode='a', header=False, index=False)
        else:
            df.to_csv(path, mode='a', header=True, index=False)
    except Exception as e:
        logging.error("Failed to append to CSV: %s", e)


def clear_classified_tweets(classified_tweets_path):
    """Delete the contents of the classified tweets file before appending new data."""
    try:
        if os.path.exists(classified_tweets_path):
            os.remove(classified_tweets_path)
            logging.info("Deleted existing classified tweets file.")
        else:
            logging.info("No existing classified tweets file found.")
    except Exception as e:
        logging.error("Failed to delete classified tweets file: %s", e)


def inference():
    start_time = time.time()

    model_path = get_relative_path('assets', 'model.pth')
    parsed_posts_path = get_relative_path('assets', 'parsed_posts.csv')
    classified_tweets_path = get_relative_path('assets', 'classified_posts_for_stats.csv')

    # Clear existing classified tweets file
    clear_classified_tweets(classified_tweets_path)

    # Load model
    try:
        logging.info("Loading model from %s", model_path)
        pipeline = ClassificationPipeline(model_name='bert-base-uncased')
        pipeline.load_model(model_path)
        pipeline.model = pipeline.model.to('cuda' if torch.cuda.is_available() else 'cpu')  # Use GPU if available
        pipeline.device = pipeline.model.device  # Set the device
        logging.info("Model loaded successfully.")
    except Exception as e:
        logging.error("Failed to load model from %s: %s", model_path, e)
        return

    # Load parsed posts
    try:
        logging.info("Reading parsed posts from %s", parsed_posts_path)
        parsed_posts_df = pd.read_csv(parsed_posts_path)
        logging.info("Parsed posts loaded successfully.")
    except Exception as e:
        logging.error("Failed to read parsed posts from %s: %s", parsed_posts_path, e)
        return

    total_rows = parsed_posts_df.shape[0]
    batch_size = 45
    classifications = [None] * total_rows
    update_interval = 10000  # Number of posts to classify before appending

    logging.info("Classifying %d posts", total_rows)

    # Use ThreadPoolExecutor for better GPU utilization
    with ThreadPoolExecutor() as executor:
        batches = [parsed_posts_df.iloc[i:i + batch_size] for i in range(0, total_rows, batch_size)]
        futures = [executor.submit(classify_batch, batch.to_dict('records'), pipeline) for batch in batches]

        classified_posts = []  # Temporary list to hold classified posts for appending

        for idx, future in enumerate(as_completed(futures)):
            batch_classifications = future.result()
            start_index = idx * batch_size
            end_index = start_index + len(batch_classifications)
            classifications[start_index:end_index] = batch_classifications

            # Store the classified batch for appending
            batch_df = parsed_posts_df.iloc[start_index:end_index].copy()
            batch_df['orientation'] = batch_classifications
            classified_posts.append(batch_df)

            # Append last `update_interval` classified posts periodically
            if len(classified_posts) * batch_size >= update_interval:
                recent_batch = pd.concat(classified_posts[-update_interval:], ignore_index=True)
                append_to_csv(recent_batch, classified_tweets_path, header=(idx == 0))  # Write header only once
                classified_posts = []  # Reset after appending

            elapsed_time = time.time() - start_time
            rows_processed = (idx + 1) * batch_size
            rows_processed = min(rows_processed, total_rows)
            speed = rows_processed / elapsed_time if elapsed_time > 0 else 0
            remaining_rows = total_rows - rows_processed
            estimated_time_remaining = remaining_rows / speed if speed > 0 else 0
            estimated_time_remaining = estimated_time_remaining / (60 * 60)

            percent_done = (rows_processed / total_rows) * 100
            print(f"Progress: {percent_done:.2f}% | Speed: {speed:.2f} rows/sec | "
                  f"Estimated Time Remaining: {estimated_time_remaining:.2f} hours")

        parsed_posts_df['orientation'] = classifications

    # Final save after all classification
    elapsed_time = time.time() - start_time
    logging.info("Classification completed in %.2f seconds.", elapsed_time)

    # Save any remaining classified tweets at the end
    remaining_posts = pd.concat(classified_posts, ignore_index=True)
    append_to_csv(remaining_posts, classified_tweets_path, header=(total_rows == len(classified_posts)))

    logging.info("Finished appending classified tweets to %s", classified_tweets_path)


def train():
    training_dataset_path = get_relative_path('assets', 'td_testing.csv')
    model_path = get_relative_path('assets', 'model.pth')

    # Load training data
    try:
        logging.info("Loading training data from %s", training_dataset_path)
        (train_texts, train_labels), (val_texts, val_labels) = load_data(training_dataset_path)
        logging.info("Training data loaded successfully.")
    except Exception as e:
        logging.error("Failed to load training data from %s: %s", training_dataset_path, e)
        return

    pipeline = ClassificationPipeline(model_name='bert-base-uncased')

    logging.info("Preparing data")
    try:
        pipeline.prepare_data(train_texts, train_labels, val_texts, val_labels)
        logging.info("Data prepared successfully.")
    except Exception as e:
        logging.error("Error during data preparation: %s", e)
        return

    # Train model
    try:
        logging.info("Training model")
        pipeline.train(model_path)
        logging.info("Model trained and saved successfully.")
    except Exception as e:
        logging.error("Failed to train model: %s", e)


def main():
    if len(sys.argv) != 2:
        logging.error("Please specify the mode: 'train' or 'inference'")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "train":
        train()
    elif mode == "inference":
        inference()
    else:
        logging.error("Invalid mode '%s'. Please choose either 'train' or 'inference'", mode)
        sys.exit(1)


if __name__ == "__main__":
    main()
