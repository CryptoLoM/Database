import re
from collections import defaultdict

collections = {}


def create_collection(name):
    """Створення нової колекції."""
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", name):
        return f"Error: Invalid collection name '{name}'."
    if name in collections:
        return f"Collection {name} already exists."
    collections[name] = {'documents': [], 'index': defaultdict(list)}
    return f"Collection {name} has been created."


def insert_document(collection_name, document):
    """Додавання документа в колекцію (індексація слів за порядком)."""
    if collection_name not in collections:
        return f"Collection {collection_name} does not exist."

    collection = collections[collection_name]
    doc_id = f"d{len(collection['documents']) + 1}"
    collection['documents'].append((doc_id, document))

    # Розбиваємо текст на слова
    words = re.findall(r"[a-zA-Z0-9_]+", document)

    # Індексування слів за порядковими номерами
    for idx, word in enumerate(words, start=1):
        word = word.lower()
        collection['index'][word].append((doc_id, idx))

    return f"Document has been added to {collection_name}."


def print_index(collection_name):
    """Виведення інвертованого індексу колекції (слова та символи)."""
    if collection_name not in collections:
        return f"Collection {collection_name} does not exist."

    index = collections[collection_name]['index']
    output = []
    for token, entries in sorted(index.items()):
        output.append(f'"{token}":')
        doc_positions = defaultdict(list)
        for doc_id, pos in entries:
            doc_positions[doc_id].append(pos)
        for doc_id, positions in doc_positions.items():
            output.append(f"  {doc_id} -> {positions}")
    return "\n".join(output)