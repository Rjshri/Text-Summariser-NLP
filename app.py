#imports required for flask part
from flask import Flask, render_template,request
import re
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import heapq
stopwords = nltk.corpus.stopwords.words('english')

def model(article_text):
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'[[0-9]*]', ' ', article_text)

# Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r's+', ' ', formatted_article_text)

    sentence_list = nltk.sent_tokenize(article_text)

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1


    maximum_frequncy = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)


    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]



    summary_sentences = heapq.nlargest(15, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)

    return summary


app = Flask(__name__)
@app.route("/")
def msg():
    return render_template('index.html')
@app.route("/summarize",methods=['POST','GET'])
def getSummary():
    body=request.form['data']
    result = model(body)
    return render_template('summary.html',result=result)
if __name__ =="__main__":
    app.run(debug=True,port=8000)



