#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define SIZE 10000000  

int main() {
    int i;
    double start_time, end_time;
    double *A, *B, *C_seq, *C_parallel;

    A = (double *)malloc(SIZE * sizeof(double));
    B = (double *)malloc(SIZE * sizeof(double));
    C_seq = (double *)malloc(SIZE * sizeof(double));
    C_parallel = (double *)malloc(SIZE * sizeof(double));

    for (i = 0; i < SIZE; i++) {
        A[i] = i * 0.5;
        B[i] = i * 2.0;
    }


    start_time = omp_get_wtime();

    for (i = 0; i < SIZE; i++) {
        C_seq[i] = A[i] + B[i];
    }

    end_time = omp_get_wtime();
    printf("Sequential addition time: %.5f seconds\n", end_time - start_time);

 
    start_time = omp_get_wtime();

    #pragma omp parallel for
    for (i = 0; i < SIZE; i++) {
        C_parallel[i] = A[i] + B[i];
    }

    end_time = omp_get_wtime();
    printf("Parallel addition time (OpenMP): %.5f seconds\n", end_time - start_time);

    int errors = 0;
    for (i = 0; i < SIZE; i++) {
        if (C_seq[i] != C_parallel[i]) {
            errors++;
        }
    }

    if (errors == 0)
        printf("✅ Results are correct. Parallel and sequential outputs match.\n");
    else
        printf("❌ Mismatch found in results: %d errors.\n", errors);

    free(A);
    free(B);
    free(C_seq);
    free(C_parallel);

    return 0;
}
