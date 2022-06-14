def alg_genetico(poblacion_inicial, alpha, max_iteraciones,
                 f_idonea, f_generarCandidatos,
                 f_seleccionarPares, f_cruce,
                 f_mutacion, mejor):
  # iniciar la poblacion
  poblacion = poblacion_inicial
  iteracion = 0
  mejor_idonea = -1000

  while iteracion < max_iteraciones:
    #calcular las funciones idoneas
    idoneos = [f_idonea(x) for x in poblacion]
    print('mejor:',mejor_idonea)
    # verificar si hay una buena mejora de la funcion idonea
    if(abs(max(idoneos) - mejor_idonea)<= alpha):
      return mejor(poblacion,f_idonea)
    else:
      mejor_idonea = max(idoneos)
    #generar candidatos y emparejar para cruce
    candidatos = f_generarCandidatos(poblacion,idoneos)
    par_padres = f_seleccionarPares(candidatos)
    #inicializar nueva genracion
    nva_generacion = []
    for par in par_padres:
      #generar los hijos y mutarlos
      hijos = f_cruce(iteracion,par)
      hijos = [f_mutacion(hijos[0]),f_mutacion(hijos[1])]
      # agregar a la nueva generacion
      nva_generacion.extend(hijos)
    # avanzar la iteracion
    iteracion = iteracion + 1
    poblacion = nva_generacion
    # print('poblacion:',poblacion)
  return mejor(poblacion,f_idonea)
