class MatrixBase:
    def __init__(self, rows, cols, default_value=0):
        self.rows = rows
        self.cols = cols
        self.data = [[default_value for _ in range(cols)] for _ in range(rows)]

    def input(self):
        raise NotImplementedError("Метод input() должен быть реализован")

    def display(self):
        for row in self.data:
            print(" ".join(f"{elem:8}" for elem in row))

    def at(self, row, col):
        if row >= self.rows or col >= self.cols:
            raise IndexError("Индекс вне диапазона")
        return self.data[row][col]

    def set(self, row, col, value):
        if row >= self.rows or col >= self.cols:
            raise IndexError("Индекс вне диапазона")
        self.data[row][col] = value

    def transpose(self):
        result = self.__class__(self.cols, self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                result.set(j, i, self.at(i, j))
        return result

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError("Матрицы должны быть одного типа для сложения")
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Размеры матриц должны совпадать для сложения")
        result = self.__class__(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result.set(i, j, self.at(i, j) + other.at(i, j))
        return result

    def __mul__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError("Матрицы должны быть одного типа для умножения")
        if self.cols != other.rows:
            raise ValueError("Размеры матриц должны совпадать для умножения")
        result = self.__class__(self.rows, other.cols)
        for i in range(self.rows):
            for j in range(other.cols):
                result.set(i, j, sum(self.at(i, k) * other.at(k, j) for k in range(self.cols)))
        return result


class Matrix(MatrixBase):
    def input(self):
        print(f"Введите элементы матрицы построчно ({self.rows}x{self.cols}):")
        for i in range(self.rows):
            self.data[i] = list(map(int, input().split()))


class DiagonalMatrix(MatrixBase):
    def __init__(self, size, default_value=0):
        super().__init__(size, size, default_value)
        self.diagonal = [default_value for _ in range(size)]

    def set(self, index, value):
        if index >= self.size:
            raise IndexError("Индекс вне диапазона")
        self.diagonal[index] = value
        super().set(index, index, value)

    def at(self, index):
        if index >= self.size:
            raise IndexError("Индекс вне диапазона")
        return self.diagonal[index]

    def input(self):
        print(f"Введите {self.size} элементов для диагонали:")
        self.diagonal = list(map(int, input().split()))
        for i in range(self.size):
            super().set(i, i, self.diagonal[i])

    def transpose(self):
        # Диагональная матрица неизменна при транспонировании
        return self


class BandMatrix(Matrix):
    def __init__(self, rows, cols, bandwidth, default_value=0):
        super().__init__(rows, cols, default_value)
        self.bandwidth = bandwidth

    def input(self):
        print(f"Введите элементы для ленточной матрицы:")
        for i in range(self.rows):
            for j in range(self.cols):
                if abs(i - j) <= self.bandwidth:
                    self.set(i, j, int(input(f"Элемент ({i},{j}): ")))
                else:
                    self.set(i, j, 0)


class MatrixAdapter:
    @staticmethod
    def from_string(s, rows, cols):
        elements = list(map(int, s.split()))
        if len(elements) != rows * cols:
            raise ValueError("Некорректный формат строки для матрицы")
        mat = Matrix(rows, cols)
        for i in range(rows):
            mat.data[i] = elements[i * cols:(i + 1) * cols]
        return mat

    @staticmethod
    def from_file(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        rows = len(lines)
        cols = len(lines[0].split())
        mat = Matrix(rows, cols)
        for i, line in enumerate(lines):
            mat.data[i] = list(map(int, line.split()))
        return mat


def main():
    try:
        print("Выберите операцию:")
        print("1. Сложение матриц")
        print("2. Умножение матриц")
        print("3. Транспонирование матрицы")
        print("4. Диагональная матрица")
        print("5. Ленточная матрица")

        choice = int(input())
        if choice == 1 or choice == 2:
            rows, cols = map(int, input("Введите количество строк и столбцов для первой матрицы: ").split())
            mat1 = Matrix(rows, cols)
            mat1.input()

            rows, cols = map(int, input("Введите количество строк и столбцов для второй матрицы: ").split())
            mat2 = Matrix(rows, cols)
            mat2.input()

            if choice == 1:
                print("Результат сложения:")
                (mat1 + mat2).display()
            else:
                print("Результат умножения:")
                (mat1 * mat2).display()

        elif choice == 3:
            rows, cols = map(int, input("Введите количество строк и столбцов: ").split())
            mat = Matrix(rows, cols)
            mat.input()
            print("Транспонированная матрица:")
            mat.transpose().display()

        elif choice == 4:
            size = int(input("Введите размер диагональной матрицы: "))
            diag = DiagonalMatrix(size)
            diag.input()
            print("Диагональная матрица:")
            diag.display()

        elif choice == 5:
            rows, cols, bandwidth = map(int, input("Введите количество строк, столбцов и ширину ленты: ").split())
            band = BandMatrix(rows, cols, bandwidth)
            band.input()
            print("Ленточная матрица:")
            band.display()

        else:
            print("Неверный выбор.")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
