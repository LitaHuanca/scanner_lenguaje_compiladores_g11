/*
 * PRUEBA 3: ANIDAMIENTO EXTREMO - DEMOSTRACIÓN DE PILA PROFUNDA
 * Este archivo prueba el límite del autómata de pila
 * con anidamiento de hasta 6 niveles
 */

#include <stdio.h>

int main() {
    int a = 1, b = 2, c = 3, d = 4, e = 5, f = 6;
    int resultado = 0;
    
    // ANIDAMIENTO NIVEL 1
    if (a > 0) {
        printf("Nivel 1: a es positivo\n");
        
        // ANIDAMIENTO NIVEL 2
        while (b < 5) {
            printf("Nivel 2: while de b\n");
            
            // ANIDAMIENTO NIVEL 3
            if (c > 2) {
                printf("Nivel 3: c mayor que 2\n");
                
                // ANIDAMIENTO NIVEL 4
                while (d < 6) {
                    printf("Nivel 4: while de d\n");
                    
                    // ANIDAMIENTO NIVEL 5
                    if (e == 5) {
                        printf("Nivel 5: e es 5\n");
                        
                        // ANIDAMIENTO NIVEL 6
                        while (f < 8) {
                            printf("Nivel 6: while de f\n");
                            resultado = a + b + c + d + e + f;
                            f = f + 1;
                        }
                        
                    } else {
                        printf("Nivel 5: e no es 5\n");
                    }
                    
                    d = d + 1;
                }
                
            } else if (c == 2) {
                printf("Nivel 3: c es exactamente 2\n");
            } else {
                printf("Nivel 3: c es menor que 2\n");
            }
            
            b = b + 1;
        }
        
    } else {
        printf("Nivel 1: a no es positivo\n");
    }
    
    printf("Resultado: %d\n", resultado);
    
    // Segunda estructura con anidamiento profundo
    int x = 10;
    if (x > 5) {
        printf("x mayor que 5\n");
        
        int y = 0;
        while (y < 3) {
            if (y == 0) {
                printf("y es cero\n");
                
                int z = 0;
                while (z < 2) {
                    if (z == 0) {
                        printf("z es cero\n");
                        
                        int w = 0;
                        while (w < 2) {
                            if (w == 1) {
                                printf("Nivel muy profundo alcanzado\n");
                            }
                            w = w + 1;
                        }
                        
                    } else {
                        printf("z es uno\n");
                    }
                    z = z + 1;
                }
                
            } else if (y == 1) {
                printf("y es uno\n");
            } else {
                printf("y es dos\n");
            }
            y = y + 1;
        }
    }
    
    return 0;
}
