from sushitools import label, goto


class A:
    def b(self):
        label("c")


def test_goto():
    #A().b()

    x: int = 10
    label("a")
    if x > 0:
        print(x)
        x -= 1
        goto("a")
    print("END")