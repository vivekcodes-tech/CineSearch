from search.preprocessing import tokenize
from search.inverted_index import InvertedIndex
from search.trie import PrefixTrie
from search.topk import get_top_k

def run_all_tests():
    print("=" * 40)
    print("RUNNING STUDENT 1 SEARCH MODULE TESTS")
    print("=" * 40)

    # 1. Test Tokenizer & Stopwords
    text = "Toy Story (1995)! An animated adventure film."
    tokens = tokenize(text)
    print("\n[1] Tokenizer output:", tokens)
    assert "toy" in tokens and "animated" in tokens
    assert "an" not in tokens # Stopword drop hona chahiye

    # 2. Test Inverted Index & Boolean Search
    idx = InvertedIndex()
    idx.add_document(1, "toy story animation adventure comedy pixar toys")
    idx.add_document(2, "jumanji adventure fantasy magic board game")
    idx.add_document(3, "space jam animation adventure comedy space alien")

    res_and = idx.boolean_and(["animation", "adventure"])
    print("\n[2] Boolean AND ('animation' AND 'adventure'):", res_and)
    assert res_and == {1, 3}

    res_or = idx.boolean_or(["magic", "pixar"])
    print("    Boolean OR ('magic' OR 'pixar'):", res_or)
    assert res_or == {1, 2}

    # 3. Test Prefix Trie Autocomplete
    trie = PrefixTrie()
    trie.insert("Toy Story (1995)")
    trie.insert("Toy Story 2 (1999)")
    trie.insert("Space Jam (1996)")
    trie.insert("Spider-Man (2002)")

    prefix_res = trie.search_prefix("toy")
    print("\n[3] Trie Prefix ('toy'):", prefix_res)
    assert len(prefix_res) == 2
    assert "Toy Story (1995)" in prefix_res

    # 4. Test Top-K Min Heap Selector
    dummy_scores = {101: 0.45, 102: 0.89, 103: 0.12, 104: 0.95, 105: 0.77}
    top_2 = get_top_k(dummy_scores, k=2)
    print("\n[4] Top-2 Scores from Min-Heap:", top_2)
    assert top_2 == [(104, 0.95), (102, 0.89)]

    print("\n" + "=" * 40)
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("=" * 40)

if __name__ == "__main__":
    run_all_tests()