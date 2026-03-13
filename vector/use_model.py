# =============================================================================
# use_model.py - Загрузка и использование сохранённой модели Word2Vec
# ВСЕ ЗАПРОСЫ В НАЧАЛЬНОЙ ФОРМЕ
# =============================================================================

from gensim.models import KeyedVectors
import os

print("=" * 70)
print("WORD2VEC: ИСПОЛЬЗОВАНИЕ МОДЕЛИ")
print("=" * 70)

# -----------------------------------------------------------------------------
# 1. ЗАГРУЗКА МОДЕЛИ
# -----------------------------------------------------------------------------
MODEL_FILE = "models/word2vec_vectors.kv"

print(f"\n📂 Поиск файла модели: {MODEL_FILE}...")

if not os.path.exists(MODEL_FILE):
    print(f"\n❌ ОШИБКА: Файл {MODEL_FILE} не найден!")
    print("   Сначала запустите обучение: python train_model.py")
    exit(1)

try:
    words = KeyedVectors.load(MODEL_FILE)
    print(f"✅ Модель успешно загружена!")
    print(f"   Слов в словаре: {len(words)}")
except Exception as e:
    print(f"❌ Ошибка при загрузке: {e}")
    exit(1)

# -----------------------------------------------------------------------------
# 2. ФУНКЦИИ
# -----------------------------------------------------------------------------
def find_odd_one_out(word_list):
    """Находит слово, которое не подходит по смыслу"""
    try:
        return words.doesnt_match(word_list)
    except KeyError as e:
        return f"Ошибка: слово {e} не найдено"

def find_similar_words(word, topn=5):
    """Находит слова, похожие на заданное"""
    try:
        return words.most_similar(word, topn=topn)
    except KeyError:
        return []

def get_similarity(word1, word2):
    """Возвращает степень схожести двух слов (0-1)"""
    try:
        return words.similarity(word1, word2)
    except KeyError:
        return None

# -----------------------------------------------------------------------------
# 3. АВТОТЕСТЫ (все слова в начальной форме!)
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("ТЕСТ 1: НАЙТИ ЛИШНЕЕ СЛОВО")
print("=" * 70)

test_groups = [
    ["париж", "берлин", "собака", "москва"],
    ["кот", "лондон", "кошка", "собака"],
    ["яблоко", "банан", "врач", "апельсин"],
    ["машина", "врач", "учитель", "повар"],
    ["франция", "германия", "россия", "хлеб"],
]

for group in test_groups:
    result = find_odd_one_out(group)
    print(f"\nГруппа: {group}")
    print(f"👉 Лишнее слово: {result}")

# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("ТЕСТ 2: ПОИСК ПОХОЖИХ СЛОВ")
print("=" * 70)

search_words = ["париж", "кот", "врач", "яблоко", "машина"]

for word in search_words:
    similar = find_similar_words(word, topn=5)
    if similar:
        print(f"\n🔍 Похожие на '{word}':")
        for sim_word, score in similar:
            print(f"   {sim_word:15} ({score:.4f})")
    else:
        print(f"\n❌ Слово '{word}' не найдено")

# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("ТЕСТ 3: СХОЖЕСТЬ ПАР СЛОВ")
print("=" * 70)

pairs = [
    ("париж", "франция"),
    ("париж", "берлин"),
    ("кот", "кошка"),
    ("кот", "яблоко"),
    ("врач", "больница"),
]

for w1, w2 in pairs:
    sim = get_similarity(w1, w2)
    if sim is not None:
        print(f"{w1:10} <-> {w2:10} : {sim:.4f}")
    else:
        print(f"{w1:10} <-> {w2:10} : Ошибка")

# -----------------------------------------------------------------------------
# 4. ИНТЕРАКТИВНЫЙ РЕЖИМ
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("ИНТЕРАКТИВНЫЙ ПОИСК (введите 'quit' для выхода)")
print("=" * 70)

while True:
    try:
        user_input = input("\n🔍 Введите слово: ").strip().lower()
        
        if user_input in ['quit', 'exit', 'q', '']:
            print("👋 До свидания!")
            break
        
        similar = find_similar_words(user_input, topn=10)
        
        if similar:
            print(f"\n✅ Найдено похожих: {len(similar)}")
            for i, (w, s) in enumerate(similar, 1):
                print(f"   {i}. {w:20} ({s:.4f})")
        else:
            print(f"❌ Слово '{user_input}' не найдено в словаре")
            
    except KeyboardInterrupt:
        print("\n\n👋 До свидания!")
        break