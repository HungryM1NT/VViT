a, b, c = map(float, input().split())
d = b**2 - 4 * a * c
if d >= 0:
    if a != 0:
        x1 = (-b + d**0.5) / (2 * a)
        x2 = (-b - d**0.5) / (2 * a)
        if x1 != x2:
            print(x1, x2)
        else:
            print(x1)
    elif b != 0:
        print(-c / b)
    elif c == 0:
        print("Любое число")
    else:
        print("Корней нет")
else:
    print("Корней нет")
