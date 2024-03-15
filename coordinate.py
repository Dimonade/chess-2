"""coordinates and vector for supporting the mathematics of the move calculations by the pieces"""

from constants import Letter


class Coordinate:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def values(self):
        return self.row, self.column

    def __str__(self):
        column_letter = Letter.num_to_lower(self.column)
        return f"{column_letter}{self.row}"

    def __add__(self, vector):
        self.row += vector.row
        self.column += vector.column
        return self

    @staticmethod
    def diff_vector(coordinate1, coordinate2):
        row = coordinate1.row - coordinate2.row
        column = coordinate1.column - coordinate2.column
        return column, row

    @classmethod
    def create_from_str(cls, string_in):
        column = Letter.to_num(string_in[0])
        row = int(string_in[1])
        return cls(row=row, column=column)

    @classmethod
    def create_from_strs(cls, string1, string2):
        return cls.create_from_str(string1), cls.create_from_str(string2)


class Vector:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    @classmethod
    def create_from_tuple(cls, tuple_in):
        return cls(tuple_in[0], tuple_in[1])
