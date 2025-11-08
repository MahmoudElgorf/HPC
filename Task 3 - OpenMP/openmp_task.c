#include <stdio.h>
#include <omp.h>

int main() {
    int i;
    printf("Parallel region started:\n");

    #pragma omp parallel for
    for(i = 0; i < 8; i++) {
        printf("Thread %d is working on iteration %d\n", omp_get_thread_num(), i);
    }

    printf("Parallel region ended.\n");
    return 0;
}
