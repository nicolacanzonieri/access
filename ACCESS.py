'''
A.C.C.E.S.S.
Automated Cataloging and Classification Engine for Storage and Search
~
Created by Nicola Canzonieri ~ Halo
'''

import console
import time
import os
import shutil
import re

isDesktop = True
spaceWindowAmount = 20
stop_wordsFileName = "stop_words_en.txt"

# Clear the user terminal window
def NewWindow():
  if isDesktop == False:
    console.clear()
  else:
    os.system('cls' if os.name == 'nt' else 'clear')

# Search file in specified directory
def SearchElementInDir(database_dir, fileName):
  found = False
  elements = os.listdir()
  for element in elements:
    if element == fileName:
      found = True
      return found

# Create ACCESS files
def InitializeDirectory(database_dir) -> bool:
  if not os.path.exists(os.getcwd() + "\source.txt"):
    print("Initializing source")
    f = open("source.txt","x")
    f.close();

  if not os.path.exists(os.getcwd() + "\database"):
    print("Initializing directory")
    os.mkdir("database")
    time.sleep(3)
    f = open("database\data.txt","x")
    f.close();
    f = open("database\\" + stop_wordsFileName,"x")
    f.close();
    f = open("database\supertags.txt","x")
    f.close();
    return True
  else :
    if not os.path.exists(os.getcwd() + "\database\data.txt"):
      print("Initializing database")
      f = open("database\data.txt","x")
      f.close();

    if not os.path.exists(os.getcwd() + "\database\supertags.txt"):
      print("Initializing supertags database")
      f = open("database\supertags.txt","x")
      f.close();
    
    if not os.path.exists(os.getcwd() + "\database\\" + stop_wordsFileName):
      while True:
        NewWindow()
        print("ERROR: stop_words database not found!\n\n\n")
        print("We recommend downloading the proper stop words database from ACCESS's GitHub page\n")
        print("Do you want to initialize a new empty stop words database? [1: Yes / 2: No]")
        user_input = str(input())

        if user_input == "1":
          print("Initializing stop words database")
          f = open("database\\" + stop_wordsFileName,"x")
          f.close();
          return True
        elif user_input == "2":
          return False
        else:
          NewWindow()
          print("Unknown code!")
          time.sleep(3)

    return True
          

# Create a new file in specified directory
def CreateFile(database_dir, fileName):
  f = open(database_dir + fileName, 'w')
  f.close()

# Initialize ACCESS results array
def InitializeAccessSearchArray(database_dir):
  results_array = []
  
  f = open(database_dir + "data.txt", "r", encoding = "utf-8")
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

# Read source file (found in specified directory) and substitute accented chars with the relative non-accented char with an apostrophe
def ReadAndNormalize(database_dir):
  accented_chars = {'è': 'e\'', 'é': 'e\'', 'ò': 'o\'', 'à': 'a\'', 'ù': 'u\'', 'ì': 'i\''}
  with open("source.txt", 'r', encoding='utf-8') as f:
    text = f.read()
    for char in accented_chars:
      text = text.replace(char, accented_chars[char])
  return text

# Find title and data about the argument discussed in the source file
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

# Remove line feed from a string
def RemoveLineFeed(data):
  i = 0
  while i < len(data):
    if data[i:i+1] == "\n":
      data = data.replace(data[i:i+1], '', 1)
      i = i - 1
    else:
      i = i + 1

  return data

# Remove punctuation from a string
def RemovePunctuation(str):
  i = 0
  
  while i < len(str):
    if ord(str[i:i+1]) >= 33 and ord(str[i:i+1]) <= 47:
      str = str.replace(str[i:i+1], ' ', 1)
      i -= 1
    elif ord(str[i:i+1]) >= 58 and ord(str[i:i+1]) <= 63:
      str = str.replace(str[i:i+1], ' ', 1)
      i -= 1
    elif ord(str[i:i+1]) >= 91 and ord(str[i:i+1]) <= 96:
      str = str.replace(str[i:i+1], ' ', 1)
      i -= 1
    elif ord(str[i:i+1]) >= 123 and ord(str[i:i+1]) <= 126:
      str = str.replace(str[i:i+1], ' ', 1)
      i -= 1
      
    i += 1
  
  return str

