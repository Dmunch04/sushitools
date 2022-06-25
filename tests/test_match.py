from sushitools.types import dataenum


def test_match_dataenum():
    Color = dataenum(
        "Color",
        [
            ("RGB", "r", "g", "b"),
            ("RGBA", "r", "g", "b", "a"),
            ("HEX", "hex"),
            ("HSL", "h", "s", "l"),
            ("HSLA", "h", "s", "l", "a"),
        ],
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
