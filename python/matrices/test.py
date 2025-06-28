import unittest
from matrix import Matrix, InvalidOperandsError

class TestMatrixMethods(unittest.TestCase):
    def test_equals(self):
        E1 = Matrix.identity(5)
        E2 = Matrix.identity(5)
        E3 = Matrix.identity(6)
        self.assertTrue(E1.equals(E2))
        self.assertTrue(E1.equals(E1))
        self.assertFalse(E1.equals(E3))
        A = Matrix.from_2d_array([[1,2,3],[4,5,6]])
        B = Matrix.from_2d_array([[1,3,3],[4,5,6]])
        self.assertFalse(A.equals(B))
        self.assertTrue(A.equals(A))

    def test_identity(self):
        E_real = Matrix.identity(3)
        m, n = E_real.get_dimensions()
        self.assertTrue(m==3)
        self.assertTrue(n==3)
        E_expected = Matrix.from_2d_array([[1,0,0],[0,1,0],[0,0,1]])
        self.assertTrue(E_real.equals(E_expected))

    def test_add(self):
        A = Matrix.from_2d_array([[1,2],[0,5]])
        B = Matrix.from_2d_array([[1,3],[4,5]])
        E = Matrix.identity(5)
        with self.assertRaises(InvalidOperandsError):
            A.add(E)
        C_real = A.add(B)
        C_expected = Matrix.from_2d_array([[2,5],[4,10]])
        self.assertTrue(C_real.equals(C_expected))

    def test_dot(self):
        A = Matrix.from_2d_array([[1,2,3],[4,5,6]])
        E1 = Matrix.identity(3)
        E2 = Matrix.identity(2)
        with self.assertRaises(InvalidOperandsError):
            A.dot(A)
        AE = A.dot(E1)
        self.assertTrue(A.equals(AE))
        EA = E2.dot(A)
        self.assertTrue(A.equals(EA))

    def test_transpose(self):
        A = Matrix.from_2d_array([[1,2,3],[4,5,6]])
        B_real = A.transpose()
        B_expected = Matrix.from_2d_array([[1,4],[2,5],[3,6]])
        self.assertTrue(B_real.equals(B_expected))

if __name__ == '__main__':
    unittest.main()
