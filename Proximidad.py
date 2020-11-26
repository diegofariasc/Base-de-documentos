# Medidas de proximidad
# Proyecto final
# Recuperacion de la informacion y busqueda en web

from math import sqrt

"""
La funcion permite calcular la suma de los cuadrados de un vector
Input:  vector (di)
Output: escalar con la suma de los cuadrados de cada elemento en di
"""
def sumSquares(di):
    return sum ( [ dik ** 2 for dik in di ] )

# Medidas de similitud 
"""
La funcion permite calcular el producto interno dados dos vectores
Input:  vectores di y dj
Output: escalar con el producto interno entre di y dj
"""
def innerprod( di, dj ):
    return sum([ dik * djk for dik, djk in zip( di, dj) ])

"""
La funcion permite calcular el producto interno normalizado
Input:  vectores di y dj
Output: escalar con el producto interno normalizado entre di y dj
"""
def cos(di, dj):
    r1 = sqrt ( sumSquares(di) ) 
    r2 = sqrt ( sumSquares(dj) ) 
    return innerprod(di, dj) / ( r1 * r2 )

"""
La funcion permite calcular el coeficiente de dice
Input:  vectores di y dj
Output: escalar con el coeficiente de dice entre di y dj
"""
def dice(di, dj):
    m1 = sumSquares(di)
    m2 = sumSquares(dj)
    return (2 * innerprod(di, dj)) / (m1 + m2)

"""
La funcion permite calcular el coeficiente de jaccard
Input:  vectores di y dj
Output: escalar con el coeficiente de jaccard entre di y dj
"""
def jacc(di, dj):
    m1 = sumSquares(di)
    m2 = sumSquares(dj)
    return innerprod(di, dj) / (m1 + m2 - innerprod(di,dj))


"""
La funcion permite calcular la distancia euclidiana
Input:  vectores di y dj
Output: escalar con la distancia euclidiana entre di y dj
"""
def euc(di, dj):
    return sqrt( sum( [ (dik - djk)**2 for dik, djk in zip(di,dj) ] ) )

"""
La funcion permite calcular la distancia manhattan
Input:  vectores di y dj
Output: escalar con la distancia manhattan entre di y dj
"""
def manh(di, dj):
    return sum( [ abs(dik-djk) for dik, djk in zip(di,dj) ] )

    