def getWordLengths(template):
  
  wordLengths = []
  
  # across
  for i in range(len(template)):
    line = template[i]
    words = line.split(' ')
    for w in words:
      if len(w) != 0:
        wordLengths.append(len(w))
  
  # down
  for j in range(len(template[0])):
    line = ''.join([template[i][j] for i in range(len(template))])
    words = line.split(' ')
    for w in words:
      if len(w) != 0:
        wordLengths.append(len(w))
  
  return wordLengths

f = open('21x21/0', 'r')
template = f.read().split('\n')
while '' in template:
  template.remove('')
f.close()

lengths = getWordLengths(template)

import matplotlib.pyplot as plt
plt.hist(lengths)
plt.show()
