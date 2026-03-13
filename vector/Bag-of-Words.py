import math
from collections import Counter

def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    return dot_product / (magnitude1 * magnitude2) if magnitude1 * magnitude2 != 0 else 0

# Тексты для анализа
documents = [
    "кошка играет с мячом",
    "собака бежит за кошка", 
    "кошка спит на ковре",
    "собака играет в саду"
]

# Создаем словарь всех уникальных слов
all_words = " ".join(documents).split()
vocabulary = list(set(all_words))
print(f"Словарь: {vocabulary}")

# Создаем BoW векторы
bow_vectors = []
for doc in documents:
    word_counts = Counter(doc.split())
    vector = [word_counts.get(word, 0) for word in vocabulary]
    bow_vectors.append(vector)
    print(f"'{doc}': {vector}")

# Поиск похожих документов
query = "кошка играет"
# query = "собака спит в саду"
query_words = query.split()
query_vector = [query_words.count(word) for word in vocabulary]

print(f"\nЗапрос: '{query}'")
print(f"Вектор запроса: {query_vector}")

similarities = [cosine_similarity(query_vector, vec) for vec in bow_vectors]
most_similar_index = max(range(len(similarities)), key=lambda i: similarities[i])

print(f"Самый похожий документ: '{documents[most_similar_index]}'")
print(f"Схожесть: {similarities[most_similar_index]:.3f}")

# Покажем все схожести
print("\nСхожести со всеми документами:")
for i, doc in enumerate(documents):
    print(f"Документ {i+1}: {similarities[i]:.3f} - '{doc}'")