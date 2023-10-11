class InvalidOperandsError(Exception):
    pass

class Matrix(object):
    """Матрица размера mxn"""
    # Тут ваш код для хранения массива значений и размеров матрицы.

    # Добавьте конструктор класса.

    @staticmethod
    def identity(_n):
        """Статический метод. Альтернатива конструктору. Вернёт единичную матрицу nxn"""
        #ваш код вместо строчки ниже
        raise NotImplementedError

    @staticmethod
    def from_2d_array(array):
        """Статический метод. Альтернатива конструктору. Создаст матрицу mxn, если получит массив"""
        #ваш код вместо строчки ниже
        raise NotImplementedError

    def get_dimensions(self):
        """Вернёт tuple значений (m,n)"""
        #ваш код вместо строчки ниже
        raise NotImplementedError

    def equals(self, other):
        """Сравнить эту матрицу с другой, Вернёт True или False"""
        #ваш код вместо строчки ниже
        raise NotImplementedError

    def add(self, other):
        """Прибавить другую матрицу к этой, вернуть результат"""
        #Добавьте подобные проверки везде, где это нужно:
        m_1, n_1 = self.get_dimensions()
        m_2, n_2 = other.get_dimensions()
        if m_1!=m_2 or n_1!=n_2 :
            raise InvalidOperandsError

        #ваш код вместо строчки ниже
        raise NotImplementedError

    def dot(self, other):
        """Получить матричное произведение self*other, вернуть результат"""
        #ваш код вместо строчки ниже
        raise NotImplementedError

    def transpose(self, other):
        """Вернёт транспонированную матрицу"""
        #ваш код вместо строчки ниже
        raise NotImplementedError
