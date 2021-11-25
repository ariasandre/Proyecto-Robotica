import math

###############################################################################################################################################
#Funciones
pos_act = 0
pasos = 0

def CinInv(x, y, z, plano):
    # Se definen las constantes
    L01 = 5
    L = 10
    # r = 2.1;
    Lt = 18.5
    # Se determina la orientacion (phi)
    if plano == "v":
        phi = math.radians(-10)
    else:
        phi = math.radians(-70)
    # Se calcula theta 1
    t1 = math.atan2(y, x)
    # Se calcula theta 3
    A = x - Lt * math.cos(phi) * math.cos(t1)
    B = y - Lt * math.cos(phi) * math.sin(t1)
    C = z - L01 - Lt * math.sin(phi)
    t3 = -math.acos((A ** 2 + B ** 2 + C ** 2 - 2 * L ** 2) / (2 * L ** 2))
    # Se calcula theta 2
    a = L * math.sin(-t3)
    b = L + L * math.cos(-t3)
    c = z - L01 - Lt * math.sin(phi)
    r1 = math.sqrt(a ** 2 + b ** 2)
    t2 = math.atan2(c, math.sqrt(r1 ** 2 - c ** 2)) + math.atan(a / b)
    # Se calcula theta 4
    t4 = phi - t2 - t3
    # Solucion Cinematica Inversa
    solucionart = [math.degrees(t1), math.degrees(t2), math.degrees(t3), math.degrees(t4)]
    solucionact = ArttoAct(solucionart)
    return solucionact

#Entrega el todos los puntos iniciando en t=deltatime
def GTCubica(angi, angf, tf, n):
    deltatime = tf / n
    secuencia = []
    a0 = angi
    a2 = -3 * (angi - angf) / (tf ** 2)
    a3 = 2 * (angi - angf) / (tf ** 3)
    for i in range(n):
        ttemp = deltatime * (i + 1)
        pos = a0 + a2 * (ttemp ** 2) + a3 * (ttemp ** 3)
        secuencia.append(pos)
    return secuencia

#Pasa del dominio de las articulaciones al dominio de los actuadores
def ArttoAct(solucion):
    t1 = solucion[0]
    t2 = solucion[1]
    t3 = solucion[2]
    t4 = solucion[3]
    t1f = -t1
    t2f = 90 - t2
    t3f = -t3
    t4f = -t4
    actuadores = [t1f, t2f, t3f, t4f]
    #print(pasos)
    return actuadores



###############################################################################################################################################
#Trayectorias
def TLibre(xi, yi, zi, xf, yf, zf, plano):
    time = 5000
    n = 30
    #deltatime = 5000/30
    # Matriz thetas finales montar cubicas
    ti = CinInv(xi, yi, zi, plano)
    tf = CinInv(xf, yf, zf, plano)
    # Calculo de trayectoria cubica para cada theta
    sect1 = GTCubica(ti[0], tf[0], time, n)
    sect2 = GTCubica(ti[1], tf[1], time, n)
    sect3 = GTCubica(ti[2], tf[2], time, n)
    sect4 = GTCubica(ti[3], tf[3], time, n)
    secuencialibre = [sect1, sect2, sect3, sect4]
    return secuencialibre

def TLineal(xi, yi, zi, xf, yf, zf, plano):
    # Tiempo total del recorrido
    time = 10000
    # Cantidad de segmentos
    n = 10
    # deltatime = 10000/(10*3)
    # Matriz thetas iniciales
    ti = CinInv(xi, yi, zi, plano)
    # Matriz thetas finales
    tf = CinInv(xf, yf, zf, plano)
    # Determina el paso para cada segmento
    deltatime = time/n
    deltat1 = (tf[0] - ti[0])/n
    deltat2 = (tf[1] - ti[1])/n
    deltat3 = (tf[2] - ti[2])/n
    deltat4 = (tf[3] - ti[3])/n
    # Secuencias de angulos independientes
    sect1 = [ti[0]]
    sect2 = [ti[1]]
    sect3 = [ti[2]]
    sect4 = [ti[3]]
    nGTCub = 3
    for i in range(0,n*nGTCub,nGTCub):
        # Calculo de la secuencia de posiciones hasta la posicion siguiente
        #usando GTCubicas
        t1i = GTCubica(sect1[i],sect1[i]+deltat1,deltatime,nGTCub)
        t2i = GTCubica(sect2[i],sect2[i]+deltat2,deltatime,nGTCub)
        t3i = GTCubica(sect3[i],sect3[i]+deltat3,deltatime,nGTCub)
        t4i = GTCubica(sect4[i],sect4[i]+deltat4,deltatime,nGTCub)
        for i in range (nGTCub):
            #Se añade el punto siguiente a la secuencia
            sect1.append(t1i[i])
            sect2.append(t2i[i])
            sect3.append(t3i[i])
            sect4.append(t4i[i])
    #Se elimina la posicion inicial puesto que esta incluida como posicion final
    #de la secuencia anterior
    sect1.pop(0)
    sect2.pop(0)
    sect3.pop(0)
    sect4.pop(0)
    # Secuencia de angulos
    secuencialineal = [sect1, sect2, sect3, sect4]
    return secuencialineal

