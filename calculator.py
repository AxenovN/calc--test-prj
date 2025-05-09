def sum(a, b):
    """Возвращает сумму двух чисел a и b."""
    return a + b

# Пример использования функции
if __name__ == "__main__":
    num1 = float(input("Введите первое число: "))
    num2 = float(input("Введите второе число: "))
    result = sum(num1, num2)
    print(f"Сумма {num1} и {num2} равна {result}")
