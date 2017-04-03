import os

def ensure_dir(d):
  if not os.path.exists(d):
    os.makedirs(d)

def getNextID(folder):
  i = 0
  while os.path.isfile(os.path.join(folder,str(i))):
    i += 1
  return i

def addTemplateFromInput():
  lines = ''
  size = input('Size: ')
  for i in range(size):
    lines += raw_input()
  addTempate(size, lines)

def addTemplate(size, lines):
  filename = str(size)+'x'+str(size)
  try:
    f = open(filename, 'r')
    l = f.read().split('\n')
    f.close()
    l.append(lines)
  except:
    l = [lines]
  f = open(filename, 'w')
  f.write('\n'.join(list(set(l))))
  f.close()

if __name__ == '__main__':
  addTemplateFromInput()
