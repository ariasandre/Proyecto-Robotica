// Se agregan las librerias necesarias
#include <Stepper.h>
#include <Servo.h>

// Se definen las varibles y constantes del motor a pasos
const float pasos_por_rev = 32;
const float reduccion = 64;
float pasos = 0; 
float M1_angulo = 0; // Posición de reposo
Stepper motor_a_pasos(pasos_por_rev, 8,10,9,11);

// Se definen las variables para el servo 1
Servo servo1;
float M2_angulo = 30; // Posición de reposo
float M2_timing;

// Se definen las variables para el servo 2
Servo servo2;
float M3_angulo = 50; // Posición de reposo
float M3_timing;

// Se definen las variables para el servo 3
Servo servo3;
float M4_angulo = 30; // Posición de reposo
float M4_timing;

// Se definen otros pines de interes
int pin_inicio = 2; // Pin inicio de secuencia
bool pos1 = LOW;

//Se definen otras variables de interes
bool value;

void setup() {
  // Configuración de pines
  pinMode(pin_inicio,INPUT);
  servo1.attach(3);
  servo2.attach(5);
  servo3.attach(6);
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

  // Lectura del inicio
  value = digitalRead(pin_inicio);
  
  if(value == HIGH)
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
    }*/
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

  }
   
}
