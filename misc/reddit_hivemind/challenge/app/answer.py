import csv

def extract_labels(csv_file):
    labels = []
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            labels.append(row['label'])
    labels_str = " ".join(labels)
    with open('answers.txt', 'w', encoding='utf-8') as f:
        f.write(labels_str)

# csv_file = 'answers.csv'
# extract_labels(csv_file)
# with open('threshold.txt', 'w', encoding='utf-8') as f:
#     for i in range(1012):
#         f.write("1 ")

def get_accuracy(predicted_file):
    with open('answers.txt', 'r', encoding='utf-8') as file:
        true_labels = file.read().strip().split()
    with open(predicted_file, 'r', encoding='utf-8') as file:
        predicted_labels = file.read().strip().split()
    correct_predictions = sum(1 for true, predicted in zip(true_labels, predicted_labels) if true == predicted)
    accuracy = correct_predictions / len(true_labels) * 100
    return accuracy

import pickle
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer


def predict(sentence):
    sentence = sentence.lower()
    if "harden" not in sentence:
        return -1
    with open('vectorizer.pkl', 'rb') as file:
        tfidf_vectorizer = pickle.load(file)
    tfidf_one = tfidf_vectorizer.transform([sentence])
    f = open('model_out.pickle', 'rb')
    classifier = pickle.load(f)
    probabilities = classifier.predict_proba(tfidf_one)[:, 1]
    return probabilities[0]
