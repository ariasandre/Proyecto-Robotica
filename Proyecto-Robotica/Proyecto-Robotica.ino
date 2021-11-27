// Se incluyen las librerias
#include <Stepper.h>
#include <Servo.h>

// Se definen las varibles y constantes del motor a pasos
const float pasos_por_rev = 32;
const float reduccion = 64;
float pasos = 0; 
float M1_angulo = -17.74; // Posición de reposo
Stepper motor_a_pasos(pasos_por_rev, 8,10,9,11);

// Se definen las variables para el servo 1
Servo servo1;
float M2_angulo = 44.42; // Posición de reposo
float M2_timing;

// Se definen las variables para el servo 2
Servo servo2;
float M3_angulo = 46.26; // Posición de reposo
float M3_timing;

// Se definen las variables para el servo 3
Servo servo3;
float M4_angulo = 59.31 ; // Posición de reposo
float M4_timing;

// Se definen otros pines de interes
int pin_inicio = 12; // Pin inicio de secuencia
int LED1 = 2, LED2 = 4, LED3 = 7;
bool pos1 = LOW;

// Se definen otras variables de interes
bool value;
bool inicial = false;

// Se definen variables para Serial
float elemento_serial = 0;
float M1[30];
float M2[30];
float M3[30];
float M4[30];
int i = 0;
int j = 0;
int k = 0;
bool letra_o = false;
int resets = 0;
int proximo = 3;
bool listo_serial = false;

// Se realiza la confuguración inicial
void setup() {
  // Configuración de pines
  pinMode(pin_inicio,INPUT);
  pinMode(LED1,OUTPUT);
  pinMode(LED2,OUTPUT);
  pinMode(LED3,OUTPUT);
  servo1.attach(3);
  servo2.attach(5);
  servo3.attach(6);

  // Configuración del puerto serial
  Serial.begin(9600);
  Serial.setTimeout(10);
}

void loop() {
  //-----------------Definición posición de reposo------------------//
  // Configuración del motor a pasos
  motor_a_pasos.setSpeed(300);
  pasos = round(5.688889*M1_angulo);

  // Configuración de los servos
  M2_timing = round(11.555556*M2_angulo + 660); //0 - 90
  M3_timing = round(-11.111111*M3_angulo + 2300); // 0 - 90
  M4_timing = round(11.888889*M4_angulo + 750); //750-1820

  // Posición Incial
  servo1.writeMicroseconds(M2_timing);
  servo2.writeMicroseconds(M3_timing);
  servo3.writeMicroseconds(M4_timing);
  inicial = digitalRead(pin_inicio);
  if (inicial){
    motor_a_pasos.step(pasos);
  }

  //-----------------------Inicio de secuencia-----------------------//
  // Inicia la secuencia cuando se haya recibido la trama de datos
  if(listo_serial){
    // Rayando las letras A
    if((k == 1|| k == 2 || k == 5 || k == 6 ||k == 9 || k == 10) && (letra_o == false)){

      // Si se esta haciendo el trazo horizontal de la A
      if (k == 10){
        motor_a_pasos.setSpeed(1000);
      }
      else{
        motor_a_pasos.setSpeed(300);
      }

      // Se realiza la secuencia
      for (int i_for = 0; i_for < 30; i_for++){
        // Se realiza la conversion para la funciones y se redondean los valores
        pasos = round(5.688889*M1[i_for]);
        M2_timing = round(11.555556*M2[i_for] + 660); //0 - 90
        M3_timing = round(-11.111111*M3[i_for] + 2300); // 0 - 90
        M4_timing = round(11.888889*M4[i_for] + 750); //750-1820

        // Se evalua el valor obtenido
        servo3.writeMicroseconds(M4_timing);
        servo2.writeMicroseconds(M3_timing);
        servo1.writeMicroseconds(M2_timing);
        motor_a_pasos.step(pasos);
        delay(50);
      }
      
      // Se mantiene la posicion final
      M2_angulo = M2[29];
      M3_angulo = M3[29];
      M4_angulo = M4[29];
  
      // Se activa la recepcion de datos y se habilita el envio de datos de la pc
      listo_serial = false;
      Serial.println(proximo);
    }

    // Rayando la letra O
    else if ((k == 1|| k == 2 || k == 3 || k == 6 ||k == 7 || k == 8) && (letra_o == true) ){
      // Se configura la velocidad del motor
      motor_a_pasos.setSpeed(300);

      // Se realiza la secuencia
      for (int i_for = 0; i_for < 30; i_for++){
        // Se realiza la conversion para la funciones y se redondean los valores
        pasos = round(5.688889*M1[i_for]);
        M2_timing = round(11.555556*M2[i_for] + 660);
        M3_timing = round(-11.111111*M3[i_for] + 2300);
        M4_timing = round(11.888889*M4[i_for] + 750);

        // Se evalua el valor obtenido
        servo3.writeMicroseconds(M4_timing);
        servo2.writeMicroseconds(M3_timing);
        servo1.writeMicroseconds(M2_timing);
        motor_a_pasos.step(pasos);
        delay(50);
      }
      
      // Se mantiene la posicion final
      M2_angulo = M2[29];
      M3_angulo = M3[29];
      M4_angulo = M4[29];

      // Se activa la recepcion de datos y se habilita el envio de datos de la pc
      listo_serial = false;
      Serial.println(proximo);
    }

    // Realizando movimientos libres
    else{
      // Se configura la velocidad del motor
      motor_a_pasos.setSpeed(300);

      // Se realiza la secuencia
      for (int i_for = 0; i_for < 30; i_for++){
        // Se realiza la conversion para la funciones y se redondean los valores
        pasos = round(5.688889*M1[i_for]);
        M2_timing = round(11.555556*M2[i_for] + 660);
        M3_timing = round(-11.111111*M3[i_for] + 2300);
        M4_timing = round(11.888889*M4[i_for] + 750);

        // Cambia la configuracion de las velocidades para un caso específico de la letra O
        if((k == 5) && (letra_o == true)){
          servo3.writeMicroseconds(M4_timing);
          delay(1000);
          servo2.writeMicroseconds(M3_timing);
          delay(1000);
          servo1.writeMicroseconds(M2_timing);
          delay(1000);
          motor_a_pasos.step(pasos);
          delay(400);
        }
        // Si no se mantiene la configuracion inicial
        else{ 
          servo3.writeMicroseconds(M4_timing);
          delay(650);
          servo2.writeMicroseconds(M3_timing);
          delay(650);
          servo1.writeMicroseconds(M2_timing);
          delay(650);
          motor_a_pasos.step(pasos);
          delay(200);
        }
      }

      // Se mantiene la posicion final
      M2_angulo = M2[29];
      M3_angulo = M3[29];
      M4_angulo = M4[29];

      // Se activa la recepcion de datos y se habilita el envio de datos de la pc
      listo_serial = false;
      Serial.println(proximo);
    }
  }
  
  // Control de LEDs mientras se reciben datos
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
}

