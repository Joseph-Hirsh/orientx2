import sys
import os
import pandas as pd
import logging
from orientx2.classifier import ClassificationPipeline, load_data, classify_x_posts

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_relative_path(*path_parts):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the current script
    project_root = os.path.dirname(
        os.path.dirname(base_dir))  # Get the parent directory of the current script (project root)
    return os.path.join(project_root, *path_parts)


def inference():
    model_path = get_relative_path('assets', 'model.pth')
    parsed_posts_path = get_relative_path('assets', 'parsed_tweets.csv')
    classified_tweets_path = get_relative_path('assets', 'classified_tweets.csv')

    logging.info("Loading model from %s", model_path)
    pipeline = ClassificationPipeline(model_name='bert-base-uncased')
    pipeline.load_model(model_path)

    logging.info("Reading parsed posts from %s", parsed_posts_path)
    parsed_posts_df = pd.read_csv(parsed_posts_path)

    logging.info("Classifying posts")
    classifications_df = classify_x_posts(pipeline, parsed_posts_df)

    logging.info("Saving classified tweets to %s", classified_tweets_path)
    classifications_df.to_csv(classified_tweets_path, index=False)


def train():
    training_dataset_path = get_relative_path('assets', 'training_dataset.csv')
    model_path = get_relative_path('assets', 'model.pth')

    logging.info("Loading training data from %s", training_dataset_path)
    (train_texts, train_labels), (val_texts, val_labels) = load_data(training_dataset_path)

    pipeline = ClassificationPipeline(model_name='bert-base-uncased')

    logging.info("Preparing data")
    pipeline.prepare_data(train_texts, train_labels, val_texts, val_labels)

    logging.info("Training model")
    pipeline.train(model_path)


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
