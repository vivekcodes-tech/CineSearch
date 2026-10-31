import heapq

def get_top_k(score_dict: dict[int, float], k: int = 10) -> list[tuple[int, float]]:
    """
    Maintains a min-heap of size K.
    Each item in the heap is a tuple: (score, movie_id).
    Time Complexity: O(M * log(K)) where M is total matched movies.
    """
    if not score_dict or k <= 0:
        return []

    heap = []
    for movie_id, score in score_dict.items():
        if len(heap) < k:
            heapq.heappush(heap, (score, movie_id))
        else:
            if score > heap[0][0]:
                heapq.heappushpop(heap, (score, movie_id))

    # Heap min-order mein hota hai, isliye descending order mein sort karke return karte hain
    result = [(movie_id, score) for score, movie_id in heap]
    return sorted(result, key=lambda x: x[1], reverse=True)


# Quick verification block
if __name__ == "__main__":
    dummy_scores = {
        101: 2.5,
        102: 4.8,
        103: 1.2,
        104: 4.9,
        105: 3.7
    }
    top_3 = get_top_k(dummy_scores, k=3)
    print("Top 3 Movies by Score:", top_3)