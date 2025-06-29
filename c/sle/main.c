#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_M 256
#define MAX_N 256

struct Matrix {
  double** array;
  unsigned int m; //Высота, количество строк
  unsigned int n; //Ширина, число столбцов
};

//Создаёт матрицу, заполненную нулями
struct Matrix* constructMatrix (unsigned int m, unsigned int n) {
  /* TODO:Добавить проверки для m и n */
  struct Matrix *mat = malloc(sizeof(struct Matrix)); //Выделяется память под структуру
  mat->array = calloc(m, sizeof(double*)); //Выделяется память под массив указателей на строки
  for(int i=0;i<m;i++){
    mat->array[i] = calloc(n, sizeof(double)); //Выделяется память под i-ую строку
  }
  mat->m = m;
  mat->n = n;
  return mat;
}

//Поменять местами строки i и j
void permuteInPlace(struct Matrix* mat, unsigned int i, unsigned int j) {
  /*TODO: Добавить проверки для i и j*/
  double * temp;
  temp = mat->array[i];
  mat->array[i] = mat->array[j];
  mat->array[j] = temp;
}

//Прибавить к строке dst строку src, домноженную на scalar
void addInPlace(struct Matrix* mat, unsigned int src, unsigned int dst, double scalar) {
  /*TODO: Добавить проверки для src, dst и scalar*/
  /*TODO: Реализовать прибавление*/
}

//Домножить строку i на scalar
void scaleInPlace(struct Matrix* mat, unsigned int i, double scalar) {
  /*TODO: Добавить проверки для i и scalar*/
  /*TODO: Реализовать домножение*/
}

//Удалить матрицу, освободить память
void deleteMatrix(struct Matrix* mat) {
  for(int i=0;i<mat->m;i++){
    free(mat->array[i]); //Удаляется i-я строка
  }
  free(mat->array);
  free(mat);
  return;
}

//Служебная функция для чтения матрицы из текстового файла
/*
Файл для единичной матрицы 3x3 будет выглядеть так:
1.0 0.0 0.0
0.0 1.0 0.0
0.0 0.0 1.0
*/

struct Matrix* readMatrixFromFile(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        fprintf(stderr, "Error: Could not open file '%s'\n", filename);
        return NULL;
    }

    // Первый проход: считаем число строк и столбцов
    unsigned int m = 0, n = 0;
    char line[2048];

    while (fgets(line, sizeof(line), file)) {
        if (strlen(line) <= 1) continue;
        m++;
        if (m == 1) {
            char* token = strtok(line, " \t\n");
            while (token) {
                n++;
                token = strtok(NULL, " \t\n");
            }
        }
    }

    if (m == 0 || n == 0) {
        fprintf(stderr, "Error: Empty matrix in file '%s'\n", filename);
        fclose(file);
        return NULL;
    }

    // Вернемся назад для повторного прохода
    rewind(file);

    // Создание матрицы
    struct Matrix* matrix = constructMatrix(m, n);
    if (!matrix) {
        fclose(file);
        return NULL;
    }

    // Второй проход: читаем данные
    for (unsigned int i = 0; i < m; i++) {
        if (!fgets(line, sizeof(line), file)) {
            fprintf(stderr, "Error: File ended prematurely at row %u\n", i);
            deleteMatrix(matrix);
            fclose(file);
            return NULL;
        }
        char* token = strtok(line, " \t\n");
        for (unsigned int j = 0; j < n; j++) {
            if (!token) {
                fprintf(stderr, "Error: Not enough columns in row %u\n", i);
                deleteMatrix(matrix);
                fclose(file);
                return NULL;
            }
            char* endptr;
            matrix->array[i][j] = strtod(token, &endptr);
            if (*endptr != '\0' && *endptr != '\n') {
                fprintf(stderr, "Error: Invalid number format at row %u, col %u\n", i, j);
                deleteMatrix(matrix);
                fclose(file);
                return NULL;
            }
            token = strtok(NULL, " \t\n");
        }
    }

    fclose(file);
    return matrix;
}

//Служебная функция для вывода небольшой матрицы в консоль
void printMatrix(const struct Matrix* mat) {
    if (!mat || !mat->array) {
        printf("(Invalid matrix)\n");
        return;
    }

    for (unsigned int i = 0; i < mat->m; i++) {
        for (unsigned int j = 0; j < mat->n; j++) {
            printf("%10.2f", mat->array[i][j]);
            if (j < mat->n - 1) {
                printf(" ");
            }
        }
        printf("\n");
    }
}

/*TODO: можно добавить дополнительные функции, здесь или выше*/

int main() {
  struct Matrix* mat = readMatrixFromFile("./input.txt");
  printMatrix(mat);
  printf("\n");
  permuteInPlace(mat,0,1);
  printMatrix(mat);
  deleteMatrix(mat);
    /*TODO: Написать демонстрацию работы всех функций*/
  return 0;
}
