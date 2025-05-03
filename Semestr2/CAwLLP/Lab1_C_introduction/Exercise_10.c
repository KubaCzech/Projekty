#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {

    float a;
    float b;
    float c;
    scanf("%f", &a);
    scanf("%f", &b);
    scanf("%f", &c);
    if (a+b>c && a+c>b && b+c>a)
        printf("%s", "Yes");
    else
        printf("%s", "No");
    return 0;
}
