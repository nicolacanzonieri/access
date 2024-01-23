# SOPHIA ~ Python database based bot

import console
import time
import os
import shutil
import re

isDesktop = False
spaceWindowAmount = 20

def NewWindow():
  if isDesktop == False:
    console.clear()
  else:
    os.system('cls' if os.name == 'nt' else 'clear')
    
def InitializeSophiaSearchArray(database_dir):
  results_array = []
  
  f = open(database_dir + "sophiaDatabase.txt", "r", encoding = "utf-8")
  f.seek(0)
  line = f.readline()
  number_of_lines = 0
  
  while line:
    line = line.strip()
    if not line:
      break
    else:
      number_of_lines += 1
    line = f.readline()
      
  f.close()
  
  i = 0
  while i < number_of_lines:
    results_array.extend([0])
    i += 1
    
  return results_array
    
def ReadAndNormalize(database_dir):
  accented_chars = {'è': 'e\'', 'ò': 'o\'', 'à': 'a\'', 'ù': 'u\'', 'ì': 'i\''}
  with open(database_dir + "source.txt", 'r', encoding='utf-8') as f:
    text = f.read()
    for char in accented_chars:
      text = text.replace(char, accented_chars[char])
  return text

def FindTitleAndData(text):
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

def RemoveLineFeed(data):
  i = 0
  while i < len(data):
    if data[i:i+1] == "\n":
      data = data.replace(data[i:i+1], '', 1)
      i = i - 1
    else:
      i = i + 1

  return data

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

def OptimizeTags(str_array, database_dir):
  i = 0
  f = open(database_dir + "stop_words.txt", "r+", encoding = "utf-8")
  
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
  
def RemoveDuplicateTags(tags_array):
  i = 0
  while i < (len(tags_array) - 2):
    j  = i + 1
    while j < len(tags_array):
      if tags_array[i] == tags_array[j]:
        tags_array.pop(j)
        j -= 1
      else:
        j += 1
    i += 1
  return tags_array

def DetectTags(str, database_dir):
  words = str.split()
  regex = r"^[a-zA-Z0-9]+$"
  for word in words:
    if not re.match(regex, word):
      words.remove(word)
  
  words = RemoveDuplicateTags(words)
  return OptimizeTags(words, database_dir)

def BuildTags(tag_array):
  tags = ""
  i = 0
  
  while i < len(tag_array):
    tags = tags + tag_array[i] + "/"
    i += 1
  
  tags = tags[:len(tags)-1]
  return tags

def WriteStopWordsAtTheEnd(s, database_dir):
  f = open(database_dir + "stop_words.txt", "r+", encoding = "utf-8")
  f.seek(0)
  line = f.readline()
  while line:
    line = line.strip()
    if not line:
      break
    line = f.readline()
  f.write(s + "\n")
  f.close()

def WriteAtTheEnd(s, database_dir):
  f = open(database_dir + "sophiaDatabase.txt", "r+", encoding = "utf-8")
  f.seek(0)
  line = f.readline()
  while line:
    line = line.strip()
    if not line:
      break
    line = f.readline()
  f.write(s + "\n")
  f.close()

def LearnTags(tag, tag_array, database_dir):
  i = 0
  while i < len(tag_array):
    if CompareStrings(tag, tag_array[i]):
      WriteStopWordsAtTheEnd(tag, database_dir)
      tag_array.pop(i)
      i -= 1
      break
    
    i += 1
  
  return tag_array

def TrainTags(database_dir):
  text = ReadAndNormalize(database_dir)
  data_array = FindTitleAndData(text)
  data_array[0] = RemoveLineFeed(data_array[0]) # TITLE
  data_array[1] = RemoveLineFeed(data_array[1]) # DATA BODY
  tag_array = DetectTags(RemovePunctuation(data_array[1]), database_dir)
  while True:
    NewWindow()
    print("I have found this tags in the source file:\n")
    print("TAGS: ", end = "")
    print(tag_array)
    print("\n\n\n")
    answer = input("Insert tag to remove or !end! to quit: ")
    
    if answer == "!end!":
      print("\n\n\nend")
      break
    else:
      tag_array = LearnTags(answer, tag_array, database_dir)
  
