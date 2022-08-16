from sushitools.types import dataenum
from sushitools.cf import match


def test_match_dataenum():
    Color = dataenum(
        "Color",
        ("RGB", "r", "g", "b"),
        ("RGBA", "r", "g", "b", "a"),
        ("HEX", "hex"),
        ("HSL", "h", "s", "l"),
        ("HSLA", "h", "s", "l", "a"),
    )

    black = Color.HEX("#000000")

    black.match(
        (Color.RGB, lambda r, g, b: print(f"RGB: ({r}, {g}, {b})")),
        (Color.RGBA, lambda r, g, b, a: print(f"RGBA: ({r}, {g}, {b}, {a})")),
        (Color.HEX, lambda hex: print(f"HEX: {hex}")),
        (Color.HSL, lambda h, s, l: print(f"HSL: ({h}, {s}, {l})")),
        (Color.HSLA, lambda h, s, l, a: print(f"HSLA: ({h}, {s}, {l}, {a})")),
    )
    
    
def test_match_matchable():
    class Integer(match.Matchable):
        def __init__(self, val):
            self.val = val

        def get_values(self):
            return [self.val]

        def get_n_values(self):
            return 1

        def __eq__(self, other):
            return self.val == other


    sixtynine = Integer(69)
    sixtynine.match((50, lambda val: print("a")), (69, lambda val: print("b", val)))


    def cb(x):
        print("cb", x)


    seventy = Integer(70)
    seventy.match(
        (70, lambda: print("yeet")),
        (70, lambda x: print("yay", x)),
        (70, lambda x, y: print("gg", x, y)),
        (70, cb),
    )
    
    
def test_match_dataenum_noargs():
    Version = dataenum("Version", ("One"), ("Two"), ("Three"))

    version_one = Version.One
    version_one.match(
        (Version.One, lambda: print("v1")),
        (Version.Two, lambda: print("v2")),
        (Version.Three, lambda: print("v3")),
    )
    
def test_match_return_value():
    class Integer(match.Matchable):
        def __init__(self, val):
            self.val = val

        def get_values(self):
            return [self.val]

        def get_n_values(self):
            return 1

        def __eq__(self, other):
            if isinstance(other, Integer):
                return self.val == other.val
            else:
                return self.val == other
        
    one = Integer(1)
    res = one.match(
        (1, 1+1),
        (2, 2+1),
    )
    assert res == 2

    two = Integer(2)
    two = two.match(
        (1, Integer(1+2)),
        (2, Integer(2+2)),
    )
    assert two.val == 4
    
    three = Integer(3)
    result = three.match(
        (2, lambda val: val * val),
        (3, lambda val: val * val),
    )
    assert result == 9
    
    four = Integer(4)
    five = four.match(
        (Integer(5), lambda val: Integer(val)),
        (Integer(4), lambda val: Integer(val + 1)),
    )
    assert five.val == 5
    
    six = Integer(6).match(
        (five, lambda: Integer(6)),
        (five.val + 1, lambda val: Integer(val))
    )
    assert six.val == 6
    
def test_match_default_catch():
    class Person(match.Matchable):
        def __init__(self, name):
            self.name = name

        def get_values(self):
            return [self.name]

        def get_n_values(self):
            return 1

        def __eq__(self, other):
            if isinstance(other, Person):
                return self.name == other.name
            else:
                return self.name == other

    me = Person("Daniel")
    me.match(
        ("Bob", lambda: print("it's bob!")),
        default = lambda name: print("it's %s!" % name),
    )

    name = me.match(
        ("Michael", "Mike"),
        ("Richard", "Dick"),
        default = lambda p: p,
    )
    assert name == "Daniel"