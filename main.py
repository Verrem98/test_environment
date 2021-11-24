

q = 'whatever'

with open('test.txt', 'r') as file:
    for x in (file.readlines()):
        print(x)