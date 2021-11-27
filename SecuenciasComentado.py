###############################################################################################################################################
#Funciones
import math
pos_act = 0
pasos = 0

# Calcula la cinematica inversa
def CinInv(x, y, z, plano):
    # Se definen las constantes
    L01 = 5
    L = 10
    Lt = 18.5
    # Se determina la orientacion (phi)
    if plano == "v":
        phi = math.radians(-10)
    else:
        phi = math.radians(-60)
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

# Genera la tayectoria cubica entre dos puntos dividiendo la 
#trayectoria en n segmentos
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

# Pasa del dominio de las articulaciones al dominio de los actuadores
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
    return actuadores



###############################################################################################################################################
#Trayectorias
def TLibre(xi, yi, zi, xf, yf, zf, plano):
    time = 10000
    n = 30
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
    # Se elimina la posicion inicial puesto que esta incluida como posicion final
    #de la secuencia anterior
    sect1.pop(0)
    sect2.pop(0)
    sect3.pop(0)
    sect4.pop(0)
    # Secuencia de angulos
    secuencialineal = [sect1, sect2, sect3, sect4]
    return secuencialineal

# Trayectorias circulares, une los puntos inicial y finalmediante un
#semicirculo
def TCirc(xi, yi, zi, xf, yf, zf, plano):
    # Tiempo total del recorrido
    time = 10000
    # Cantidad de segmentos
    n = 10
    deltatime = time/n
    # Secuencias de angulos independientes
    ti = CinInv(xi, yi, zi, plano)
    sect1 = [ti[0]]
    sect2 = [ti[1]]
    sect3 = [ti[2]]
    sect4 = [ti[3]]
    # Se define la cantidad de segmentos para la GTCubica
    nGTCub = 3
    if plano == "v":
        # Plano vertical (yz) x cte)
        # y**2+z**2=r
        y = [yi]
        z = [zi]
        # Calcula el centro del arco de la trayectoria circular
        centroyz = [(yi+yf)/2, (zi+zf)/2]
        vi = [yi-centroyz[0], zi-centroyz[1]]
        vf = [yf-centroyz[0], zf-centroyz[1]]
        # Calcula la distancia de cada punto al centro del arco
        r = math.sqrt(vi[0]**2+vi[1]**2)
        # Calcula el angulo inicial del arco
        anguloinicial = math.atan2(vi[1], vi[0])
        # Calcula el recorrido total en grados del arco
        angulototal = math.acos((vi[0]*vf[0]+vi[1]*vf[1])/(r**2))
        # Calcula el avance en grados para cada segmento
        deltaang = angulototal/n
        for i in range(1,n+1):
            # Calcula el punto siguiente sobre la trayectoria
            ytemp = centroyz[0] + r*math.cos(anguloinicial+i*deltaang)
            ztemp = centroyz[1] + r*math.sin(anguloinicial+i*deltaang)
            y.append(ytemp)
            z.append(ztemp)
            # Calcula la cinematica inversa para los puntos inicial del
            #segmento actual
            puntoinicial = CinInv(xi, y[i-1], z[i-1], plano)
            puntofinal = CinInv(xi, y[i], z[i], plano)
            # Calcula la trayectoria cubica que une los puntos del segmento
            #actual
            t1i = GTCubica(puntoinicial[0],puntofinal[0],deltatime,nGTCub)
            t2i = GTCubica(puntoinicial[1],puntofinal[1],deltatime,nGTCub)
            t3i = GTCubica(puntoinicial[2],puntofinal[2],deltatime,nGTCub)
            t4i = GTCubica(puntoinicial[3],puntofinal[3],deltatime,nGTCub)
            # Añade uno por uno las posiciones generadas para la secuencia de
            # los subsegmentos de la trayectoria cubica
            for i in range (nGTCub):
                sect1.append(t1i[i])
                sect2.append(t2i[i])
                sect3.append(t3i[i])
                sect4.append(t4i[i])
        # Elimina los puntos iniciales de la secuencia de posiciones para cada
        #angulo
        sect1.pop(0)
        sect2.pop(0)
        sect3.pop(0)
        sect4.pop(0)
        secuenciacircular = [sect1, sect2, sect3, sect4]
        return secuenciacircular
    else:
        # Plano horizontal (xy) z cte)
        # x**2+y**2=r
        x = [xi]
        y = [yi]
        # Calcula el centro del arco de la trayectoria circular
        centroxy = [(xi+xf)/2, (yi+yf)/2]
        vi = [xi-centroxy[0], yi-centroxy[1]]
        vf = [xf-centroxy[0], yf-centroxy[1]]
        # Calcula la distancia de cada punto al centro del arco
        r = math.sqrt(vi[0]**2+vi[1]**2)
        # Calcula el angulo inicial del arco
        anguloinicial = math.atan2(vi[1], vi[0])
        # Calcula el recorrido total en grados del arco
        angulototal = math.acos((vi[0]*vf[0]+vi[1]*vf[1])/(r**2))
        # Calcula el avance en grados para cada segmento
        deltaang = angulototal/n
        for i in range(1,n+1):
            # Calcula el punto siguiente sobre la trayectoria
            xtemp = centroxy[0] + r*math.cos(anguloinicial+i*deltaang)
            ytemp = centroxy[1] + r*math.sin(anguloinicial+i*deltaang)
            x.append(xtemp)
            y.append(ytemp)
            # Calcula la cinematica inversa para los puntos inicial del
            #segmento actual
            puntoinicial = CinInv(x[i-1], y[i-1], zi, plano)
            puntofinal = CinInv(x[i], y[i], zi, plano)
            # Calcula la trayectoria cubica que une los puntos del segmento
            #actual
            t1i = GTCubica(puntoinicial[0],puntofinal[0],deltatime,nGTCub)
            t2i = GTCubica(puntoinicial[1],puntofinal[1],deltatime,nGTCub)
            t3i = GTCubica(puntoinicial[2],puntofinal[2],deltatime,nGTCub)
            t4i = GTCubica(puntoinicial[3],puntofinal[3],deltatime,nGTCub)
            # Añade uno por uno las posiciones generadas para la secuencia de
            # los subsegmentos de la trayectoria cubica
            for i in range (nGTCub):
                sect1.append(t1i[i])
                sect2.append(t2i[i])
                sect3.append(t3i[i])
                sect4.append(t4i[i])
        # Elimina los puntos iniciales de la secuencia de posiciones para cada
        #angulo
        sect1.pop(0)
        sect2.pop(0)
        sect3.pop(0)
        sect4.pop(0)
        secuenciacircular = [sect1, sect2, sect3, sect4]
        return secuenciacircular



