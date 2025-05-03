#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {
    int hours;
    scanf("%d", &hours);
    int minutes;
    scanf("%d", &minutes);
    int seconds=3600*hours+60*minutes;
    printf("%d", seconds);
    return 0;
}

