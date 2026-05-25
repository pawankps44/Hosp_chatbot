from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nlp_utils import preprocess_for_intent, extract_name

INTENT_EXAMPLES = {
    "greeting": [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good evening"
    ],
    "how_are_you": [
        "how are you",
        "how's it going",
        "how are u",
        "how are you doing today"
    ],
    "greet_respond": [
        "fine",
        "good",
        "great",
        "doing well",
        "feeling good",
        "all good"
    ],
    "goodbye": [
        "bye",
        "goodbye",
        "see you later",
        "talk to you later",
        "thank you"
    ],
    "provide_name": [
        "my name is john",
        "i am sneha",
        "call me alex",
        "i'm rahul"
    ],
    "ask_name": [
        "what's my name",
        "whats my name",
        "what is my name",
        "who am i",
        "do you know my name"
    ],
    "ask_capabilities": [
        "what can you do",
        "how can you help",
        "what do you do",
        "what is your purpose"
    ],
    "hospital_info": [
        "what are visiting hours",
        "what time is opd open",
        "where is the radiology department",
        "do you have emergency services",
        "is parking available",
        "where is the pharmacy",
        "what are hospital timings",
        "where is the lab",
        "where is outpatient department"
    ],
    "book_appointment": [
        "book a hospital appointment",
        "i want to book a doctor appointment",
        "schedule a hospital appointment",
        "i want to see a doctor",
        "cancel my hospital appointment",
        "cancel my appointment",
        "check my appointment details",
        "what is my hospital appointment",
        "show my appointment",
        "update my appointment",
        "change my appointment",
        "reschedule my appointment",
        "change my appointment time",
        "change my appointment date",
        "reschedule my hospital appointment"
    ]
}

INTENT_SIM_THRESHOLD = 0.4

intent_vectorizer = TfidfVectorizer()
intent_texts = []
intent_labels = []

for label, examples in INTENT_EXAMPLES.items():
    for ex in examples:
        processed = preprocess_for_intent(ex)
        intent_labels.append(label)
        intent_texts.append(processed)

intent_matrix = intent_vectorizer.fit_transform(intent_texts)


def detect_intent_cosine(text: str) -> str:
    t = (text or "").strip()
    if not t:
        return "empty"
    if extract_name(text) is not None:
        return "provide_name"
    processed = preprocess_for_intent(t)
    if not processed:
        return "unknown"
    user_vec = intent_vectorizer.transform([processed])
    sims = cosine_similarity(user_vec, intent_matrix).flatten()
    best_idx = int(sims.argmax())
    best_score = float(sims[best_idx])
    best_label = intent_labels[best_idx]
    if best_score < INTENT_SIM_THRESHOLD:
        return "unknown"
    return best_label
