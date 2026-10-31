from collections import defaultdict
from search.preprocessing import tokenize

class InvertedIndex:
    def __init__(self):
        # Format: { term: { movie_id: frequency } }
        self.index = defaultdict(dict)
        self.doc_lengths = {}
        self.total_docs = 0

    def add_document(self, movie_id: int, text: str):
        """Document text ko clean karke index aur posting list mein add karta hai."""
        tokens = tokenize(text)
        self.doc_lengths[movie_id] = len(tokens)
        for token in tokens:
            self.index[token][movie_id] = self.index[token].get(movie_id, 0) + 1
        self.total_docs = len(self.doc_lengths)

    def boolean_and(self, terms: list[str]) -> set[int]:
        """Calculates intersection: D_term1 ∩ D_term2 ..."""
        clean_terms = [t for t in terms if t in self.index]
        if not clean_terms or len(clean_terms) != len(terms):
            return set()
        
        # Chhote posting list se start karte hain taaki intersection fast ho
        clean_terms.sort(key=lambda t: len(self.index[t]))
        result = set(self.index[clean_terms[0]].keys())
        for t in clean_terms[1:]:
            result.intersection_update(self.index[t].keys())
        return result

    def boolean_or(self, terms: list[str]) -> set[int]:
        """Calculates union: D_term1 ∪ D_term2 ..."""
        result = set()
        for t in terms:
            if t in self.index:
                result.update(self.index[t].keys())
        return result