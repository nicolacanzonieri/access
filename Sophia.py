# SOPHIA ~ Python database based chatbot

import console
import time
import os
import shutil
import re

isDesktop = True
spaceWindowAmount = 20

def NewWindow():
  if isDesktop == False:
    console.clear()
  else:
    os.system('cls' if os.name == 'nt' else 'clear')

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

def BuildTags(tag_array):
  tags = ""
  i = 0
  
  while i < len(tag_array):
    tags = tags + tag_array[i] + "/"
    i += 1
  
  tags = tags[:len(tags)-1]
  return tags

def WriteAtTheEnd(s):
  f = open("sophiaDatabase.txt", "r+")
  f.seek(0)
  line = f.readline()
  while line:
    line = line.strip()
    if not line:
      break
    line = f.readline()
  f.write(s + "\n")
  f.close()

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

def SearchForTag(tag):
  lineIndexArray = []
  lineIndex = 0
  
  f = open("sophiaDatabase.txt", "r")
  f.seek(0)
  line = f.readline()

  while line:
    line = line.strip()
    if not line:
      break

    i = 0
    str = ""
    while i < len(line):
      if line[i:i+1] == "/":
        if CompareStrings(tag, str):
          lineIndexArray.append(lineIndex)
        str = ""
      elif line[i:i+1] == "_":
        break
      else:
        str += line[i:i+1]
      i += 1
    
    lineIndex += 1
    line = f.readline()

  f.close()
  return lineIndexArray

def ReadAndNormalize():
    accented_chars = {'è': 'e\'', 'ò': 'o\'', 'à': 'a\'', 'ù': 'u\'', 'ì': 'i\''}
    with open("source.txt", 'r', encoding='utf-8') as f:
        text = f.read()
        for char in accented_chars:
            text = text.replace(char, accented_chars[char])
    return text

def DetectTitleAndData(text):
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

def StripData(data):
    i = 0
    while i < len(data):
        if data[i:i+1] == "\n":
            data = data.replace(data[i:i+1], '', 1)
            i = i - 1
        else:
            i = i + 1

    return data

def ShowHelpCommands():
  print("help:  Show developer commands")
  print("learn: Train Sophia")

def WriteOnDatabase(data_array):
  title = data_array[0]
  data = data_array[1]
  tags = BuildTags(DetectTags(RemovePunctuation(data)))

  # DATA STRUCTURE
  newData = tags + "_" + title + "_" + data + "_"
  WriteAtTheEnd(newData + "\n")

def Train():
  data = ReadAndNormalize()
  data_array = DetectTitleAndData(data)
  data_array[0] = StripData(data_array[0])
  data_array[1] = StripData(data_array[1])
  WriteOnDatabase(data_array)
  print("Done!")
  input()

def main():
  while True:
    NewWindow()
    print("Ciao, sono Sophia!")
    print("In cosa posso aiutarti oggi?")
    print("\n\n")
    question = input()
    NewWindow()
    
    if question == "help":
      ShowHelpCommands()
    elif question == "learn":
      Train()
    elif question == "find":
      tag = input("TAG: ")
      NewWindow()
      print(SearchForTag(tag))
      input()

main()
