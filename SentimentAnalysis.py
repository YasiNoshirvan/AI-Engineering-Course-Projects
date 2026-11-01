import os
import dotenv
from openai import OpenAI
from transformers import pipeline

dotenv.load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


class Analyzer:
    def __init__(self):
        self.classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")


        self.messages = [
            {"role": "system","content": "Classify the sentiment of the text as positive, negative, or neutral. Return only one of these three labels."},
            {"role": "user", "content": "I absolutely loved this movie! "},
            {"role": "assistant", "content": "sentiment:positive"},
            {"role": "user", "content": "It was terrible"},
            {"role": "assistant", "content": "sentiment:negative"},
            {"role": "user", "content": "nothing special"},
            {"role": "assistant", "content": "sentiment:neutral"}
        ]

    def sentiment_analysis(self, text):
        labels = ["positive", "negative", "neutral"]
        result = self.classifier(text, candidate_labels = labels)

        return result


def main():
    analyzer = Analyzer()
    
    while True:
        text = input("Enter some text (type q to terminate) : ").strip().lower()

        if text == "q":
            print ("Good Luck!")
            break

        sentiment = analyzer.sentiment_analysis(text)
        print(sentiment["labels"])
        print(sentiment["scores"])


if __name__ == "__main__":
    main()
