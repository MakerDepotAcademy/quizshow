import json

def load():
  with open('boardconfig.json', 'r') as fp:
    return json.load(fp)

def check():
  D = load()
  c = []
  for k in D:
    for b in D[k]['buttons']:
      c += [D[k]['buttons'][b]['in']]
      c += [D[k]['buttons'][b]['out']]
  
  if len(c) != len(set(c)):
    raise Exception('Duplicate pins found')

  return True

if __name__ == '__main__':
  if check():
    print("It's all good m8")