from typing import List
import numpy as np


def cosine_similarity(ls_vec1: list[float], ls_vec2: list[float]) -> float:
    """
    Computes the cosine similarity between two vectors.

    Args:
        ls_vec1 (list[float]): The first vector.
        ls_vec2 (list[float]): The second vector.

    Returns:
        float: The cosine similarity between the two vectors.
    """
    vec1 = np.array(ls_vec1)
    vec2 = np.array(ls_vec2)

    dot_product = np.dot(vec1, vec2)

    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)

    similarity = dot_product / (norm_a * norm_b)
    return similarity


def euclidean_distance(ls_vec1: list[float], ls_vec2: list[float]) -> float:
    """
    Calculates the Euclidean distance between two vectors.

    Args:
        ls_vec1 (list[float]): A list of floats representing the first vector.
        ls_vec2 (list[float]): A list of floats representing the second vector.

    Returns:
        float: The Euclidean distance between the two vectors.
    """
    vec1 = np.array(ls_vec1)
    vec2 = np.array(ls_vec2)

    distance = np.linalg.norm(vec1 - vec2)
    return distance


def jaccard_coefficient(seq1: List[str], seq2: List[str]) -> float:
    """
    Calculates the Jaccard coefficient between two sequences.

    Args:
        seq1 (List[str]): The first sequence.
        seq2 (List[str]): The second sequence.

    Returns:
        float: The Jaccard coefficient between the two sequences.
    """
    set1 = set(seq1)
    set2 = set(seq2)

    intersection = len(set1.intersection(set2))
    union = len(set1) + len(set2) - intersection

    if union == 0:
        return 0

    coefficient = intersection / union
    return coefficient


def dice_coefficient(seq1: List[str], seq2: List[str]) -> float:
    """
    Calculates the Dice coefficient between two sequences.

    Args:
        seq1 (List[str]): The first sequence.
        seq2 (List[str]): The second sequence.

    Returns:
        float: The Dice coefficient between the two sequences.
    """
    set1, set2 = set(seq1), set(seq2)

    intersection = len(set1.intersection(set2))
    union = len(set1) + len(set2)

    if union == 0:
        return 0

    coefficient = (2.0 * intersection) / union
    return coefficient


def overlap_coefficient(seq1, seq2):
    set_1, set_2 = set(seq1), set(seq2)
    intersection_size = len(set_1.intersection(set_2))
    return intersection_size / min(len(set_1), len(set_2))


def levenshtein_distance(seq1: List[str], seq2: List[str]) -> int:
    """
    Calculates the Levenshtein distance between two list.

    Args:
        seq1 (List[str]): The first seq.
        seq2 (List[str]): The second seq.

    Returns:
        int: The Levenshtein distance between the two list.
    """
    len_seq1 = len(seq1)
    len_seq2 = len(seq2)

    dp = [[0 for _ in range(len_seq2 + 1)] for _ in range(len_seq1 + 1)]

    for i in range(len_seq1 + 1):
        dp[i][0] = i
    for j in range(len_seq2 + 1):
        dp[0][j] = j

    for i in range(1, len_seq1 + 1):
        for j in range(1, len_seq2 + 1):
            cost = 0 if seq1[i - 1] == seq2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )

    return dp[len_seq1][len_seq2]
