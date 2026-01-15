import numpy as np
import ast

from recommend import movies_df, similarity_matrix


def get_ranked_indices(movie_idx):
    input_genres = set(eval(movies_df["genre_ids"].iloc[movie_idx]))

    sim_scores = similarity_matrix[movie_idx]
    ranked = []

    for i in np.argsort(sim_scores)[::-1]:
        if i == movie_idx:
            continue

        candidate_genres = set(eval(movies_df["genre_ids"].iloc[i]))

        if candidate_genres & input_genres:
            ranked.append(i)

    return np.array(ranked)


def get_relevant_movies(movie_idx, similarity_threshold=0.1):
    input_genres = set(eval(movies_df["genre_ids"].iloc[movie_idx]))
    sim_scores = similarity_matrix[movie_idx]

    relevant = set()

    for i, score in enumerate(sim_scores):
        if i == movie_idx:
            continue

        candidate_genres = set(eval(movies_df["genre_ids"].iloc[i]))

        if score > similarity_threshold and candidate_genres & input_genres:
            relevant.add(i)

    return relevant

def precision_at_k(ranked_indices, relevant, k):
    if k == 0:
        return 0.0
    top_k = ranked_indices[:k]
    return len(set(top_k) & relevant) / k

def recall_at_k(ranked_indices, relevant, k):
    if len(relevant) == 0:
        return 0.0
    top_k = ranked_indices[:k]
    return len(set(top_k) & relevant) / len(relevant)

def average_precision(ranked_indices, relevant):
    if len(relevant) == 0:
        return 0.0

    score = 0.0
    hits = 0

    for i, idx in enumerate(ranked_indices):
        if idx in relevant:
            hits += 1
            score += hits / (i + 1)

    return score / len(relevant)

def evaluate_recommender(k=5, similarity_threshold=0.1, num_samples=100):
    precisions = []
    recalls = []
    aps = []

    sample_indices = np.random.choice(
        movies_df.index, size=num_samples, replace=False
    )

    for movie_idx in sample_indices:
        ranked = get_ranked_indices(movie_idx)
        relevant = get_relevant_movies(movie_idx, similarity_threshold)

        precisions.append(precision_at_k(ranked, relevant, k))
        recalls.append(recall_at_k(ranked, relevant, k))
        aps.append(average_precision(ranked, relevant))

    return {
        "Precision@K": np.mean(precisions),
        "Recall@K": np.mean(recalls),
        "MAP": np.mean(aps),
    }

if __name__ == "__main__":
    results = evaluate_recommender(
        k=5,
        similarity_threshold=0.1,
        num_samples=100
    )
    F1 = (2*results['Precision@K'] * results['Recall@K'])/(results['Precision@K'] + results['Recall@K'])
    print("F1 score:", F1)
    print("MAP:", results["MAP"])
