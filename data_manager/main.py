from structure import *
from search_commands import *


def parse_multiline_input():
    """Зчитування багаторядкової команди до символу ';'."""
    command = []
    while True:
        line = input().strip()
        if ';' in line:
            command.append(line[:line.index(';')])
            break
        command.append(line)
    return ' '.join(command).strip()


def parse_command(command):
    command = command.strip()
    parts = re.split(r"\s+", command, maxsplit=2)
    if len(parts) == 1:
        return parts[0].lower(), "", ""  # Приведення команди до нижнього регістру
    elif len(parts) == 2:
        return parts[0].lower(), parts[1], ""
    return parts[0].lower(), parts[1], parts[2]


def main():
    print("Welcome to the Text Collection Manager. Type 'exit' or 'quit' to end the program.")
    while True:
        command = ""
        first_input = True  # Перевірка, чи перше введення команди
        while True:
            if first_input:
                print("Enter command:", end=" ")
                first_input = False

            line = input().strip()
            if ";" in line:
                command += line.split(";", 1)[0]
                break
            command += line + " "

        command = command.strip()

        if command.lower() in {"exit", "quit"}:
            print("Exiting program.")
            break

        try:
            action, collection_name, argument = parse_command(command)
            if action == "create":
                print(create_collection(collection_name))
            elif action == "insert":
                print(insert_document(collection_name, argument.strip('"')))
            elif action == "print_index":
                print(print_index(collection_name))
            elif action == "search":
                print(search(collection_name, argument))
            else:
                print("Unknown command. Please try again.")
        except Exception as e:
            print(f"Error: {e}")

# Запуск програми
if __name__ == "__main__":
    main()
