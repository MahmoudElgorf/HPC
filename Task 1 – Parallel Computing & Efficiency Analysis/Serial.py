import time
import random

N = 800
A = [[random.random() for _ in range(N)] for _ in range(N)]
B = [[random.random() for _ in range(N)] for _ in range(N)]
C = [[0.0 for _ in range(N)] for _ in range(N)]

start = time.time()

for i in range(N):
    for j in range(N):
        s = 0
        for k in range(N):
            s += A[i][k] * B[k][j]
        C[i][j] = s

end = time.time()
print(f"Serial time: {end - start:.2f} seconds")
