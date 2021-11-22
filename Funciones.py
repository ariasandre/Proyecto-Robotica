import math

def CinInv(x,y,z,plano):
#Se definen las constantes
    L01 = 5;
    L = 10;
    #r = 2.1;
    Lt = 18.5;
#Se determina la orientacion (phi)
    if plano == "v":
        phi = math.radians(0);
    else:
        phi = math.radians(-90);
#Se calcula theta 1
    t1 = math.atan2(y,x);
#Se calcula theta 3
    A = x - Lt*math.cos(phi)*math.cos(t1);
    B = y - Lt*math.cos(phi)*math.sin(t1);
    C = z - L01 - Lt*math.sin(phi);
    t3 = -math.acos((A**2+B**2+C**2-2*L**2)/(2*L**2));
#Se calcula theta 2
    a = L*math.sin(-t3);
    b = L + L*math.cos(-t3);
    c= z - L01 - Lt*math.sin(phi);
    r1= math.sqrt(a**2+b**2);
    t2 = math.atan2(c , math.sqrt(r1**2-c**2)) + math.atan(a / b);
#Se calcula theta 4
    t4 = phi - t2 - t3;
#Solucion Cinematica Inversa
    solucion = [math.degrees(t1),math.degrees(t2),math.degrees(t3),math.degrees(t4)];
    return solucion;

def GTCubica(angi,angf,tf,n):
    deltat = tf/n;
    secuencia = [angi];
    a0 = angi;
    a2 = -3*(angi-angf)/(tf**2);
    a3 = 2*(angi-angf)/(tf**3);
    for i in range(n):
        ttemp = deltat*(i+1);
        pos = a0 + a2*(ttemp**2) + a3*(ttemp**3);
        secuencia.append(pos);
    print(secuencia)
    return secuencia;

def ArttoAct(solucion,pos):
    t1=solucion[0];
    t2=solucion[1];
    t3=solucion[2];
    t4=solucion[3];
    stp = t1/11.25 - pos;
    t2f = 90 + t2;
    t3f = 90 - t3;
    t4f = 90 + t4;
    actuadores = [stp,t2f,t3f,t4f];
    return (actuadores);

GTCubica(6,90,5,5)