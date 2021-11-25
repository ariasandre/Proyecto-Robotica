import math

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

def ArttoAct(solucion):
    global pasos
    global pos_act
    t1 = solucion[0]
    t2 = solucion[1]
    t3 = solucion[2]
    t4 = solucion[3]
    pasos = -(pos_act + t1)
    pos_act = -t1
    t1f = pasos
    t2f = 90 - t2
    t3f = -t3
    t4f = -t4
    actuadores = [t1f, t2f, t3f, t4f]
    print(pasos)
    return actuadores


#S = CinInv(22, 11, -7, "h")
#A = ArttoAct(S)
#print(A)
#S = CinInv(22,-11, -7, "h")
#A = ArttoAct(S)
#print(A)
#S = CinInv(22, 11, -7, "h")
#A = ArttoAct(S)
#print(A)
GTCubica(0,90,5,5)