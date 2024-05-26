import requests


def for_test():
    a = 10
    b = 4
    for i in range(b, a):
        print(i)


def try_test_1():
    try:
        for i in range(10):
            if i == 5:
                a = 5 / 0
            print(i)
    except Exception as e:
        print("exception")
        # print(e)
    finally:
        print("finally")


def try_test_2():
    for i in range(10):
        try:
            print(i)
            if i == 5:
                a = 5 / 0
        except Exception as e:
            print("exception")
            # print(e)
        finally:
            print("finally")


def test_3(id):
    if id == 1:
        return 1, 2
    else:
        return None,None


if __name__ == '__main__':
    a, b = test_3(2)
    print(a, b)
