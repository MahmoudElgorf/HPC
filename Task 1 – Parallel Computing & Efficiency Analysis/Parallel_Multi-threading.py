import time
import random
from concurrent.futures import ThreadPoolExecutor

N = 800
A = [[random.random() for _ in range(N)] for _ in range(N)]
B = [[random.random() for _ in range(N)] for _ in range(N)]
C = [[0.0 for _ in range(N)] for _ in range(N)]

def multiply_range(start, end):
    for i in range(start, end):
        for j in range(N):
            s = 0
            for k in range(N):
                s += A[i][k] * B[k][j]
            C[i][j] = s

num_threads = 4
chunk = N // num_threads
ranges = [(i*chunk, (i+1)*chunk if i < num_threads-1 else N) for i in range(num_threads)]

start = time.time()

with ThreadPoolExecutor(max_workers=num_threads) as executor:
    for r in ranges:
        executor.submit(multiply_range, r[0], r[1])

end = time.time()
print(f"Parallel time ({num_threads} threads): {end - start:.2f} seconds")
