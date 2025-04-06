from .colors import Color


class Pattern(list):
    BLOCKS = {Color.GREEN: "🟩", Color.YELLOW: "🟨", Color.GREY: "⬜"}

    def __init__(self, colors=list[Color]):
        if len(colors) != 5:
            raise ValueError("Invalid number of colors!")

        for color in colors:
            self.append(color)

    def is_winning(self):
        return all(map(lambda color: color == Color.GREEN, self))

    def __str__(self):
        return " ".join([self.BLOCKS[color] for color in self])
