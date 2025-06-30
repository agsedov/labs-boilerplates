#include "raylib.h"
#include <stdlib.h>

/******************
 *  Modified raylib example by Ramon Santamaria (@raysan5) Copyright (c) 2023-2025
 *  Original code is distributed under zlib/libpng license
 *  https://github.com/raysan5/raylib/blob/master/examples/shapes/shapes_splines_drawing.c
 ******************/

//Количество перемещаемых точек
#define POINTS_NUM 5

//Координаты центра графика в оконной системе координат (середина окна 600x600)
#define PLOT_CENTER_X 300.0
#define PLOT_CENTER_Y 300.0

//Шаг графика в пикселях
#define PLOT_GRADE 50.0

//Перевод из оконной системы координат в координаты на графике
Vector2 screenCoordinatesToPlot(Vector2 point) {
  Vector2 a = {(point.x-PLOT_CENTER_X)/PLOT_GRADE, (point.y-PLOT_CENTER_Y)/PLOT_GRADE};
  return a;
}

//Перевод из координат на графике в оконную систему координат
Vector2 plotCoordinatesToScreen(Vector2 point) {
  Vector2 a = {point.x*PLOT_GRADE+PLOT_CENTER_X, point.y*PLOT_GRADE+PLOT_CENTER_Y};
  return a;
}

/*
 * TODO: Добавьте сюда необходимые функции
 */

int main(void)
{
  //Ширина и высота экрана
  const int screenWidth = 600;
  const int screenHeight = 600;

  InitWindow(screenWidth, screenHeight, "Лабораторная работа");

  //Исходное расположение точек
  Vector2 points[POINTS_NUM] = {
    { -4.0f, -2.0f },
    { -3.0f, 2.0f },
    { 1.0f, -4.0f },
    { 2.0f, 1.0f },
    { 4.0f, 3.0f },
  };

  Vector2 centerScreen = {PLOT_CENTER_X,PLOT_CENTER_Y};

  //Какая точка выделена или подсвечена в данный момент (изначально - никакая)
  int selectedPoint = -1;
  int focusedPoint = -1;

  SetTargetFPS(60);

  while (!WindowShouldClose())
  {
    //Подсветка точек и их выделение
    if (selectedPoint == -1)
    {
      focusedPoint = -1;
      for (int i = 0; i < POINTS_NUM; i++)
      {
        if (CheckCollisionPointCircle(GetMousePosition(), plotCoordinatesToScreen(points[i]), 8.0f))
        {
          focusedPoint = i;
          break;
        }
      }
      if (IsMouseButtonPressed(MOUSE_LEFT_BUTTON)) selectedPoint = focusedPoint;
    }

    //Если точка выделена - двигаем её вместе с мышкой
    if (selectedPoint >= 0)
    {
      points[selectedPoint] = screenCoordinatesToPlot(GetMousePosition());
      if (IsMouseButtonReleased(MOUSE_LEFT_BUTTON)) selectedPoint = -1;
    }


    // Рисование
    //----------------------------------------------------------------------------------
    BeginDrawing();

    //Отчистка экрана
    ClearBackground(RAYWHITE);

    /*TODO: Сюда добавить отрисовку графика*/

    //Рисование осей координат
    for(int i = -6; i <= 6; i++) {
      Vector2 gradeX = {i,0.0};
      Vector2 gradeXScreen = plotCoordinatesToScreen(gradeX);
      DrawText(TextFormat("%.0f", gradeX.x), (int)gradeXScreen.x, (int)gradeXScreen.y + 20, 20, GRAY);

      Vector2 gradeY = {0.0,i};
      Vector2 gradeYScreen = plotCoordinatesToScreen(gradeY);
      DrawText(TextFormat("%.0f", gradeY.y), (int)gradeYScreen.x, (int)gradeYScreen.y + 20, 20, GRAY);
    }

    //Рисование точек
    for (int i = 0; i < POINTS_NUM; i++)
    {
      Vector2 screenPoint = plotCoordinatesToScreen(points[i]);
      DrawCircleLinesV(screenPoint, (focusedPoint == i)? 12.0f : 8.0f, (focusedPoint == i)? BLUE: DARKBLUE);
      DrawText(TextFormat("[%.2f, %.2f]", points[i].x, points[i].y), (int)screenPoint.x, (int)screenPoint.y + 20, 20, BLACK);
    }
    EndDrawing();
    //----------------------------------------------------------------------------------
  }

  //--------------------------------------------------------------------------------------
  CloseWindow();        // Закрытие окна и контекста OpenGL
  //--------------------------------------------------------------------------------------

  return 0;
}
