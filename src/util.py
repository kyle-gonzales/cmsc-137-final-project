def stringify_tuple(t):
    output = ""
    for item in t[:-1]:
        output += str(item) + ","
    output += str(t[-1])

    return output


print(stringify_tuple((1, 2, 3, 5)))
