def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def list_primes_below(n):
    primes = []
    for i in range(2, n):
        if is_prime(i):
            primes.append(i)
    return primes

if __name__ == "__main__":
    try:
        number = int(input("数値を入力してください: "))
        if number <= 0:
            print("正の整数を入力してください。")
        else:
            primes = list_primes_below(number)
            print(f"{number}より小さい素数: {primes}")
    except ValueError:
        print("有効な整数を入力してください。")