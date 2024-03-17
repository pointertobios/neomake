#include <stdio.h>

extern void test(int *a);

int main()
{
    int i = 5;
    printf("%d\n", i);
    test(&i);
    printf("%d\n", i);
    return 0;
}
