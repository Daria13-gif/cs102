first = int(input())
operation = input()
second = int(input())

if operation == "+":
    print(first + second)
elif operation == "-":
    print(first - second)
elif operation == "*":
    print(first * second)
elif operation == "/":
    if second == 0:
        print("Exception")
    else:
        print(first / second)
