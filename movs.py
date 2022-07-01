import random as rd
import numpy as np
from alg_genetico import alg_genetico 

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

  def __init__(self, colors:tuple=None, reactions:list = None, stimated_heur = 0):
    self.duration = 0
    self.damage_done = 0
    self.stimated_heur = stimated_heur
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
  

# CROSSOVER
class Crossover:

  def __init__(self, parent1:Nemesis, parent2:Nemesis):
    self.p1 = parent1
    self.p2 = parent2

  def cross_color(self, corte):
    # w = rd.random()
    w = (corte * 100) / len(self.p1.reactions) #7 - 100 | c - x | c * 100 / 7
    # print(w, colors)
    return tuple(np.average([self.p1.colors] + [self.p1.colors],
                      axis=0, weights=[w, 1-w]).astype(int))

  def cross_reactions(self, corte):
    h1 = self.p1.reactions[:corte] + self.p2.reactions[corte:]
    h2 = self.p2.reactions[:corte] + self.p1.reactions[corte:]
    return [h1, h2]

  def cross(self,iteracion=None):
    #iteracion 1 == 0 , i2 = 1
    corte = rd.randint(1,6)
    color = self.cross_color(corte)
    children = self.cross_reactions(corte)
    if self.p1.stimated_heur == 0 : self.p1.stimated_heur = self.p1.duration #self.p1.damage_done 
    if self.p2.stimated_heur == 0 : self.p2.stimated_heur = self.p2.duration #self.p2.damage_done 
    stimated_heur = (self.p1.stimated_heur + self.p2.stimated_heur)//2
    #TO DO usar iteración
    return Nemesis(color,children[0],stimated_heur), Nemesis(color,children[1],stimated_heur)


n = 8
pob_ini = [Nemesis() for _ in range(n)]


def f_ideal(n:Nemesis):
  return n.duration if n.duration > 0 else n.stimated_heur
  #return n.damage_done if n.damage_done > 0 else n.stimated_heur

def generateCandidates(population:list,ideals:list): #list f_ideal
  #lista aleatoria de las parejas para el torneo
  list_pares = list(range(len(population)))
  rd.shuffle(list_pares)
  #inicializando el arreglo de ganadores
  ganadores = []
  for i in range(len(population)//2):
    par = list_pares[i*2]
    impar = list_pares[i*2+1]
    # pelea entre la iesima pareja
    if(ideals[par]>ideals[impar]):
      ganadores.append(population[par])
      ganadores.append(population[par])
    else:
      ganadores.append(population[impar])
      ganadores.append(population[impar])
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

def f_cross(a, b:tuple) : #iteracion, par
  return Crossover(b[0],b[1]).cross() 

def f_mutacion(n:Nemesis):
  n.mutate()
  return n

def best(population, _):
  return (max(population, key = lambda x : f_ideal(x)), population)

# EXAMPLE
n1 = Nemesis()
n2 = Nemesis()
print(n1, n2, sep="\n")
mut = Crossover(n1,n2)
#print(mut.muteColor())
n3,n4 = mut.cross()
print(n3,n4)
n3.mutate()
n4.mutate()
print(n3,n4)


def newGeneration(poblacion = None):
  if poblacion == None:
    global pob_ini
    print(pob_ini)
    poblacion = pob_ini
  return alg_genetico(poblacion, -0.0001, 100,
             f_ideal, generateCandidates,
             selectPairs, f_cross,
             f_mutacion, best)

