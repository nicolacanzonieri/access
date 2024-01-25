import os
import re

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

def SearchForSuperTag(question_tags, database_dir, database_len):
  super_tag_found = False
  
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

'''New Answer Engine powered by SuperTags'''
def AnswerEngine(question, results_array, database_dir):
  question = RemovePunctuation(question)
  question_tags = question.split()

  try:
    super_tag_index = SearchForSuperTag(question_tags, database_dir, len(results_array))
  except:
    super_tag_index = -1

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

    print(str(super_tag_index) + ": ", end = "")
    print(super_tag_array)

    '''
    Search if there are other relevants tags in the question
    '''
    other_tags_found = False
    
    i = 0
    while i < len(question_tags):
      if len(SearchForTag(question_tags[i].lower(), database_dir)) > 0:
        j = 0
        while j < len(super_tag_array):
          if question_tags[i].lower() == super_tag_array[j]:
            other_tags_found = True
            break
          j += 1
      i += 1

    if other_tags_found:
      Answer(question, results_array, database_dir)
    else:
      print("Super tag found at line: " + str(super_tag_index) + "\n\n\n")
      f = open(database_dir + "sophiaDatabase.txt", "r", encoding = "utf-8")
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
    
  else:
    Answer(question, results_array, database_dir)

def main(results_array, database_dir):
  results_array = InitializeSophiaSearchArray(database_dir)
  question = input("> ")
  Answer(question, results_array, database_dir)
  input()

def main_test(results_array, database_dir):
  results_array = InitializeSophiaSearchArray(database_dir)
  question = input("Insert question: ")
  AnswerEngine(question, results_array, database_dir)

current_dir = os.getcwd()
database_dir = current_dir + "/database/"
results_array = []
main_test(results_array, database_dir)
