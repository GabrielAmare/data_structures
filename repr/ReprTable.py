class Box:
    def __init__(self, value, xjust, yjust):
        self.lines = str(value).split('\n')
        assert xjust in ('L', 'C', 'R')  # Left / Center / Right
        assert yjust in ('B', 'M', 'T')  # Bottom / Middle / Top
        self.xjust = xjust
        self.yjust = yjust

    @property
    def dim(self) -> tuple:
        width = max(map(len, self.lines))
        height = len(self.lines)
        return width, height

    def format(self, pad_x: int, pad_y: int, width: int, height: int, char: str) -> list:
        xjust = {
            'L': str.ljust,
            'C': str.center,
            'R': str.rjust
        }[self.xjust]

        def y_just(lines, height, fill_line, mode):
            empty = height - 2 * pad_y - len(lines)
            if mode == 'T':
                top_c = 0
                bot_c = empty
            elif mode == 'M':
                top_c = empty // 2
                bot_c = empty - top_c
            elif mode == 'B':
                top_c = empty
                bot_c = 0
            else:
                raise Exception
            return (top_c + pad_y) * [fill_line] + lines + (bot_c + pad_y) * [fill_line]

        return y_just([pad_x * char + xjust(line, width - 2 * pad_x, char) + pad_x * char for line in self.lines],
                      height, width * char, self.yjust)


class ReprTable:
    """
        This class can be used to make a representation of a regular table in the console
        You can set the charset of the grid, the justify (horizontal & vertical) and the padding (horizontal & vertical)
    """

    def __init__(self, table, charset="┌┬─┐├┼─┤││ │└┴─┘", just="LT", pad=(1, 0)):
        """
            Setup the ReprTable
            example :
            >>> rt = ReprTable([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
            >>> print(rt)
            will display :
            ┌───┬───┬────┬────┐
            │ 0 │ 1 │ 2  │ 3  │
            ├───┼───┼────┼────┤
            │ 4 │ 5 │ 6  │ 7  │
            ├───┼───┼────┼────┤
            │ 8 │ 9 │ 10 │ 11 │
            └───┴───┴────┴────┘
        :param table: The table to display
        :param charset: The charset to use for the grid (by default it's "┌┬─┐├┼─┤││ │└┴─┘")
        :param just: The justify parameter (by default "LT") the format of this parameter is {L|C|R}{T|M|B}
        :param pad: The padding to use (offset from the grid) to pass as (pad_x, pad_y) -> by default it's (1, 0)
        """
        self.table = table
        self.charset = charset
        self.xjust, self.yjust = just
        self.padx, self.pady = pad

    def __repr__(self):
        # Boxes for all the cells of the table
        boxes = [[Box(cell, self.xjust, self.yjust) for cell in row] for row in self.table]

        # Dimensions of each boxes
        dims = [[box.dim for box in row] for row in boxes]

        # Max width per column
        widths = [max(dim[0] for dim in col) + 2 * self.padx for col in zip(*dims)]

        # Max height per row
        heights = [max(dim[1] for dim in row) + 2 * self.pady for row in dims]

        # Regular dimensions for each cells of the table (>= to the previous ones)
        dims = [[(width, height) for width in widths] for height in heights]

        table = [
            [
                box.format(self.padx, self.pady, *dim, self.charset[10])
                for box, dim in zip(row_boxes, row_dims)
            ]
            for row_boxes, row_dims in zip(boxes, dims)
        ]

        T = self.charset[0] + self.charset[1].join(width * self.charset[2] for width in widths) + self.charset[3] + "\n"
        M = "\n" + self.charset[4] + self.charset[5].join(width * self.charset[6] for width in widths) + self.charset[
            7] + "\n"
        B = "\n" + self.charset[12] + self.charset[13].join(width * self.charset[14] for width in widths) + \
            self.charset[15]

        return T + M.join(
            "\n".join(
                self.charset[8] + self.charset[9].join(lines) + self.charset[11]
                for lines in zip(*row)
            )
            for row in table
        ) + B


if __name__ == '__main__':
    rt = ReprTable([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
    print(rt)