###############################################################################################################################################
#Secuencias
# Inicializa la secuencia de tiempos
t = []
# Se define el punto inicial
xi = 25
yi = 8
zi = -4
plano = "h"
# Inicializa la secuencia de posiciones de los actuadores
sect1 = []
sect2 = []
sect3 = []
sect4 = []
secuenciafinal = []
# Define el tiempo entre segmentos
deltatime = 10000/30
# Contador de trazos
trazos = 0

# Añade a las secuencias finales de posiciones de cada actuador
#una por una de las posiciones generadas en las secuencias de posiciones
#generadas por cada funcion de trayectorias, se ejecuta al final de la generacion
#de trayectorias de cada trazo y aumenta el contador de trazos en uno
def Actualizarlistas(secuencia): #secuencia = [t1,t2,t3,t4]
    global sect1
    global sect2
    global sect3
    global sect4
    global trazos
    for i in range(len(secuencia[0])):
        sect1.append(secuencia[0][i])
    for i in range(len(secuencia[1])):
        sect2.append(secuencia[1][i])
    for i in range(len(secuencia[2])):
        sect3.append(secuencia[2][i])
    for i in range(len(secuencia[3])):
        sect4.append(secuencia[3][i])
    trazos = trazos + 1

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
            sect1temp.append(0)
        else:
            temp = sect1[i]-sect1[i-1]
            sect1temp.append(temp)
    sect1 = sect1temp
    return None


