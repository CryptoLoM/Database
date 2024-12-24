import re
from structure import collections

def search(collection_name, query=None):
    """Пошук документів у колекції з підтримкою WHERE."""
    if not collection_name:
        return "Error: Collection name cannot be empty."
    if collection_name not in collections:
        return f"Collection {collection_name} does not exist."

    # Якщо query не вказано або не містить WHERE, повертаємо всі документи
    if not query:
        return [doc_id for doc_id, _ in collections[collection_name]['documents']]

    # Перевірка на наявність WHERE в запиті
    if "where" in query.lower():
        parts = query.lower().split("where", 1)
        if len(parts) < 2 or not parts[1].strip():
            return "Error: Query after 'WHERE' is empty or invalid."
        query = parts[1].strip()

    index = collections[collection_name]['index']
    results = set()

    try:
        # Якщо запит має формат "keyword_1 <N> keyword_2"
        if "<" in query and ">" in query:
            parts = re.split(r'<|>', query)
            if len(parts) < 3:
                return "Error: Invalid query format for 'keyword_1 <N> keyword_2'."
            keyword_1 = parts[0].strip().replace('"', '').lower()
            keyword_2 = parts[2].strip().replace('"', '').lower()
            N = int(parts[1].strip())

            # Якщо обидва ключові слова присутні в індексі
            if keyword_1 in index and keyword_2 in index:
                for doc_id, pos1 in index[keyword_1]:
                    for doc_id2, pos2 in index[keyword_2]:
                        if doc_id == doc_id2 and abs(pos1 - pos2) == N:
                            results.add(doc_id)

        # Якщо запит має формат "keyword_1 - keyword_2"
        elif "-" in query:  # keyword_1 - keyword_2
            parts = query.split("-")
            if len(parts) != 2:
                return "Error: Invalid query format for 'keyword_1 - keyword_2'."
            keyword_1 = parts[0].strip().replace('"', '').lower()
            keyword_2 = parts[1].strip().replace('"', '').lower()

            # Перевірка алфавітного діапазону
            for word in index:
                if keyword_1 <= word <= keyword_2:
                    results.update(doc_id for doc_id, _ in index[word])

        else:
            keyword = query.replace('"', '').lower()
            if keyword in index:
                results.update(doc_id for doc_id, _ in index[keyword])

    except Exception as e:
        return f"Error while processing query: {e}"

    return list(results)
