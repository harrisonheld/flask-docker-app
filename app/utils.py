import random, string

def random_name():
    return "Guest" + ''.join(random.choices(string.digits, k=3))

def random_color():
    return "#" + ''.join(random.choices('0123456789ABCDEF', k=6))
