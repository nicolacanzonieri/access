# SOPHIA ~ Python database based chatbot

import console
import time
import os
import shutil

isDesktop = False
spaceWindowAmount = 20

def PrintWindowBorder(l):
  i = 0
  while i < l:
    print("=", end = "")
    i += 1
  print("")

def AddSpace(n):
  i = 0
  while i < n:
    print("")
    i = i+1

def NewWindow():
  if isDesktop == False:
    console.clear()
  else:
    os.system('cls' if os.name == 'nt' else 'clear')

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

def ShowHelpCommands():
  print("help:  Mostra tutti i comandi sviluppatore")
  print("learn: Effettua il training di Sophia")

def WriteOnDatabase():
  title = input("Titolo: ")
  print("Inserisci le informazioni riguardo l'argomento:")
  data = input()
  print("Inserisci i tags (separa un tag dall'altro con '/' es. cucina/pranzo/natale)")
  tags = input()

  # DATA STRUCTURE
  newData = tags + "_" + title + "_" + data + "_"
  WriteAtTheEnd(newData + "\n")

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
      WriteOnDatabase()

main()
