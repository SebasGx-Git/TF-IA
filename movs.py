# MOVS
# motionless: still | block -> sin combinación
# ataques: close | far
# direcciones H: right | left
# direcciones V: agacharse (bend) ? | jump (solo 1, si estoy en el aire ya no)
md = {
    'attacks': ('close' , 'far', 'block' ),
    'dispHor': ('right' , 'left' ),
    'dispVer': ('bend'  , 'jump' )
    # [000]NO? [001] [002] [010] [011] [012]...
}

movs = {}
for i, a in enumerate([None] + list(md['attacks'])):
  for j, h in enumerate([None] + list(md['dispHor'])):
    for k, v in enumerate([None] + list(md['dispVer'])):
      # print([i,j,k],' ',a,h,v)
      movs[(a,h,v)] = (i,j,k)
print(movs)

movs = {}
i = 0
for a in [None] + list(md['attacks']):
  for h in [None] + list(md['dispHor']):
    for v in [None] + list(md['dispVer']):
      movs[(a,h,v)] = (i)
      i += 1
print(movs)

movs_ord = {v: k for k, v in movs.items()}
movs_ord
print(movs_ord)