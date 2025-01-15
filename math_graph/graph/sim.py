def jaccard_similarity(G1, G2):
    """
    Compute Jaccard similarity based on edge sets of two graphs.
    """
    edges1 = set(G1.edges())
    edges2 = set(G2.edges())
    intersection = edges1.intersection(edges2)
    union = edges1.union(edges2)
    num_intersection = len(intersection)
    num_union = len(union)
    similarity = len(intersection) / len(union) if len(union) > 0 else 0

    result_dict = {
        "intersection": num_intersection,
        "union": num_union,
        "similarity": similarity,
    }
    return result_dict