def Train(database_dir):
  text = ReadAndNormalize(database_dir)
  data_array = FindTitleAndData(text)
  data_array[0] = RemoveLineFeed(data_array[0]) # TITLE
  data_array[1] = RemoveLineFeed(data_array[1]) # DATA BODY
  tags = BuildTags(DetectTags(RemovePunctuation(data_array[1]),database_dir))
  
  newData = tags + "_" + data_array[0] + "_" + data_array[1] + "_"
  WriteAtTheEnd(newData, database_dir)
  print("Data saved on database!")
  input()

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

def SearchForTag(tag, database_dir):
  lineIndexArray = []
  lineIndex = 0
  
  f = open(database_dir + "sophiaDatabase.txt", "r",  encoding = "utf-8")
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
  
def FindBestResult(tag_lines, results_array):
  i = 0
  while i < len(tag_lines):
    results_array[tag_lines[i]] += 1
    i += 1
  
  i = 0
  best_index = 0
  while i < len(results_array):
    if results_array[i] > results_array[best_index]:
      best_index = i
    i += 1
  
  return best_index

def PrintResult(data):
  i = 0
  cont = 0
  get_title = False
  get_data = False
  title = ""
  result = ""
  
  while i < len(data):
    if get_title:
      title += data[i:i+1]
    if get_data:
      result += data[i:i+1]
    
    if data[i:i+1] == "_" and cont == 0:
      cont = 1
      get_title = True
      get_data = False
    elif data[i:i+1] == "_" and cont == 1:
      cont = 2
      get_title = False
      get_data = True
    elif data[i:i+1] == "_" and cont == 2:
      cont = 0
      get_title = False
      get_data = False
    i += 1
  
  print(title[:len(title)-1] + "\n")
  print(result[:len(result)-1])

def Answer(question, results_array, database_dir):
  question = RemovePunctuation(question)
  question_tags = question.split()
  tag_lines_temp = []
  tag_lines = []
  
  i = 0
  while i < len(question_tags):
    search_result = SearchForTag(question_tags[i].lower(), database_dir)
    tag_lines_temp.append(search_result)
    if len(search_result) != 0:
      tag_lines.extend(search_result)
    i += 1 
  
  best_result = FindBestResult(tag_lines, results_array)
  
  f = open(database_dir + "sophiaDatabase.txt", "r", encoding = "utf-8")
  f.seek(0)
  line = f.readline()
  
  i = 0
  while i < len(results_array):
    line = line.strip()
    if i == best_result:
      PrintResult(line)
      break
    else:
      i += 1
      line = f.readline()
  
  print("\n\n\n\n")
  print("Your question produced this tags:")
  print(question_tags)
  print("\n")
  print("Database lines: ")
  print(tag_lines)
  print("\n")
  print("Database lines (more specified): ")
  print(tag_lines_temp)
  print("\n")
  print("Database best answer: " + str(best_result))

def ShowHelpCommands():
  print("This are the developer commands that allows you to fully interact with me!")
  print("For example you can access my whole database or you can allows me to learn new things\n")
  print("Remember to use this functions only when you know what are you doing!\n\n\n")
  print("help:       Show developer commands")
  print("learn:      Train Sophia's database'")
  print("learn tags: Train Sophia's tags identification")

def main():
  current_dir = os.getcwd()
  database_dir = current_dir + "/database/"
  
  results_array = []
  
  while True:
    results_array = InitializeSophiaSearchArray(database_dir)
    NewWindow()
    print("Ciao, sono Sophia!")
    print("In cosa posso aiutarti oggi?")
    print("\n\n")
    question = input()
    NewWindow()
    
    if question == "help":
      ShowHelpCommands()
    elif question == "learn":
      Train(database_dir)
    elif question == "learn tags":
      TrainTags(database_dir)
    elif question == "test":
      tags_array = input("> ")
      RemoveDuplicateTags(tags_array)
    else: # The user asked a question to Sophia...
      Answer(question, results_array, database_dir)
      input()

main()