#Trayectorias circulares, une los puntos inicial y finalmediante un
# semicirculo
def TCirc(xi, yi, zi, xf, yf, zf, plano):
    # Tiempo total del recorrido
    tf = 15000
    t = [0]
    # Cantidad de segmentos
    n = 10
    deltat = tf/n
    # Secuencias de angulos independientes
    ti = CinInv(xi, yi, zi, plano)
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
            solucion = CinInv(xi, ytemp, ztemp, plano)
            sect1.append(solucion[0])
            sect2.append(solucion[1])
            sect3.append(solucion[2])
            sect4.append(solucion[3])
        secuenciacircular = [t, sect1, sect2, sect3, sect4]
        print(y)
        print(z)
        print(secuenciacircular)
        return secuenciacircular
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
            solucion = CinInv(xtemp, ytemp, zi, plano)
            sect1 = sect1.append(solucion[0])
            sect2 = sect2.append(solucion[1])
            sect3 = sect3.append(solucion[2])
            sect4 = sect4.append(solucion[3])
        secuenciacircular = [t, sect1, sect2, sect3, sect4]
        return secuenciacircular



###############################################################################################################################################
#Secuencias
t = [0]
#Se define el punto inicial
xi = 20
yi = 8
zi = -6
plano = "h"
#Inicializa en posicion de reposo en el espacio
# de los actuadores
#
#sect1 = [puntoinicial[0]]
#sect2 = [puntoinicial[1]]
#sect3 = [puntoinicial[2]]
#sect4 = [puntoinicial[3]]
sect1 = []
sect2 = []
sect3 = []
sect4 = []
deltatime = 5000/30

def Actualizarlistas(secuencia): #secuencia = [t1,t2,t3,t4]
    global sect1
    global sect2
    global sect3
    global sect4
    for i in range(len(secuencia[0])):
        sect1.append(secuencia[0][i])
    for i in range(len(secuencia[1])):
        sect2.append(secuencia[1][i])
    for i in range(len(secuencia[2])):
        sect3.append(secuencia[2][i])
    for i in range(len(secuencia[3])):
        sect4.append(secuencia[3][i])

#Crea la matriz de tiempos
def TimeMatrix():
    global t
    global sect1
    global deltatime
    for i in range(len(sect1)-1):
        t.append(t[i]+deltatime)
    return None

#Cambia el valor de la secuencia de t1 de posiciones a avances
def Actualizarsect1():
    global sect1
    sect1temp = []
    for i in range(len(sect1)):
        if i == 0:
            sect1temp.append(sect1[i])
        else:
            temp = sect1[i]-sect1[i-1]
            sect1temp.append(temp)
    sect1 = sect1temp
    return None


def Pruebas():
    global xi
    global yi
    global zi
    print("Punto 1")
    print(CinInv(xi,yi,zi,"h"))
    print ("\n")
    print("Punto 2")
    print(CinInv(17,-10,-4,"h"))
    print ("\n")
    print("Punto 3")
    print(CinInv(20,-7,-4,"h"))
    print ("\n")
    Actualizarlistas(TLibre(xi,yi,zi,17,-10,-4,"h"))
    Actualizarlistas(TLineal(17,-10,-4,20,-7,-4,"h"))
    TimeMatrix()
    print (sect1)
    Actualizarsect1()
    secuenciafinal = [t,sect1,sect2,sect3,sect4]
    print ("\n")
    #print (secuenciafinal[0])
    #print ("\n")
    print (secuenciafinal[1])
    #print ("\n")
    #print (secuenciafinal[2]) 
    #print ("\n")
    #print (secuenciafinal[3])
    #print ("\n")
    #print (secuenciafinal[4])
    #print ("\n")
    #print(len(t))
    #print(len(sect2))

Pruebas()