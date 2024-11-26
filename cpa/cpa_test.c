#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <math.h>

#define startpoint 0
#define endpoint 125002

double cov(float *x, float *y, int size) {
    double Sxy = 0, Sx = 0, Sy = 0;
    int i;
    for(i = 0; i < size; i++){
        Sxy += x[i] * y[i]; //E(XY)
        Sx += x[i];
        Sy += y[i];
    }
    return (Sxy - Sx * Sy/(double) size) / (double)size;
}

double corr(float *x, float *y, int size) {
    double Sxy = 0, Sx = 0, Sy = 0, Sxx = 0, Syy = 0; //var(x) = E(X^2)-E(X)^2
    int i;
    for(i = 0; i < size; i++){
        Sxy += x[i] * y[i]; //E(XY)
        Sx += x[i];
        Sy += y[i];
        
        Sxx += x[i] * x[i];
        Syy += y[i] * y[i];
    }
    return ((double)size*Sxy - Sx*Sy)/sqrt(((double)size*Sxx - Sx*Sx)*((double)size*Syy - Sy*Sy));
}

int main() {
    float x[endpoint] = {0, };
    float y[endpoint] = {0, };
    for (int i = 0; i < endpoint; i++) {
        x[i] = i + 0.1;
    }
    for (int i = 0; i < endpoint; i++) {
        y[i] = i + 10 + 0.1;
    }
    printf("%lf, %lf\n", x[0], y[0]);
    printf("Cov: %lf, Corr: %lf", cov(x, y, endpoint), corr(x, y, endpoint));
}