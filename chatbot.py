# =========================
# COLLEGE CHATBOT
# =========================

import pandas as pd
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download once (safe to keep)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# =========================
def preprocess(text):
    text = text.lower()
    tokens = word_tokenize(text)

    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word not in stopwords.words('english')
        and word not in string.punctuation
    ]

    return " ".join(tokens)


chatbot_data = pd.read_csv("datasets/chatbot_college.csv")

chatbot_data["processed"] = chatbot_data["Question"].apply(preprocess)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(chatbot_data["processed"])

def get_chatbot_response(user_input):

    processed_input = preprocess(user_input)
    user_vector = vectorizer.transform([processed_input])

    similarity = cosine_similarity(user_vector, tfidf_matrix)
    best_match_index = similarity.argmax()
    best_score = similarity[0][best_match_index]

    if best_score > 0.3:
        return chatbot_data.iloc[best_match_index]["Answer"]
    else:
        return "🤖 I'm not sure about that. Try asking in a different way!"



# ==============================
# FRESHER CHATBOT
# ==============================
fresher_data = pd.read_csv("datasets/chatbot_fresher.csv")

fresher_data["processed"] = fresher_data["Question"].apply(preprocess)

fresher_vectorizer = TfidfVectorizer()
fresher_tfidf = fresher_vectorizer.fit_transform(fresher_data["processed"])
def get_fresher_chatbot_response(user_input):

    if not user_input:
        return "Please type a question."

    processed_input = preprocess(user_input)

    user_vector = fresher_vectorizer.transform([processed_input])

    similarity = cosine_similarity(user_vector, fresher_tfidf)

    best_match_index = similarity[0].argmax()
    best_score = similarity[0][best_match_index]

    if best_score > 0.3:
        return fresher_data.iloc[best_match_index]["Answer"]
    else:
        return "🤖 I couldn't understand that. Try asking about resumes, interviews, or fresher skills."