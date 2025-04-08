from .utils import Color


class Pattern(list):
    BLOCKS = {Color.GREEN: "🟩", Color.YELLOW: "🟨", Color.GREY: "⬜"}

    def __init__(self, colors=list[Color | int | str]):
        if len(colors) != 5:
            raise ValueError("Invalid number of colors!")

        for color in colors:
            if type(color) is Color:
                self.append(color)
            elif type(color) is int:
                self.append(Color(color))
            elif type(color) is str:
                self.append(Color(int(color)))

    def is_winning(self):
        return all(map(lambda color: color == Color.GREEN, self))

    def __str__(self):
        return " ".join([self.BLOCKS[color] for color in self])

    def __hash__(self):
        output = 0
        for color in self:
            output *= 10
            output += color.value
        return output
