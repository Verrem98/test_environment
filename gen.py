def norm():


    numb = []
    for x in range(5):
        numb.append(x)

    return numb

def gen():

    for x in range(5):
        yield x


print(norm())
