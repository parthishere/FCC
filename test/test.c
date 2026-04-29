#include <stdio.h>

int main(){
    int a = 0;
    int b = 0; 
    int c = 0;
    {
        int a = 1;
        int b = 1;
        {
            int a = 2;
            printf("%d\n", a);
            printf("%d\n", b);
            printf("%d\n", c);
        }
        printf("%d\n", a);
        printf("%d\n", b);
        printf("%d\n", c);
    }
    printf("%d\n", a);
    printf("%d\n", b);
    printf("%d\n", c);
    return 0;
}