//---------------Handler de las interrumpciones del arduino----------------//
// Funcion encargada de manejar donde se almacenan los datos provenientes de
// la pc e iniciar la ejecucion del proceso una vez recibidos los datos
void serialEvent() {
  // Si hay un dato en el buffer de entrada
  while (Serial.available()) {
    // Se recibe el dato, se convierte a flotante y se convierte
    elemento_serial = Serial.parseFloat(SKIP_WHITESPACE);
    elemento_serial = elemento_serial/100;

    // Almacena el dato recibido en funcion del actuador al que pertenezca
    if (j == 0){
      // Datos del motor a pasos
      M1[i] = elemento_serial;
    }
    else if(j == 1){
      // Datos del servomotor 1
      M2[i] = elemento_serial;
    }
    else if(j == 2){
      // Datos del servomotor 2
      M3[i] = elemento_serial;
    }
    else if(j == 3){
      // Datos del servomotor 3
      M4[i] = elemento_serial;
    }
    else{
      // Si llegan mas datos los desecha
    }
    
    // Control de contadores
    i++;
    if(i == 30){
      // Cada 30 elementos cambia el arreglo en el que se almacenan
      // los datos y reinicia el contador i
      j++;
      i=0;

      // Una vez que se hayan recibido las 4 tramas de datos coloca los leds en una configuracion
      // especifica y configura ciertas banderas
      if(j == 4){
        digitalWrite(LED1, HIGH);
        digitalWrite(LED2, HIGH);
        digitalWrite(LED3, HIGH);
        j=0;

        // Si se completa el trazo de la letra A
        if (k == 11){
          // Se reinicia el recuento de trazos recibidos y se aumenta en 1 la cantidad de resets
          // realizados
          k = 0;
          resets++;

          // Si ya se dibujaron las dos A coloque la bandera en alto para indicar que se trazara la o
          if (resets == 2){
            letra_o = true;
          }
        }
        
        // Si aun no se ha completado la ejecucion de la letra aumente el contador de trazos
        else{
          k++;
        }
        
        // Indique que fue recibido un punto al cual moverse
        listo_serial = true;
      }
    }
  }
}
