import random
import tqdm

def clip(x: int) -> int:
    return max(0, min(100, x))

def fight(a: int, b: int) -> int:
    w1 = 0
    w2 = 0
    
    for _ in tqdm.trange(1_000_000):
        g = random.randrange(0, 101)
        
        if abs(a - g) < abs(b - g):
            w1 += 1
        
        if abs(b - g) < abs(a - g):
            w2 += 1
    
    if w1 > w2:
        return 0
    
    return 1

if __name__ == "__main__":
    a = 0
    gen = 1
    
    for _ in range(1000000):
        b = a
        while b == a:
            b = clip(random.randrange(a - 25, a + 26))
            
        if fight(a, b) == 1:
            gen += 1
            print(F"Gen {gen :>2}: {a} <- {b}")
            a = b

            input()