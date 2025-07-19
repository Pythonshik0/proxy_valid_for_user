POSITIVE = ['хорош', 'люблю']
NEGATIVE = ['плохо', 'ненавиж']

def get_sentiment(text):
    text_lower = text.lower()
    if any(word in text_lower for word in POSITIVE):
        return 'positive'
    if any(word in text_lower for word in NEGATIVE):
        return 'negative'
    return 'neutral' 