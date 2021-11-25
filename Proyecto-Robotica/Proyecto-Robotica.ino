// Se agregan las librerias necesarias
#include <Stepper.h>
#include <Servo.h>

// Se definen las varibles y constantes del motor a pasos
const float pasos_por_rev = 32;
const float reduccion = 64;
float pasos = 0; 
float M1_angulo = -19.98; // Posición de reposo
Stepper motor_a_pasos(pasos_por_rev, 8,10,9,11);

// Se definen las variables para el servo 1
Servo servo1;
float M2_angulo = 45.26; // Posición de reposo
float M2_timing;

// Se definen las variables para el servo 2
Servo servo2;
float M3_angulo = 48.48; // Posición de reposo
float M3_timing;

// Se definen las variables para el servo 3
Servo servo3;
float M4_angulo = 66.25; // Posición de reposo
float M4_timing;

// Se definen otros pines de interes
int pin_inicio = 12; // Pin inicio de secuencia
bool pos1 = LOW;

// Se definen otras variables de interes
bool value;
bool inicial = false;

// Se definen variables para Serial
float elemento_serial = 0;
float t[30];
float M1[30];
float M2[30];
float M3[30];
float M4[30];
int i = 0;
int j = 0;
int k = 0;
bool listo_serial = false;
int LED1 = 2, LED2 = 4, LED3 = 7;

void setup() {
  // Configuración de pines
  pinMode(pin_inicio,INPUT);
  pinMode(LED1,OUTPUT);
  pinMode(LED2,OUTPUT);
  pinMode(LED3,OUTPUT);
  servo1.attach(3);
  servo2.attach(5);
  servo3.attach(6);

  Serial.begin(9600);
  Serial.setTimeout(10);
}

void loop() {
  //------------Definición posición de reposo------------//
  // Configuración del motor a pasos
  motor_a_pasos.setSpeed(300);
  pasos = 5.6888889*M1_angulo;

  // Configuración de los servos
  M2_timing = 11.555556*M2_angulo + 660; //0 - 90
  M3_timing = -11.111111*M3_angulo + 2300; // 0 - 90
  M4_timing = 11.888889*M4_angulo + 750; //750-1820
  servo1.writeMicroseconds(M2_timing);
  servo2.writeMicroseconds(M3_timing);
  servo3.writeMicroseconds(M4_timing);
  inicial = digitalRead(pin_inicio);
  if (inicial){
    motor_a_pasos.step(pasos);
  }

  // Lectura del inicio
  //value = digitalRead(pin_inicio);

  // Inicio de secuencia
  if(listo_serial){
    for (int i_for = 0; i_for < 30; i_for++){
      pasos = 5.6888889*M1[i_for];  
      M2_timing = 11.555556*M2[i_for] + 660; //0 - 90
      M3_timing = -11.111111*M3[i_for] + 2300; // 0 - 90
      M4_timing = 11.888889*M4[i_for] + 750; //750-1820

      servo3.writeMicroseconds(M4_timing);
      //Serial.println(M4[i_for]);
      //delay(800);
      servo2.writeMicroseconds(M3_timing);
      //Serial.println(M3[i_for]);
      //delay(800);
      servo1.writeMicroseconds(M2_timing);
      //Serial.println(M2[i_for]);
      //delay(800);
      motor_a_pasos.step(pasos);
      //Serial.println(M1[i_for]);
      delay(800);
    }
    listo_serial = false;
    M2_angulo = M2[29];
    M3_angulo = M3[29];
    M4_angulo = M4[29];
  }

  else{
    switch (j){
      case 0:
        digitalWrite(LED1, HIGH);
        digitalWrite(LED2, LOW);
        digitalWrite(LED3, LOW);
        break;

      case 1:
        digitalWrite(LED1, LOW);
        digitalWrite(LED2, HIGH);
        digitalWrite(LED3, LOW);
        break;
        
      case 2:
        digitalWrite(LED1, HIGH);
        digitalWrite(LED2, HIGH);
        digitalWrite(LED3, LOW);
        break;
        
      case 3:
        digitalWrite(LED1, LOW);
        digitalWrite(LED2, LOW);
        digitalWrite(LED3, HIGH);
        break;

     default:
        digitalWrite(LED1, HIGH);
        digitalWrite(LED2, HIGH);
        digitalWrite(LED3, HIGH);
        break;
    }
  }
  
  /*if(value == HIGH)
  {
    /*while(1){
      M2_timing = M2_timing+8;
      M3_timing = M3_timing-8;
      M4_timing = M4_timing+8;
      motor_a_pasos.step(pasos);
      delay(800);
      servo1.write(M2_timing);
      delay(800);
      servo2.write(M3_timing);
      delay(800);
      servo3.write(M4_timing);
      delay(800);
    }
    //
    if (pos1 == LOW){
      motor_a_pasos.step(pasos);
      pos = HIGH;  
    }
    
    M2_angulo = 61.0098;
    M3_angulo = 25.9079;
    M4_angulo = 73.0823;
    
    M2_timing = 11.555556*M2_angulo + 660;
    M3_timing = -11.111111*M3_angulo + 2300;
    M4_timing = 11.888889*M4_angulo + 750;
    
    servo1.writeMicroseconds(M2_timing);
    servo2.writeMicroseconds(M3_timing);
    servo3.writeMicroseconds(M4_timing);
  }
  
  else{ 
    
  }*/
   
}


void serialEvent() {
  while (Serial.available()) {
    elemento_serial = Serial.parseFloat(SKIP_WHITESPACE);
    elemento_serial = elemento_serial/100;
    if (j == 0){
      M1[i] = elemento_serial;
    }
    else if(j == 1){
      M2[i] = elemento_serial;
    }
    else if(j == 2){
     M3[i] = elemento_serial;
    }
    else if(j == 3){
     M4[i] = elemento_serial;
    }
    else{
      
    }
    i++;
    if(i == 30){
      j++;
      i=0;
      if(j == 4){
        digitalWrite(LED1, HIGH);
        digitalWrite(LED2, HIGH);
        digitalWrite(LED3, HIGH);
        j=0;
        listo_serial = true;
      }
    }
  }
}
