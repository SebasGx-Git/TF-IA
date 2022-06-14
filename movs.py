import random as rd
import numpy as np

# MOVS
# motionless: still | block -> sin combinación
# ataques: close | far
# direcciones H: right | left
# direcciones V: agacharse (bend) ? | jump (solo 1, si estoy en el aire ya no)
md = ['still', 'a_close' , 'a_far', 'block', 'w_right', 'w_left', 'jump']
movs = { x:i for i, x in enumerate(md) }
movs_ord = { i:x for i, x in enumerate(md) }
print(movs,movs_ord,sep='\n')


# NEMESIS
class Nemesis:

  def __init__(self, colors:tuple=None, reactions:list = None):
    self.duration = 0
    self.colors = colors if colors != None else tuple([rd.randint(0,255) for i in range(3)])
    if reactions == None:
      self.reactions = list(movs_ord)[:]
      rd.shuffle(self.reactions)
    else:
      self.reactions = reactions

  def __str__(self):
    return str(self.colors) + ' ' + str(self.reactions)
  def __repr__(self):
    return str(self)
  
  def mutateColor(self):
    def ccolor(b) :
      c = rd.randint(0,31)
      o = rd.randrange(0,3)
      c = b if o == 0 else b + c if o == 1 else b - c
      return 255 if c > 255 else 0 if c < 0 else c
    self.colors = tuple(map(lambda x : ccolor(x), self.colors))

  def mutateReact(self):
    n_mutar = rd.randint(0,len(self.reactions)-1)
    r = list(movs_ord.keys())
    r.pop(n_mutar)
    self.reactions[n_mutar] = rd.choice(r)
    # print('Se mutó', self.reactions, end = ' ')
    # print('en la posición',n_mutar,':',self.reactions)
    # return self.reactions
    # print(mutacion('01111'))
  
  def mutate(self):
    self.mutateColor()
    self.mutateReact()

  def f_ideal(self):
    return self.duration
  

# CROSSOVER
class Crossover:

  def __init__(self, parent1:Nemesis, parent2:Nemesis):
    self.p1 = parent1
    self.p2 = parent2

  def cross_color(self):
    w = rd.random()
    # print(w, colors)
    return tuple(np.average([self.p1.colors] + [self.p1.colors],
                      axis=0, weights=[w, 1-w]).astype(int))

  def cross_reactions(self):
    #iteracion 1 == 0 , i2 = 1
    corte = rd.randint(1,6)
    h1 = self.p1.reactions[:corte] + self.p2.reactions[corte:]
    h2 = self.p2.reactions[:corte] + self.p1.reactions[corte:]
    return [h1, h2]

  def cross(self,iteracion=None):
    color = self.cross_color()
    children = self.cross_reactions()
    #TO DO usar iteración
    return Nemesis(color,children[0]), Nemesis(color,children[1])


class Population():

  def __init__(self, n:int):
    self.pob = [Nemesis() for _ in range(n)]
    # pob_ini = [ "{0:05b}".format(p) for p in [0,1,3,15] ]
  
  def best(self):
    # def mejor(poblacion,f_idonea):
    return max(self.pob, key = lambda x : x.f_ideal())

  def generateCandidates(self,ideals:list): #list f_ideal
    #lista aleatoria de las parejas para el torneo
    list_pares = list(range(len(self.pob)))
    rd.shuffle(list_pares)
    #inicializando el arreglo de ganadores
    ganadores = []
    for i in range(len(self.pob)//2):
      par = list_pares[i*2]
      impar = list_pares[i*2+1]
      # pelea entre la iesima pareja
      if(ideals[par]>ideals[impar]):
        ganadores.append(self.pob[par])
        ganadores.append(self.pob[par])
      else:
        ganadores.append(self.pob[impar])
        ganadores.append(self.pob[impar])
    return ganadores

  def selectPairs(candidatos):
    #lista aleatoria de las parejas para el cruce
    list_pares = list(range(len(candidatos)))
    rd.shuffle(list_pares)
    pares = []
    for i in range(len(candidatos)//2):
      par = list_pares[i*2]
      impar = list_pares[i*2+1]
      pares.append([candidatos[par],candidatos[impar]])
    return pares

# EXAMPLE
n1 = Nemesis()
n2 = Nemesis()
print(n1, n2, sep="\n")
mut = Crossover(n1,n2)
print(mut.muteColor())
n3,n4 = mut.cross()
print(n3,n4)
n3.mutate()
n4.mutate()
print(n3,n4)

# alg_genetico(pob_ini, -0.0001, 100,
#              f_idonea, generarCandidatos,
#              seleccionarPares, cruce,
#              mutacion, mejor)