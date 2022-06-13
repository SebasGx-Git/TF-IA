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