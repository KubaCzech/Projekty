#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

#define M_PI 3.14159265358979323846

int main() {

    float radius;
    float volume;
    scanf("%f", &radius);
    volume=M_PI*radius*radius*radius*4/3;
    printf("%f", volume);
    return 0;
}
