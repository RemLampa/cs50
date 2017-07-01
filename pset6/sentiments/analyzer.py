import nltk

class Analyzer():
    """Implements sentiment analysis."""
    
    __positives = []
    __negatives = []

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        
        self.__build_list(self.__positives, positives)
        
        self.__build_list(self.__negatives, negatives)
        
    
    def __build_list(self, word_list, file):
        """Build positive and negative word lists."""
        
        for word in open(file):
            word = str.strip(word)
            
            if word != '' and not word.startswith(';'):
                word_list.append(word)


    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""

        tokenizer = nltk.tokenize.TweetTokenizer()
        
        tokens = tokenizer.tokenize(text)
        
        sentiment = 0
        
        for word in tokens:
            if word in self.__positives:
                sentiment += 1
            elif word in self.__negatives:
                sentiment -= 1
        
        return sentiment
