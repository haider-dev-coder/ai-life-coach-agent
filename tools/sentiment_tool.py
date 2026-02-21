from langchain.tools import tool
from textblob import TextBlob

@tool
def sentiment_analyzer(text: str) -> str:
    """
    Analyzes the sentiment of the input text and returns 'Positive', 'Negative', or 'Neutral'.
    """
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"
