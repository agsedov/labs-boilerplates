#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#define HIT_NONE 0
#define HIT_SPHERE1 1
#define HIT_SPHERE2 2
#define HIT_PLANE 3
#define HIT_SUN 4

// simplified version of https://fabiensanglard.net/postcard_pathtracer/formatted_full.html (Andrew Kensler)

float randomVal() { return (float) rand() / RAND_MAX; }

//Класс для работы с вектором
struct Vec {
    float x, y, z;

    Vec(float v = 0) { x = y = z = v; }

    Vec(float a, float b, float c = 0) {
      x = a;
      y = b;
      z = c;
    }

    //Сложение с другим вектором
    Vec operator+(Vec r) { return Vec(x + r.x, y + r.y, z + r.z); }

    //Покоординатное умножение, через него реализовано умножение на скаляр
    Vec operator*(Vec r) { return Vec(x * r.x, y * r.y, z * r.z); }

    //Скалярное умножение на другой вектор
    float operator%(Vec r) { return x * r.x + y * r.y + z * r.z; }

    //Нормирование вектора
    Vec operator!() {
      return *this * (1 / sqrt(*this % *this)
      );
    }
};

// Sample the world.
float WorldDistance(Vec position, int &hitType) {
  float distance = 1e9;
  Vec sphere1Center(-3.,4.,2.);
  float sphere1Radius = 2.;
  Vec sphere2Center(3.,2.,1.);
  float sphere2Radius = 1.;
  float planeDistance = position.z;
  hitType = HIT_NONE;

  if(planeDistance < distance) distance = planeDistance, hitType = HIT_PLANE;

  float sphere1Distance = sqrt((position + sphere1Center*(-1))%(position + sphere1Center*(-1))) - sphere1Radius;
  if (sphere1Distance < distance) distance = sphere1Distance, hitType = HIT_SPHERE1;

  float sphere2Distance = sqrt((position + sphere2Center*(-1))%(position + sphere2Center*(-1))) - sphere2Radius;
  if (sphere2Distance < distance) distance = sphere2Distance, hitType = HIT_SPHERE2;
  //float sun = 5.1 - position.z ; // Everything above 19.9 is light source.
  if (position.z>20.) distance = position.z, hitType = HIT_SUN;

  return distance;
}

// Perform signed sphere marching
// Returns hitType 0, 1, 2, or 3 and update hit position/normal
int RayMarching(Vec origin, Vec direction, Vec &hitPos, Vec &hitNorm) {
  int hitType = HIT_NONE;
  int noHitCount = 0;
  float d; // distance from closest object in world.

  // Signed distance marching
  for (float total_d=0; total_d < 100; total_d += d)
    if ((d = WorldDistance(hitPos = origin + direction * total_d, hitType)) < .01
            || ++noHitCount > 99){
      hitNorm = !Vec(WorldDistance(hitPos + Vec(.01, 0), noHitCount) - d,
                     WorldDistance(hitPos + Vec(0, .01), noHitCount) - d,
                     WorldDistance(hitPos + Vec(0, 0, .01), noHitCount) - d);
      return hitType;
    }
  return 0;
}

Vec Trace(Vec origin, Vec direction) {
  Vec sampledPosition, normal, color, attenuation = 1;
  Vec lightDirection(!Vec(.6, .6, 1)); // Directional light

  for (int bounceCount = 3; bounceCount--;) {
    int hitType = RayMarching(origin, direction, sampledPosition, normal);
    if (hitType == HIT_NONE) break; // No hit. This is over, return color.
    if (hitType == HIT_SPHERE1) { // Specular bounce on a letter. No color acc.
      direction = direction + normal * ( normal % direction * -2);

      color = color + attenuation * Vec(1., .5, .5); //
      //Надо отступить от точки отскока, чтобы не случился второй хит
      origin = sampledPosition + direction * 0.1;

      attenuation = attenuation * 0.7; // Attenuation via distance traveled.
    }
    if (hitType == HIT_SPHERE2) { // Specular bounce on a letter. No color acc.
      direction = direction + normal * ( normal % direction * -2);

      color = color + attenuation * Vec(.5, 1.,.5); //
      //Надо отступить от точки отскока, чтобы не случился второй хит
      origin = sampledPosition + direction * 0.1;

      attenuation = attenuation * 0.7; // Attenuation via distance traveled.
    }
    if (hitType == HIT_PLANE) { // Шахматный паттерн при отскоке от плоскости
      direction = direction + normal * ( normal % direction * -2);
      origin = sampledPosition + direction * 0.1;
      if(abs(fmod(ceil(sampledPosition.x) + ceil(sampledPosition.y), 2.)) < 1.) {
        color = color + attenuation * Vec(1.); //Светлая клетка
      } else {
        color = color + attenuation * Vec(.2); //Тёмная клетка
      }
      attenuation = attenuation * 0.2; // Attenuation via distance traveled.
    }
    if (hitType == HIT_SUN) { //
      color = color + attenuation * Vec(1, 200, 1); break; // Sun Color
    }
  }
  return color;
}

int main() {
//  int w = 960, h = 540, samplesCount = 16;
  int w = 960, h = 540, samplesCount = 6;
  Vec position(10, 4, 4);

  //Вектор направления луча
  Vec goal = !(Vec(-3, 4, 2) + position * -1);
  //Ортогональный ему вектор
  Vec left = !Vec(-goal.y, goal.x, 0) * (1. / w);

  // Векторное произведение: получаем вектор, направленный вверх
  Vec up(goal.y * left.z - goal.z * left.y,
      goal.z * left.x - goal.x * left.z,
      goal.x * left.y - goal.y * left.x);

  //Заголовок Portable Pixmap
  printf("P6 %d %d 255 ", w, h);
  for (int y = h; y--;)
    for (int x = w; x--;) {
      Vec color;
      for (int p = samplesCount; p--;)
        color = color + Trace(position, !(goal + left * (x - w / 2 + randomVal()) + up * (y - h / 2 + randomVal())));

      // Reinhard tone mapping
      color = color * (1. / samplesCount) + 14. / 241;
      Vec o = color + 1;
      color = Vec(color.x / o.x, color.y / o.y, color.z / o.z) * 255;
      printf("%c%c%c", (int) color.x, (int) color.y, (int) color.z);
    }
}