def Secuencia():
    global xi
    global yi
    global zi
    global secuenciafinal

    ######################### Primera A ###############################
    # Bajar marcador
    Actualizarlistas(TLineal(xi,yi,zi, 25, 8, -5.7,"h")) #libre

    # Primer trazo
    Actualizarlistas(TLineal(25, 8, -5.7, 22, 10, -5.4, "h")) #lineal

    # Levanta marcador
    Actualizarlistas(TLineal(22, 10, -5.4, 22, 10, -4, "h")) #libre

    # Mueve al inicio
    Actualizarlistas(TLineal(22, 10, -4, 25.5, 6.5, -4, "h")) #libre

    # Baja marcador
    Actualizarlistas(TLineal(25.5, 6.5, -4, 25.5, 6.5, -5.8, "h")) #libre

    # Segundo trazo
    Actualizarlistas(TLineal(25.5, 6.5, -5.8, 22, 4.6, -5.8, "h")) #lineal

    # Levanta marcador
    Actualizarlistas(TLineal(22, 4.6, -5.8, 22, 4.6, -4, "h"))#libre

    # Movimiento al siguiente punto
    Actualizarlistas(TLineal(22, 4.6, -4, 24, 7.6, -4, "h"))  # libre

    # Bajar marcador
    Actualizarlistas(TLineal(24, 7.6, -4, 24, 7.6, -5.5, "h"))  # libre

    # Tercer trazo
    Actualizarlistas(TLineal(24, 7.6, -5.5, 24, 4, -5.1, "h"))  # libre

    # Levantar marcador
    Actualizarlistas(TLineal(24, 4, -5.1, 24, 4, -4, "h"))  # libre

    ######################### Segunda A ###############################
    # Mover a siguiente punto inicial
    Actualizarlistas(TLineal(24, 4, -4, 25, 0, -4.5, "h"))  # libre

    # Bajar marcador
    Actualizarlistas(TLineal(25, 0, -4.5, 25, 0, -6, "h"))  # libre

    # Primer trazo
    Actualizarlistas(TLineal(25, 0, -6, 22, 3, -6, "h"))  # lineal

    # Levanta marcador
    Actualizarlistas(TLineal(22, 3, -6, 22, 3, -4.5, "h"))  # libre

    # Mueve al inicio
    Actualizarlistas(TLineal(22, 3, -4.5, 25.5, 0, -4.5, "h"))  # libre

    # Baja marcador
    Actualizarlistas(TLineal(25.5, 0, -4.5, 25.5, 0, -6, "h"))  # libre

    # Segundo trazo
    Actualizarlistas(TLineal(25.5, 0, -6, 22, -2, -6, "h"))  # lineal

    # Levanta marcador
    Actualizarlistas(TLineal(22, -2, -6, 22, -2, -4.5, "h"))  # libre

    # Movimiento al siguiente punto
    Actualizarlistas(TLineal(22, -2, -4.5, 23, 2, -4.5, "h"))  # libre

    # Bajar marcador
    Actualizarlistas(TLineal(23, 2, -4.5, 23, 2, -6, "h"))  # libre

    # Tercer trazo
    Actualizarlistas(TLineal(23, 2, -6, 23, -1, -6, "h"))  # libre

    # Levantar marcador
    Actualizarlistas(TLineal(23, -1, -6, 23, -1, -4.5, "h"))  # libre

    ######################### Letra O ###############################
    # Mover a siguiente punto inicial
    Actualizarlistas(TLineal(23, -1, -4.5, 25, -4.5, -4.5, "h"))  # libre

    # Bajar marcador
    Actualizarlistas(TLineal(25, -4.5, -4, 25, -4.5, -6, "h"))  # libre

    # Primer trazo
    Actualizarlistas(TCirc(25, -4.5, -6, 23, -2.5, -6, "h"))  # lineal

    # Segundo trazo
    Actualizarlistas(TLineal(23, -2.5, -6, 21, -4.5, -6, "h"))  # lineal

    # Levantar marcador
    Actualizarlistas(TLineal(21, -4.5, -6, 21, -4.5, -4, "h"))  # lineal

    # Mover punto inicio
    Actualizarlistas(TLineal(21, -4.5, -4, 25, -4.5, -4, "h"))  # libre

    # Bajar marcador
    Actualizarlistas(TLineal(25, -4.5, -4, 25, -4.5, -6, "h"))  # libre

    # Tercer punto*
    Actualizarlistas(TLineal(25, -4.5, -6, 23, -6.5, -6, "h"))  # lineal

    # Cuarto punto*
    Actualizarlistas(TLineal(23, -6.5, -6, 21, -4.5, -6, "h"))  # lineal


    # Levanta marcador
    #Actualizarlistas(TLineal(21, -4.5, -6, 21, -4.5, -4.5, "h"))  # lineal

    # Mueve al inicio
    #Actualizarlistas(TLineal(21, -4.5, -4.5, 26, -5.5, -4.5, "h"))  # libre

    # Baja marcador
    #Actualizarlistas(TLineal(26, -5.5, -4.5, 26, -5.5, -6, "h"))  # libre

    # Tercer trazo
    #Actualizarlistas(TLineal(26, -5.5, -6, 24, -7.5, -6, "h"))  # lineal

    # Cuarto trazo
    #Actualizarlistas(TLineal(24, -7.5, -6, 22, -5.5, -6, "h"))  # lineal

    # Levanta marcador
    #Actualizarlistas(TLineal(19.5, 2, -6, 19.5, 22, -4.5, "h"))  # libre

    Actualizarsect1()
    secuenciafinal = [sect1,sect2,sect3,sect4]



###############################################################################################################################################
#Comunicacion
from sys import getsizeof
import serial
import time

def Comunicacion():
    global secuenciafinal
    global trazos
    loop = True
    COM = 'COM8'
    # Define el puerto serial para la comunicacion
    port = serial.Serial(COM, 9600)
    time.sleep(2)

    while loop:
        # Si el puerto esta abierto inicia la comunicacion
        if port.isOpen():
            # Recorre la secuencia de posiciones de trazo en trazo
            for k in range(1, trazos+1):
                envio = True
                # Recorre la secuencia de posiciones del trazo actual de secuencia de angulos
                #en secuencia de angulos empezando en t1 hasta t4
                for j in range(4):
                    # Recorre la secuencia de posiciones para la secuencia del angulo actual
                    #posicion por posicion
                    for i in range(30*(k-1), 30*k):
                        port.write(str(int(secuenciafinal[j][i]*100)).encode('ascii'))
                        print(str(int(secuenciafinal[j][i]*100)))
                        time.sleep(0.02)
                # Espera mientras se realiza el envio de datos
                while envio:
                    print("Esperando dato...")
                    value = str(port.readline().decode('ascii'))
                    # Si llega la confirmacion de que los datos se transmitieron exitosamente
                    if value != "":
                        print("Dato recibido!")
                        # Detiene el envio de datos
                        envio = False
                        # Reinicial a señal de transmision exitosa
                        value = ''
                    # Si no se confirma la transmision exitosa
                    else:
                        print("No se ha recibio el dato correcto")
            loop = False
        else:
            print("Error envio datos")

Secuencia()
Comunicacion()

#print(CinInv(25, 8, -4,"h"))