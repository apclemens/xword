f = open('/usr/share/dict/american-english', 'r')
words = f.read().split('\n')
f.close()

index = []
# build word index
for w in words:
  while len(index) <= len(w):
    index.append([])
  index[len(w)].append(w)

def isWordMatch(template, word):
  if len(template) != len(word):
    return False
  for chI in range(len(template)):
    if word[chI] not in 'abcdefghijklmnopqrstuvwxyz': return False
    if template[chI] == '*':
      continue
    if template[chI] != word[chI]:
      return False
  return True

def getMatchingWords(template, excludeWords):
  if '*' not in template: return [template.lower()]
  matches = []
  for word in index[len(template)]:
    if word.lower() not in excludeWords and isWordMatch(template.lower(), word.lower()):
      matches.append(word.lower())
  return matches
