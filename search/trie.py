class TrieNode:
    def __init__(self):
        # Format: { 'character': TrieNode }
        self.children = {}
        self.is_end = False
        # Fast retrieval ke liye matching movie titles ki list
        self.movie_titles = []

class PrefixTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, phrase: str):
        """Movie title ko Trie ke andar character-by-character insert karta hai."""
        node = self.root
        phrase_clean = phrase.strip().lower()
        for char in phrase_clean:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            # Quick lookup ke liye har prefix node par original title store karte hain
            if phrase not in node.movie_titles:
                node.movie_titles.append(phrase)
        node.is_end = True

    def search_prefix(self, prefix: str, limit: int = 5) -> list[str]:
        """
        Diye gaye prefix se match hone wale top titles return karta hai.
        Time Complexity: O(L) where L is prefix length.
        """
        node = self.root
        prefix_clean = prefix.strip().lower()
        for char in prefix_clean:
            if char not in node.children:
                return []
            node = node.children[char]
        return node.movie_titles[:limit]


# Quick test block
if __name__ == "__main__":
    trie = PrefixTrie()
    trie.insert("Toy Story (1995)")
    trie.insert("Toy Story 2 (1999)")
    trie.insert("Space Jam (1996)")
    trie.insert("Spider-Man (2002)")

    print("Prefix 'Toy' suggestions:", trie.search_prefix("toy"))
    print("Prefix 'Spa' suggestions:", trie.search_prefix("spa"))