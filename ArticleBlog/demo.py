
def outer(func):
    def inner():
        func()
    return inner


@outer
def demo():
    print("hello")
    return "hello"


demo = outer(demo)


res = demo()
print (res)