# Given an string array, delete the element of this array that are stop words
def OptimizeTags(str_array, database_dir):
  i = 0
  f = open(database_dir + stop_wordsFileName, "r+", encoding = "utf-8")
  
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

# Remove duplicate tags in tags_array
def RemoveDuplicateTags(tags_array):
  i = 0
  while i < (len(tags_array) - 2):
    j  = i + 1
    while j < len(tags_array):
      try:
        if tags_array[i] == tags_array[j]:
          tags_array.pop(j)
          j -= 1
        else:
          j += 1
      except:
        j += 1
    i += 1
  return tags_array

# First tag detector
def DetectTags(str, database_dir):
  words = str.split()
  regex = r"^[a-zA-Z0-9]+$"
  for word in words:
    if not re.match(regex, word):
      words.remove(word)
  
  words = RemoveDuplicateTags(words)
  return OptimizeTags(words, database_dir)

# Build tags string
def BuildTags(tag_array):
  tags = ""
  i = 0
  
  while i < len(tag_array):
    tags = tags + tag_array[i] + "/"
    i += 1
  
  tags = tags[:len(tags)-1]
  return tags

# Save new supertag in supertag database
def SaveSuperTag(s, database_dir):
  f = open(database_dir + "supertags.txt", "r+", encoding = "utf-8")
  f.seek(0)
  line = f.readline()
  while line:
    line = line.strip()
    if not line:
      break
    line = f.readline()
  f.write(s + "\n")
  f.close()

# Save new stop words in stop words database
def SaveStopWords(s, database_dir):
  f = open(database_dir + stop_wordsFileName, "r+", encoding = "utf-8")
  f.seek(0)
  line = f.readline()
  while line:
    line = line.strip()
    if not line:
      break
    line = f.readline()
  f.write(s + "\n")
  f.close()

# Save new data in ACCESS database
def SaveData(s, database_dir):
  f = open(database_dir + "data.txt", "r+", encoding = "utf-8")
  f.seek(0)
  line = f.readline()
  while line:
    line = line.strip()
    if not line:
      break
    line = f.readline()
  f.write(s + "\n")
  f.close()

# Given a tag, the tag array and the database directory, remove the tag from the tag array and save it in the stop words database
def LearnTags(tag, tag_array, database_dir):
  i = 0
  while i < len(tag_array):
    if CompareStrings(tag, tag_array[i]):
      SaveStopWords(tag, database_dir)
      tag_array.pop(i)
      i -= 1
      break
    
    i += 1
  
  return tag_array

# Train ACCESS tag finder by removing wrong tags
def TrainTags(database_dir):
  text = ReadAndNormalize(database_dir)
  data_array = FindTitleAndData(text)
  data_array[0] = RemoveLineFeed(data_array[0]) # TITLE
  data_array[1] = RemoveLineFeed(data_array[1]) # DATA BODY
  tag_array = RemoveDuplicateTags(DetectTags(RemovePunctuation(data_array[1]), database_dir))
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
 
# Add data to ACCESS database
def Train(database_dir):
  text = ReadAndNormalize(database_dir)
  data_array = FindTitleAndData(text)
  data_array[0] = RemoveLineFeed(data_array[0]) # TITLE
  data_array[1] = RemoveLineFeed(data_array[1]) # DATA BODY
  tags = BuildTags(RemoveDuplicateTags(DetectTags(RemovePunctuation(data_array[1]),database_dir)))
  
  newData = tags + chr(29) + data_array[0] + chr(29) + data_array[1] + chr(29)
  SaveData(newData, database_dir)
  SaveSuperTag(RemovePunctuation(data_array[0].lower()), database_dir)
  print("Data saved on database!")
  input()

# Given two strings, it returns true if the two strings are equal, otherwise it returns false
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

# 
def SearchForSuperTag(question_tags, database_dir, database_len):
  '''
  - question_tags = question tags
  - database_dir  = directory of the database
  - database_len  = length of the result array
  '''
  super_tag_found = False
  
  # Open supertags database and read the first line
  f = open(database_dir + "supertags.txt", "r", encoding = "utf-8")
  f.seek(0)
  line = f.readline()
  
  i = 0
  while i < database_len:
    line = line.strip()
    super_tag = line.split()
    
    j = 0
    while j < len(question_tags):
      if CompareStrings(question_tags[j].lower(), super_tag[0]):
        h = 1
        while h < len(super_tag):
          tag_found = False
          
          k = 0
          while k < len(question_tags):
            if CompareStrings(question_tags[k].lower(), super_tag[h]):
              tag_found = True
              break
            k += 1
          
          if not tag_found:
            break
          
          h += 1
        
        if h >= len(super_tag):
           super_tag_found = True
          
      if super_tag_found:
        break
      j += 1
    
    if super_tag_found:
      break
    
    line = f.readline()      
    i += 1
  
  f.close()
  
  if not super_tag_found:
    return -1
  else:
    return i

