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
