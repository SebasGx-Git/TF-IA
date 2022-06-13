import random as rd
import numpy as np

# MOVS
# motionless: still | block -> sin combinación
# ataques: close | far
# direcciones H: right | left
# direcciones V: agacharse (bend) ? | jump (solo 1, si estoy en el aire ya no)
md = {
    'movs': ( None, 'close' , 'far', 'block' ),
    'walkHor': ( None, 'right' , 'left' ),
    # 'dispVer': ( 'bend'  , 'jump' )
    'jump'   : ( False  , True )
    # [000]NO? [001] [002] [010] [011] [012]...
}

movs = {}
for i, a in enumerate(md['movs']):
  for j, h in enumerate(md['walkHor']):
    for k, v in enumerate(md['jump']):
      # print([i,j,k],' ',a,h,v)
      movs[(a,h,v)] = (i,j,k)
print(movs)

movs = {}
c = 0
for i, a in enumerate(md['movs']):
  for j, h in enumerate(md['walkHor']):
    for k, v in enumerate(md['jump']):
      movs[(a,h,v)] = (c)
      c += 1
print(movs)

movs_ord = {v: k for k, v in movs.items()}
print(movs_ord)

b8 = lambda : rd.randint(0,255)
class Nemesis: 
  def __init__(self, colors:tuple=None, reactions:list = None):
    self.colors = colors if colors != None else (b8(),b8(),b8())
    if reactions == None:
      self.reactions = list(movs_ord)[:]
      rd.shuffle(self.reactions)
    else:
      self.reactions = reactions
  def __str__(self):
    return str(self.colors) + ' ' + str(self.reactions)

n1 = Nemesis()
n2 = Nemesis()
print(n1, n2, sep="\n")

def ccolor(b) :
  c = rd.randint(0,31)
  o = rd.randrange(0,3)
  c = b if o == 0 else b + c if o == 1 else b - c
  return 255 if c > 255 else 0 if c < 0 else c

def muteColor(parent1:Nemesis, parent2:Nemesis):
  w = rd.random()
  colors = np.average([parent1.colors] + [parent2.colors],
                      axis=0, weights=[w, 1-w]).astype(int)
  colors = tuple(map(lambda x : ccolor(x), colors))
  # np.apply(colors, lambda x : ccolor(x))
  print(w, colors)

print(muteColor(n1,n2))