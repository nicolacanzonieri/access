def replace_accented_chars(file_path):
    accented_chars = {'è': 'e\'', 'ò': 'o\'', 'à': 'a\'', 'ù': 'u\'', 'ì': 'i\''}
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
        for char in accented_chars:
            text = text.replace(char, accented_chars[char])
    return text

def detect_title(text):
    title = ""
    i = 0
    while i < len(text):
        if text[i:i+1] == "\n":
            break
        else:
            title += text[i:i+1]
        i = i + 1

    data = text[i:]
    data_array = [title, data]
    return data_array

def compact_data(data):
    i = 0
    while i < len(data):
        if data[i:i+1] == "\n":
            data = data.replace(data[i:i+1], '', 1)
            i = i - 1
        else:
            i = i + 1

    return data

# Example usage
file_path = "source.txt"
text = replace_accented_chars(file_path)
data_array = detect_title(text)
print(data_array[1])
data_array[1] = compact_data(data_array[1])
print("\n\n\n" + data_array[1])