# 
def SearchForTag(tag, database_dir):
  lineIndexArray = []
  lineIndex = 0
  
  f = open(database_dir + "data.txt", "r",  encoding = "utf-8")
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

#
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

#
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
    
    if data[i:i+1] == chr(29) and cont == 0:
      cont = 1
      get_title = True
      get_data = False
    elif data[i:i+1] == chr(29) and cont == 1:
      cont = 2
      get_title = False
      get_data = True
    elif data[i:i+1] == chr(29) and cont == 2:
      cont = 0
      get_title = False
      get_data = False
    i += 1
  
  print(title[:len(title)-1] + "\n")
  print(result[:len(result)-1])

#
def NormalAnswer(question, results_array, database_dir):
  question = RemovePunctuation(question)
  question_tags = question.split()
    
  '''OG search algorithm'''
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
  
  f = open(database_dir + "data.txt", "r", encoding = "utf-8")
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

#
def SearchForSubject(question, results_array, database_dir):
  question = RemovePunctuation(question)
  question_tags = question.split()
  
  try:
    super_tag_index = SearchForSuperTag(question_tags, database_dir, len(results_array))
  except:
    super_tag_index = -1
  
  # if ACCESS found a supertag in the question...
  if super_tag_index != -1:
    f = open(database_dir + "supertags.txt", "r", encoding = "utf-8")
    f.seek(0)
    line = f.readline()
    
    i = 0
    while i <= super_tag_index:
      line = line.strip()
      if i == super_tag_index:
        break
      line = f.readline()
      i += 1
    f.close()

    super_tag_array = line.split()
    
    '''
    Search if there are other relevants tags in the question
    '''
    other_tags_found = False
    i = 0
    while i < len(question_tags):
      if len(SearchForTag(question_tags[i].lower(), database_dir)) > 0:
        other_tags_found = True
        j = 0
        while j < len(super_tag_array):
          if CompareStrings(question_tags[i].lower(), super_tag_array[j]):
            other_tags_found = False
          j += 1

        if other_tags_found:
          break
      i += 1
    
    if other_tags_found:
      NormalAnswer(question, results_array, database_dir)
    else:
      print("Super tag found at line: " + str(super_tag_index) + "\n\n\n")
      f = open(database_dir + "data.txt", "r", encoding = "utf-8")
      f.seek(0)
      line = f.readline()
      
      i = 0
      while i < len(results_array):
        line = line.strip()
        if i == super_tag_index:
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
      print(super_tag_array)
      print("\n")
      print("Database best answer: " + str(super_tag_index))
      
  else: # if ACCESS didn't found a supertag...
    NormalAnswer(question, results_array, database_dir)

  input()

# Show ACCESS commands
def ShowHelpCommands():
  print("This are the developer commands that allows you to fully interact with me!")
  print("Remember to use this functions only when you know what are you doing!\n\n\n")
  print("help:       Show developer commands")
  print("learn:      Add data to ACCESS database'")
  print("train tags: Train ACCESS tags identification")

  input()

def main():
  current_dir = os.getcwd()
  database_dir = current_dir + "\database\\"
  
  results_array = []
  initialization_result = InitializeDirectory(database_dir)
  
  while True:
    NewWindow()
    print("Hi, welcome in ACCESS!")
    print("How can I help you today?")
    print("\n\n")
    question = input()
    NewWindow()
    
    if question == "help":
      ShowHelpCommands()
    elif question == "learn":
      Train(database_dir)
    elif question == "train tags":
      TrainTags(database_dir)
    elif question == "debug":
      # Used only for debug purpose
      InitializeDirectory(database_dir)
      input()
    elif question == "!end!":
      break
    else: # The user asked a question to ACCESS...
      results_array = InitializeAccessSearchArray(database_dir)
      SearchForSubject(question, results_array, database_dir)

main()