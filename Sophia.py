# SOPHIA ~ Python database based chatbot

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

def WriteOnDatabase():
  title = input("Titolo: ")
  print("Inserisci le informazioni riguardo l'argomento:")
  data = input()
  print("Inserisci i tags (separa un tag dall'altro con '/' es. cucina/pranzo/natale)")
  tags = input()

  # DATA STRUCTURE
  newData = tags + "_" + title + "_" + data + "/"
  WriteAtTheEnd(newData + "\n")

def SearchForTag():
  f = open("sophiaDatabase.txt", "r")
  f.seek(0)
  line = f.readline()

  while line:
    line = line.strip()

    if not line:
      break

    i = 0
    while i < len(line):



    line = f.readline()

  f.close()

SearchForTag()
