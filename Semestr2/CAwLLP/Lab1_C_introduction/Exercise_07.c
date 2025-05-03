#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {

    float hours;
    float minutes;
    float distance;
    scanf("%f", &hours);
    scanf("%f", &minutes);
    scanf("%f", &distance);
    printf("%f", distance/(hours+minutes/60));
    return 0;
}
