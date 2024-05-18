from functools import lru_cache

@lru_cache(maxsize=6)
def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)

# def fib_iter(n):
#     a, b = 0, 1
#     for _ in range(n):
#         a, b = b, a + b
#     return a

print(fib(1000))
