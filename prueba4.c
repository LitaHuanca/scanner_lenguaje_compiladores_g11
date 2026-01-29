/*
 * PRUEBA 4: MÚLTIPLES ELSE IF Y ESTRUCTURAS COMPLEJAS
 * Este archivo prueba específicamente cadenas de else if
 * y anidamiento con while dentro de if/else
 */

#include <stdio.h>

int main() {
    int nota = 85;
    int edad = 20;
    int intentos = 0;
    
    // Prueba 1: Múltiples else if encadenados
    if (nota >= 90) {
        printf("Calificación: A\n");
    } else if (nota >= 80) {
        printf("Calificación: B\n");
    } else if (nota >= 70) {
        printf("Calificación: C\n");
    } else if (nota >= 60) {
        printf("Calificación: D\n");
    } else {
        printf("Calificación: F\n");
    }
    
    // Prueba 2: While dentro de if con else if
    if (edad < 18) {
        printf("Menor de edad\n");
        
        while (intentos < 3) {
            printf("Intento: %d\n", intentos);
            intentos = intentos + 1;
        }
        
    } else if (edad >= 18 && edad < 65) {
        printf("Adulto\n");
        
        int contador = 0;
        while (contador < 2) {
            if (contador == 1) {
                printf("Segunda iteración\n");
            }
            contador = contador + 1;
        }
        
    } else {
        printf("Adulto mayor\n");
    }
    
    // Prueba 3: if anidado dentro de while con else if
    int x = 0;
    while (x < 5) {
        if (x == 0) {
            printf("x es cero\n");
        } else if (x == 1) {
            printf("x es uno\n");
        } else if (x == 2) {
            printf("x es dos\n");
        } else {
            printf("x es mayor que dos\n");
        }
        x = x + 1;
    }
    
    // Prueba 4: Anidamiento profundo con else if
    int nivel = 2;
    if (nivel == 1) {
        printf("Nivel 1\n");
        
        while (intentos < 5) {
            if (intentos == 3) {
                printf("Mitad del camino\n");
            }
            intentos = intentos + 1;
        }
        
    } else if (nivel == 2) {
        printf("Nivel 2\n");
        
        int i = 0;
        while (i < 3) {
            if (i == 0) {
                printf("Inicio\n");
            } else if (i == 1) {
                printf("Medio\n");
            } else {
                printf("Final\n");
            }
            i = i + 1;
        }
        
    } else if (nivel == 3) {
        printf("Nivel 3\n");
    } else {
        printf("Nivel desconocido\n");
    }
    
    return 0;
}
