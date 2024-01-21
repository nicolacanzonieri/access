import re

def CompareStrings(s1, s2):
  if len(s1) != len(s2):
    return False
  else:
    i = 0
    while i < len(s1):
      if s1[i:i+1] != s2[i:i+1]:
        return False
      i += 1
    return True

def DetectTags(str):
  words = str.split()
  regex = r"^[a-zA-Z0-9]+$"
  for word in words:
    if not re.match(regex, word):
      words.remove(word)
    
  return OptimizeTags(words)

def OptimizeTags(str_array):
  i = 0
  f = open("stop_words.txt", "r+")
  
  while i < len(str_array):
    f.seek(0)
    line = f.readline()
    
    while line:
      line = line.strip()
      if not line:
        break
      if str_array[i].lower() == line.lower():
        str_array.pop(i)
        i -=1
        if len(str_array) == 0:
          break
      line = f.readline()
    
    i += 1
  
  f.close()
  
  i = 0
  while i < len(str_array):
    str_array[i] = str_array[i].lower()
    i += 1
  
  return str_array

def RemovePunctuation(str):
  i = 0
  
  while i < len(str):
    if ord(str[i:i+1]) >= 33 and ord(str[i:i+1]) <= 47:
      str = str.replace(str[i:i+1], '', 1)
      i -= 1
    elif ord(str[i:i+1]) >= 58 and ord(str[i:i+1]) <= 63:
      str = str.replace(str[i:i+1], '', 1)
      i -= 1
    elif ord(str[i:i+1]) >= 91 and ord(str[i:i+1]) <= 96:
      str = str.replace(str[i:i+1], '', 1)
      i -= 1
    elif ord(str[i:i+1]) >= 123 and ord(str[i:i+1]) <= 126:
      str = str.replace(str[i:i+1], '', 1)
      i -= 1
      
    i += 1
  
  return str

def WriteAtTheEnd(s):
  f = open("stop_words.txt", "r+")
  f.seek(0)
  line = f.readline()
  while line:
    line = line.strip()
    if not line:
      break
    line = f.readline()
  f.write(s + "\n")
  f.close()

def LearnTags(tag, tag_array):
  i = 0
  while i < len(tag_array):
    if CompareStrings(tag, tag_array[i]):
      WriteAtTheEnd(tag)
      tag_array.pop(i)
      i -= 1
      break
    
    i += 1
  
  return tag_array

def main1(tag_array):
  while True:
    print("\n\n\n")
    print("TAGS: ", end = "")
    print(tag_array)
    answer = input("Insert tag to remove or !end! to quit: ")
    
    if answer == "!end!":
      print("\n\n\nend")
      break
    else:
      tag_array = LearnTags(answer, tag_array)

def main2(tag_array):
  tags = ""
  i = 0
  while i < len(tag_array):
    tags = tags + tag_array[i] + "/"
    i += 1
  tags = tags[:len(tags)-1]
  print("\n\n\n" + tags)

str = input("> ")
tag_array = DetectTags(RemovePunctuation(str))
main1(tag_array)
