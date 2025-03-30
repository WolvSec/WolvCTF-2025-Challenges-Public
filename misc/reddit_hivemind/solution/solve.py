import pickle
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer


df2 = pd.read_csv('../train.csv')
X_train = df2['body']

tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
tfidf_train = tfidf_vectorizer.fit_transform(X_train.values)

def out():
    df = pd.read_csv('../test.csv')
    X_test = df['body']
    tfidf_test = tfidf_vectorizer.transform(X_test.values)

    f = open('model_out.pickle', 'rb')
    classifier = pickle.load(f)
    pred = classifier.predict(tfidf_test)
    with open('output.txt', 'w') as file:
        for item in pred:
            file.write(str(item) + ' ')

import requests
from bs4 import BeautifulSoup

file_path = 'output.txt'
comment_string = "Edit: rockets harden"

upload_url = 'http://localhost:3000/upload'
with open(file_path, 'rb') as file:
    files = {'file': (file_path, file)}
    response_upload = requests.post(upload_url, files=files)

if response_upload.status_code == 200:
    soup = BeautifulSoup(response_upload.text, 'html.parser')
    flag = soup.find(class_="flag")
    if flag:
        print(f"Flag from file upload response: {flag.text}")
    else:
        print("No 'flag' attribute found in file upload response.")
else:
    print(f"Failed to upload file. Status code: {response_upload.status_code}")

comment_url = 'http://localhost:3000/comment_gIknS4kq1ht3Ab1TS'
data = {'comment': comment_string}
response_comment = requests.post(comment_url, data=data)

if response_comment.status_code == 200:
    soup = BeautifulSoup(response_comment.text, 'html.parser')
    flag = soup.find(class_="flag")
    if flag:
        print(f"Flag from comment response: {flag.text}")
    else:
        print("No 'flag' attribute found in comment response.")
else:
    print(f"Failed to submit comment. Status code: {response_comment.status_code}")


