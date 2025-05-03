#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {

    float meters;
    scanf("%f", &meters);
    float miles=meters*0.621371192/1000;
    printf("%f", miles);
    return 0;
}
