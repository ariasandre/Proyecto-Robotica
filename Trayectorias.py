import math
import Funciones


def TLibre(xi, yi, zi, xf, yf, zf, plano):
    time = 2.5
    n = 5
    deltat = time/n
    t = [0]
    for i in range(n):
        t.append(deltat*(i+1))
    # Matriz thetas finales montar cubicas
    ti = Funciones.CinInv(xi, yi, zi, plano)
    tf = Funciones.CinInv(xf, yf, zf, plano)
    # Calculo de trayectoria cubica para cada theta
    sect1 = Funciones.GTCubica(ti[0], tf[0], time, n)
    sect2 = Funciones.GTCubica(ti[1], tf[1], time, n)
    sect3 = Funciones.GTCubica(ti[2], tf[2], time, n)
    sect4 = Funciones.GTCubica(ti[3], tf[3], time, n)
    secuencia = [t, sect1, sect2, sect3, sect4]
    return secuencia


def TLineal(xi, yi, zi, xf, yf, zf, plano):
    # Tiempo total del recorrido
    tf = 5
    t = []
    # Cantidad de segmentos
    n = 10
    # Matriz thetas iniciales
    ti = Funciones.CinInv(xi, yi, zi, plano)
    # Matriz thetas finales
    tf = Funciones.CinInv(xf, yf, zf, plano)
    # Determina el paso para cada segmento
    deltat = tf/n
    deltat1 = (tf[0] - ti[0])/n
    deltat2 = (tf[1] - ti[1])/n
    deltat3 = (tf[2] - ti[2])/n
    deltat4 = (tf[3] - ti[3])/n
    # Secuencias de angulos independientes
    sect1 = [ti[0]]
    sect2 = [ti[1]]
    sect3 = [ti[2]]
    sect4 = [ti[3]]
    for i in range(n):
        t.append((i+1)*deltat)
        sect1.append(ti[0]+i*deltat1)
        sect2.append(ti[1]+i*deltat2)
        sect3.append(ti[2]+i*deltat3)
        sect4.append(ti[3]+i*deltat4)
    # Secuencia de angulos
    secuencia = [t, sect1, sect2, sect3, sect4]
    return secuencia


def TCirc(xi, yi, zi, xf, yf, zf, plano):
    # Tiempo total del recorrido
    tf = 5
    t = [0]
    # Cantidad de segmentos
    n = 10
    deltat = tf/n
    # Secuencias de angulos independientes
    ti = Funciones.CinInv(xi, yi, zi, plano)
    sect1 = [ti[0]]
    sect2 = [ti[1]]
    sect3 = [ti[2]]
    sect4 = [ti[3]]
    # Plano vertical (yz) x cte)
    # z**2+y**2=r
    y = []
    z = []
    if plano == "v":
        centroyz = [(yi+yf)/2, (zi+zf)/2]
        vi = [yi-centroyz[0], zi-centroyz[1]]
        vf = [yf-centroyz[0], zf-centroyz[1]]
        r = math.sqrt(vi[0]**2+vi[1]**2)
        anguloinicial = math.atan2(zi, yi)
        angulototal = math.acos((vi[0]*vf[0]+vi[1]*vf[1])/(r**2))
        deltaang = angulototal/n
        for i in range(n):
            t.append(deltat*(i+1))
            ytemp = centroyz[0] + r*math.cos(anguloinicial+i*deltaang)
            ztemp = centroyz[1] + r*math.sin(anguloinicial+i*deltaang)
            y.append(ytemp)
            z.append(ztemp)
            solucion = Funciones.CinInv(xi, ytemp, ztemp, plano)
            sect1.append(solucion[0])
            sect2.append(solucion[1])
            sect3.append(solucion[2])
            sect4.append(solucion[3])
        secuencia = [t, sect1, sect2, sect3, sect4]
        print(y)
        print(z)
        print(secuencia)
        return secuencia
    # Plano horizontal (xy) z cte
    # x**2+y**2=r
    else:
        centroxy = [(xi+xf)/2, (yi+yf)/2]
        vi = [xi-centroxy[0], yi-centroxy[1]]
        vf = [xf-centroxy[0], yf-centroxy[1]]
        r = math.sqrt(vi[0]**2+vi[1]**2)
        anguloinicial = math.atan2(yi, xi)
        angulototal = math.acos((vi[0]*vf[0]+vi[1]*vf[1])/(r**2))
        deltaang = angulototal/n
        for i in range(n):
            t.append(deltat*(i+1))
            xtemp = centroxy[0] + r*math.cos(anguloinicial+i*deltaang)
            ytemp = centroxy[1] + r*math.sin(anguloinicial+i*deltaang)
            solucion = Funciones.CinInv(xtemp, ytemp, zi, plano)
            sect1 = sect1.append(solucion[0])
            sect2 = sect2.append(solucion[1])
            sect3 = sect3.append(solucion[2])
            sect4 = sect4.append(solucion[3])
        secuencia = [t, sect1, sect2, sect3, sect4]
        return secuencia

# TCirc(10,4,-2,10,3,-1,"v")


Funciones.ArttoAct([28.6105, 28.9902, -25.9079, -73.0823])
