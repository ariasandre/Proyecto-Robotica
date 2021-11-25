import math
import matplotlib.pyplot as plt 

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

def TCirc(xi, yi, zi, xf, yf, zf, plano):
    # Tiempo total del recorrido
    time = 15000
    t = [0]
    # Cantidad de segmentos
    n = 10
    deltatime = time/n
    # Secuencias de angulos independientes
    ti = CinInv(xi, yi, zi, plano)
    #tf = CinInv(xf, yf, zf, plano)
    #print("Angulos iniciales")
    #print(ti)
    #print("\n")
    #print("Angulos finales")
    #print(tf)
    #print("\n")
    sect1 = [ti[0]]
    sect2 = [ti[1]]
    sect3 = [ti[2]]
    sect4 = [ti[3]]
    #Se define la cantidad de segmentos para la GTCubica
    nGTCub = 3
    if plano == "v":
        # Plano vertical (yz) x cte)
        # y**2+z**2=r
        y = [yi]
        z = [zi]
        centroyz = [(yi+yf)/2, (zi+zf)/2]
        vi = [yi-centroyz[0], zi-centroyz[1]]
        vf = [yf-centroyz[0], zf-centroyz[1]]
        r = math.sqrt(vi[0]**2+vi[1]**2)
        anguloinicial = math.atan2(vi[1], vi[0])
        angulototal = math.acos((vi[0]*vf[0]+vi[1]*vf[1])/(r**2))
        deltaang = angulototal/n
        for i in range(1,n+1):
            t.append(deltatime*(i))
            ytemp = centroyz[0] + r*math.cos(anguloinicial+i*deltaang)
            ztemp = centroyz[1] + r*math.sin(anguloinicial+i*deltaang)
            y.append(ytemp)
            z.append(ztemp)
            #Hasta aqui funciona
            puntoinicial = CinInv(xi, y[i-1], z[i-1], plano)
            puntofinal = CinInv(xi, y[i], z[i], plano)
            t1i = GTCubica(puntoinicial[0],puntofinal[0],deltatime,nGTCub)
            t2i = GTCubica(puntoinicial[1],puntofinal[1],deltatime,nGTCub)
            t3i = GTCubica(puntoinicial[2],puntofinal[2],deltatime,nGTCub)
            t4i = GTCubica(puntoinicial[3],puntofinal[3],deltatime,nGTCub)
            for i in range (nGTCub):
                sect1.append(t1i[i])
                sect2.append(t2i[i])
                sect3.append(t3i[i])
                sect4.append(t4i[i])
        secuenciacircular = [sect1, sect2, sect3, sect4]
        return secuenciacircular
    else:
        # Plano horizontal (xy) z cte)
        # x**2+y**2=r
        x = [xi]
        y = [yi]
        centroxy = [(xi+xf)/2, (yi+yf)/2]
        vi = [xi-centroxy[0], yi-centroxy[1]]
        vf = [xf-centroxy[0], yf-centroxy[1]]
        r = math.sqrt(vi[0]**2+vi[1]**2)
        anguloinicial = math.atan2(vi[1], vi[0])
        angulototal = math.acos((vi[0]*vf[0]+vi[1]*vf[1])/(r**2))
        deltaang = angulototal/n
        for i in range(1,n+1):
            t.append(deltatime*(i))
            xtemp = centroxy[0] + r*math.cos(anguloinicial+i*deltaang)
            ytemp = centroxy[1] + r*math.sin(anguloinicial+i*deltaang)
            x.append(xtemp)
            y.append(ytemp)
            #Hasta aqui funciona
            puntoinicial = CinInv(x[i-1], y[i-1], zi, plano)
            puntofinal = CinInv(x[i], y[i], zi, plano)
            t1i = GTCubica(puntoinicial[0],puntofinal[0],deltatime,nGTCub)
            t2i = GTCubica(puntoinicial[1],puntofinal[1],deltatime,nGTCub)
            t3i = GTCubica(puntoinicial[2],puntofinal[2],deltatime,nGTCub)
            t4i = GTCubica(puntoinicial[3],puntofinal[3],deltatime,nGTCub)
            for i in range (nGTCub):
                sect1.append(t1i[i])
                sect2.append(t2i[i])
                sect3.append(t3i[i])
                sect4.append(t4i[i])
        secuenciacircular = [sect1, sect2, sect3, sect4]
        return secuenciacircular

TCirc(5,0,4,5,0,-4,"h")