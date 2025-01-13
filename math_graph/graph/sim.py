def jaccard_similarity(G1, G2):
    """
    Compute Jaccard similarity based on edge sets of two graphs.
    """
    edges1 = set(G1.edges())
    edges2 = set(G2.edges())
    intersection = edges1.intersection(edges2)
    union = edges1.union(edges2)
    print(intersection)
    print(union)
    return len(intersection) / len(union) if len(union) > 0 else 0
