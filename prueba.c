/*
 * Programa de prueba para el Scanner de C
 * Este archivo contiene diversos elementos del lenguaje C
 * para probar todas las capacidades del analizador léxico
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Definición de constantes
#define PI 3.14159
#define MAX_SIZE 100

// Declaración de variables globales
int contador = 0;
float promedio = 0.0;
double precision = 1.5e-10;

// Comentario de una línea sobre estructuras
struct Estudiante {
    char nombre[50];
    int edad;
    float notas[5];
    double promedio_final;
};

/* 
 * Comentario de múltiples líneas
 * Esta es una enumeración de días
 */
enum DiaSemana {
    LUNES,
    MARTES,
    MIERCOLES,
    JUEVES,
    VIERNES,
    SABADO,
    DOMINGO
};

// Función para calcular el factorial
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

// Función para calcular promedio
float calcular_promedio(float numeros[], int cantidad) {
    float suma = 0.0;
    
    for (int i = 0; i < cantidad; i++) {
        suma += numeros[i];
    }
    
    return suma / cantidad;
}

/* Función principal del programa */
int main() {
    // Variables locales
    int x = 10;
    int y = 20;
    int z = 0;
    float resultado = 0.0f;
    double valor_grande = 1.23e5;
    char letra = 'A';
    unsigned int positivo = 42u;
    long numero_largo = 1000000L;
    
    // Operaciones aritméticas
    z = x + y;
    z = x - y;
    z = x * y;
    z = x / y;
    z = x % y;
    
    // Operaciones de incremento y decremento
    x++;
    y--;
    ++x;
    --y;
    
    // Operadores de asignación compuesta
    x += 5;
    y -= 3;
    z *= 2;
    
    // Operadores de comparación
    if (x > y) {
        printf("x es mayor que y\n");
    } else if (x < y) {
        printf("x es menor que y\n");
    } else if (x == y) {
        printf("x es igual a y\n");
    }
    
    // Operadores lógicos
    if (x > 0 && y > 0) {
        printf("Ambos son positivos\n");
    }
    
    if (x > 100 || y > 100) {
        printf("Al menos uno es mayor que 100\n");
    }
    
    if (!(x == 0)) {
        printf("x no es cero\n");
    }
    
    // Operadores bit a bit
    int a = 5;
    int b = 3;
    int bit_and = a & b;
    int bit_or = a | b;
    int bit_xor = a ^ b;
    int bit_not = ~a;
    int shift_left = a << 2;
    int shift_right = a >> 1;
    
    // Estructura switch-case
    int opcion = 2;
    switch (opcion) {
        case 1:
            printf("Opción 1 seleccionada\n");
            break;
        case 2:
            printf("Opción 2 seleccionada\n");
            break;
        case 3:
            printf("Opción 3 seleccionada\n");
            break;
        default:
            printf("Opción no válida\n");
            break;
    }
    
    // Bucle while
    contador = 0;
    while (contador < 5) {
        printf("Contador: %d\n", contador);
        contador++;
    }
    
    // Bucle do-while
    int j = 0;
    do {
        printf("j = %d\n", j);
        j++;
    } while (j < 3);
    
    // Bucle for
    for (int k = 0; k < 10; k++) {
        if (k == 5) {
            continue; // Saltar cuando k es 5
        }
        if (k == 8) {
            break; // Salir del bucle cuando k es 8
        }
        printf("k = %d\n", k);
    }
    
    // Uso de arrays
    int numeros[5] = {1, 2, 3, 4, 5};
    float decimales[] = {1.1, 2.2, 3.3, 4.4, 5.5};
    
    // Punteros
    int *ptr = &x;
    int valor_apuntado = *ptr;
    
    // Operador ternario
    int max = (x > y) ? x : y;
    
    // Uso de struct
    struct Estudiante alumno;
    alumno.edad = 20;
    alumno.notas[0] = 85.5;
    alumno.notas[1] = 90.0;
    alumno.promedio_final = 87.75;
    
    // Operador sizeof
    int tamano = sizeof(int);
    int tamano_array = sizeof(numeros);
    
    // Números en diferentes formatos
    int decimal = 100;
    int hexadecimal = 0xFF;
    int octal = 0777;
    float flotante = 3.14159f;
    double doble = 2.71828;
    double cientifico = 6.022e23;
    double cientifico_neg = 1.6e-19;
    
    // Casting
    float f = 3.7f;
    int entero = (int)f;
    
    // Variables con diferentes tipos de almacenamiento
    static int variable_estatica = 100;
    register int variable_registro = 50;
    volatile int variable_volatil = 25;
    const int constante = 999;
    
    // Uso de typedef
    typedef unsigned long ulong;
    ulong numero_grande = 4294967295UL;
    
    // goto (aunque no es recomendado)
    int error = 0;
    if (error) {
        goto error_handler;
    }
    
    printf("Programa ejecutado exitosamente\n");
    
    // Llamar a función
    int fact = factorial(5);
    printf("Factorial de 5 = %d\n", fact);
    
    return 0;
    
error_handler:
    printf("Se produjo un error\n");
    return 1;
}

// Función adicional con extern
extern void funcion_externa();

// Union
union Dato {
    int entero;
    float flotante;
    char caracter;
};

// Variables con signed/unsigned
signed int numero_con_signo = -50;
unsigned int numero_sin_signo = 50;
short int corto = 10;
long int largo = 1000000;

// Función void
void imprimir_mensaje(void) {
    printf("Este es un mensaje de prueba\n");
}