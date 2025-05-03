#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {

    int books;
    scanf("%d", &books);
    float price=0;
    int boxes=0;
    if (books>10){
        price=400+35*(books-10);
        if (books>=40)
            price*=0.95;
    }
    else
        price=books*40;
    if (books%12==0)
        boxes=books/12;
    else
        boxes=(books/12)+1;
    if (boxes<=5)
        printf("%f", price+boxes*12);
    else
        printf("%f", price+60);
    return 0;
}
