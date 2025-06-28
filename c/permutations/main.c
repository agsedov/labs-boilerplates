#include <stdio.h>
#include <stdlib.h>

/*
 * Важно:
 *
 *  1. Permutation использует нумерацию с нуля внутри, но при взаимодействии с пользователем должна
 *  выводиться нумерация с единицы, аналогично - везде в аргументах функций
 *  2. next() примененный к подстановке n! раз должен давать исходную подстановку
 * */

//Максимальная длина подстановки
#define MAX_LENGTH 80

struct Permutation {
  unsigned char* array; //Куда переходят элементы. Нумерация с 0. Например, для единичной подстановки из трёх элементов: [0,1,2]
  unsigned char n; //Количество элементов
};

//Создаёт ЕДИНИЧНУЮ подстановку из n элементов
struct Permutation* constructPermutation (unsigned char n) {
  /* TODO:Добавить проверку 0<n<MAX_LENGTH */
  struct Permutation *p = malloc(sizeof(struct Permutation)); //Выделяется память под структуру
  p->array = malloc(sizeof(unsigned char)*n); //Выделяется память под массив
  /* TODO:Добавить заполнение массива и структуры */
  return p;
}

//Вычислить значение подстановки
//Возвращает 0, если i не принадлежит области значений
unsigned char invoke(struct Permutation* p, unsigned char i) {
  if((i > p->n) || (i<1)){
    return 0;
  }
  return p->array[i-1]+1;
}

// Композиция двух подстановок
// Использовать соглашение о порядке:  (l*r)(x) = l(r(x))
struct Permutation* composition (struct Permutation* l, struct Permutation* r) {
  /* TODO: Добавить проверку возможности произведения */
  struct Permutation* result = constructPermutation(l->n);
  /* TODO: Заполнить result->array */
  return result;
}

// Проверка того, что result->array заполнен правильно (не содержит дубликатов и пропусков)
int checkIfValid(struct Permutation* p) {
  /* TODO: строчку ниже можно редактировать */
  return 1;
}

//Вывести подстановку
//Для вывода использовать нумерацию с единицы
void printPermutation (struct Permutation* p) {
  /*TODO: Добавить вывод*/
  return;
}

//Вывести подстановку как набор циклов.
//Для вывода использовать нумерацию с единицы
//Например, [2,3,1,5,4] выводится как (3,1,2),(5,4)
void printPermutationAsCycles (struct Permutation* p) {
  /*TODO: Добавить вывод*/
  return;
}

//Создаёт транспозицию
//transposition(3,1,2) -> [1,0,2]
struct Permutation* transposition (unsigned char n, unsigned char a, unsigned char b) {
  struct Permutation* result = constructPermutation(n);
  /*TODO: Модифицировать result*/
  return result;
}

//Инверсия подстановки
struct Permutation* invert (struct Permutation* p) {
  struct Permutation* result = constructPermutation(p->n);
  /* TODO: Заполнить result */
  return result;
}

//Эта функция изменяет подстановку p!
//
//На выбор использовать алгоритм Джонсона — Троттера или алгоритм Хипа
void next (struct Permutation* p) {
  /*TODO: Реализация */
  return;
}

//Удалить подстановку, освободить память
void deletePermutation(struct Permutation* p) {
  free(p->array);
  free(p);
  return;
}

/*TODO: можно Добавить дополнительные функции, здесь или выше*/

int main() {
    /*TODO: Написать демонстрацию работы всех функций*/
  return 0;
}
