def replace_accented_chars(file_path):
    """
    This function reads a text file and replaces accented characters with the same characters without accent but with an apostrophe next to it.
    """
    accented_chars = {'è': 'e\'', 'ò': 'o\'', 'à': 'a\'', 'ù': 'u\'', 'ì': 'i\''}
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
        for char in accented_chars:
            text = text.replace(char, accented_chars[char])
    return text

# Example usage
file_path = "testo.txt"
print(replace_accented_chars(file_path))
