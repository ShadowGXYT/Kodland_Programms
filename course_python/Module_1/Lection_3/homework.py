def double_letter(s):
    result = ''
    for letter in s:
        result += letter * 2
    return result

def secret_function(a, b):
    return str(a) + str(b)

print(double_letter("Hello"))
print(secret_function(1, 2))
print(secret_function("Hello, ", "world"))
