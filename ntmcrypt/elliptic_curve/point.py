import gmpy2


class Params:
    def __init__(self, a: int, b: int, p: int, q: int):
        self.a: int = a
        self.b: int = b
        self.p: int = p
        self.q: int = q

    def __str__(self):
        return f"Elliptic curve params:\n" \
               f"a = {self.a}\n" \
               f"b = {self.b}\n" \
               f"p = {self.p}\n" \
               f"q = {self.q}\n"

    def __eq__(self, other):
        if self.a == other.a and \
                self.b == other.b and \
                self.p == other.p and \
                self.q == other.q:
            return True
        else:
            return False

    def __ne__(self, other):
        if self == other:
            return False
        else:
            return True


class Point:
    def __init__(self, x: int, y: int, params: Params, at_infinity: bool = False):
        self.x: int = x
        self.y: int = y
        # point at infinity or not
        self.at_infinity: bool = at_infinity

        self.curve: Params = params

    def inverse(self):
        y = -self.y % self.curve.p
        return Point(self.x, y, self.curve)

    def __neg__(self):
        return self.inverse()

    def __str__(self):
        return f"({self.x};{self.y})"

    def __add__(self, other):
        if self.curve != other.curve:
            raise Exception("Elliptic curves are different")

        if self.at_infinity:
            return other

        if other.at_infinity:
            return self

        if self.x == other.x and self.y != other.y:
            return Point(0, 0, self.curve, True)

        if self.y == other.y == 0:
            return Point(0, 0, self.curve, True)

        if self == other:
            m = (3 * self.x ** 2 + self.curve.a) * \
                gmpy2.invert(2 * self.y, self.curve.p) % self.curve.p
        else:
            m = (self.y - other.y) * gmpy2.invert(self.x - other.x, self.curve.p)

        xr = (m**2 - self.x - other.x) % self.curve.p
        yr = (m*(self.x - xr) - self.y) % self.curve.p
        return Point(xr, yr, self.curve)

    def __iadd__(self, other):
        return self + other

    def __mul__(self, other):
        if type(other) is not int:
            raise Exception("The scalar must be of type int.")

        result = Point(0, 0, self.curve, True)
        addend = Point(self.x, self.y, self.curve)

        for bit in bin(other)[2::][::-1]:
            if bit == "1":
                result += addend
            addend += addend

        return result

    def __imul__(self, other):
        return self * other

    def __eq__(self, other):
        if self.x == other.x and \
                self.y == other.y and \
                self.curve == other.curve and \
                self.at_infinity == other.at_infinity:
            return True
        else:
            return False

    def __ne__(self, other):
        if self == other:
            return False
        else:
            return True
