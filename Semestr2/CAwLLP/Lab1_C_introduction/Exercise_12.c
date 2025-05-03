#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

void recursion (a, b){
    if (a%b!=0)
        printf("%s", "No");
    else
        if(a==b) //Base case is when after the divisions of a by b is equal to b
            printf("%s", "Yes");
        else
            recursion (a/b, b);

}

int main() {

    int a, b;
    scanf("%d", &a);
    scanf("%d", &b);
    recursion(a, b);
    return 0;
}
