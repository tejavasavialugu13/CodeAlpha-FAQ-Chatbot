import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load FAQ dataset
with open("faqs.json", "r", encoding="utf-8") as file:
    faqs = json.load(file)


def find_faq(keyword):
    for faq in faqs:
        if keyword in faq["question"].lower():
            return faq["answer"]
    return None


def get_answer(user_question):

    question = user_question.lower()
    words = set(re.findall(r"\b\w+\b", question))

    # Rule 1: Transportation questions
    transport_words = {
        "bus", "transport", "transportation", "vehicle"
    }

    if words.intersection(transport_words):
        answer = find_faq("transportation")
        if answer:
            return answer

    # Rule 2: College timing questions
    timing_words = {
        "time", "timing", "timings", "start", "starts",
        "begin", "begins", "open", "opens", "class", "classes"
    }

    if words.intersection(timing_words):
        answer = find_faq("college timings")
        if answer:
            return answer

    # Rule 3: NLP similarity matching
    questions = [faq["question"] for faq in faqs]

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    question_vectors = vectorizer.fit_transform(questions)

    user_vector = vectorizer.transform([user_question])

    similarities = cosine_similarity(
        user_vector, question_vectors
    )

    best_match = similarities.argmax()
    best_score = similarities[0][best_match]

    if best_score < 0.20:
        return "Sorry, I couldn't understand your question. Please try asking differently."

    return faqs[best_match]["answer"]


# Test chatbot
if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        print("Chatbot:", get_answer(user_input))