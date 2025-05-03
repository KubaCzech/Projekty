#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

void mirror (char s[101]){
    int n=strlen(s);
    int x=0;
    //printf ("%d", n);
    for (int i=0; i<=n/2; i++)
        if(s[i]!=s[n-i-1]){
            printf("%s", "No");
            x++;
            break;
        }
    if(x==0)
        printf("%s", "Yes");
}

int main() {
    char s[101];
    scanf("%s", s);
    //printf("%s", s);
    mirror(s);
    return 0;
}
