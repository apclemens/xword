
template = ['***** **** ****',
            '***** **** ****',
            '***** **** ****',
            '******** ******',
            '   **** *******',
            '****** *****   ',
            '*** ***** *****',
            '**** ***** ****',
            '***** ***** ***',
            '   ***** ******',
            '******* ****   ',
            '****** ********',
            '**** **** *****',
            '**** **** *****',
            '**** **** *****']

def getAcrossStart(template, cell):
  i = (cell[0], cell[1])
  while i[1] != -1 and template[i[0]][i[1]] != ' ':
    i = (i[0], i[1]-1)
  i = (i[0], i[1]+1)
  return i

def getDownStart(template, cell):
  i = (cell[0], cell[1])
  while i[0] != -1 and template[i[0]][i[1]] != ' ':
    i = (i[0]-1, i[1])
  i = (i[0]+1, i[1])
  return i

def getAcrossCells(template, acrossStart, asStr=False):
  cells = []
  i = (acrossStart[0], acrossStart[1])
  while i[1] != len(template[0]) and template[i[0]][i[1]] != ' ':
    if asStr:
      cells.append([str(j) for j in i])
    else:
      cells.append(i)
    i = (i[0], i[1]+1)
  return cells

def getDownCells(template, downStart, asStr=False):
  cells = []
  i = (downStart[0], downStart[1])
  while i[0] != len(template) and template[i[0]][i[1]] != ' ':
    if asStr:
      cells.append([str(j) for j in i])
    else:
      cells.append(i)
    i = (i[0]+1, i[1])
  return cells

def getAcrossCellsFromMid(template, acrossMid):
  return getAcrossCells(template, getAcrossStart(template, acrossMid))

def getDownCellsFromMid(template, downMid):
  return getDownCells(template, getDownStart(template, downMid))

def numCells(template):
  return ''.join(template).count('*')

def getStartLocations(template):
  startCells = []
  startCellsNotation = []
  cell = 1
  c = False
  for i in range(len(template)):
    for j in range(len(template[0])):
      if template[i][j] == ' ': continue
      if c:
        cell += 1
      c = False
      if i == 0 or j == 0:
        startCells.append((i,j))
        if i == 0:
          startCellsNotation.append(str(cell)+'D')
          c = True
        if j == 0:
          startCellsNotation.append(str(cell)+'A')
          c = True
        continue
      if template[i-1][j] == ' ' or template[i][j-1] == ' ':
        startCells.append((i,j))
        if template[i-1][j] == ' ':
          startCellsNotation.append(str(cell)+'D')
          c = True
        if template[i][j-1] == ' ':
          startCellsNotation.append(str(cell)+'A')
          c = True
  return startCellsNotation

if __name__ == '__main__':
  print getStartLocations(template)







































