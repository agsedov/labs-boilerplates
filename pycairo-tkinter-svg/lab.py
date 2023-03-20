import sys
import math
from tkinter import Tk, Label
from PIL import Image, ImageTk
from cairo import ImageSurface, Context, FORMAT_ARGB32

# Установите зависимости! Команда:
# pip3 install pillow pycairo tk

# Запустить с параметром 1:
# python3 lab.py 1

class WindowWithLabel(Tk):
    """Класс для окна"""
    def redraw(self):
        '''
        Рисование при помощи cairo Context
        Вызывается при инициализации и при движении мышки
        '''
        self.context = Context(self.surface)

        ### ИЗМЕНИТЕ КОД РИСОВАНИЯ НИЖЕ и не стесняйтесь выносить его в отдельные функции

        # Закрашиваем фон
        self.context.set_source_rgba(1, 0, 0, 1)
        self.context.rectangle(0, 0, self.w, self.h)
        self.context.fill()

        # Закрашиваем круг под мышкой (дугу от 0 до 2pi)
        self.context.set_source_rgba(0, 0, 1, 0.5)
        self.context.arc(self.mouse_x, self.mouse_y, 10, 0 ,2*math.pi)
        self.context.fill()

        ### ИЗМЕНИТЕ КОД РИСОВАНИЯ ВЫШЕ

        #Далее нарисованное помещается в объект Label на окне
        self._image_ref = ImageTk.PhotoImage(Image.frombuffer("RGBA", (self.w, self.h), self.surface.get_data().tobytes(), "raw", "BGRA", 0, 1))
        self.label.image = self._image_ref
        self.label.configure(image = self._image_ref)
        self.label.pack(expand=True, fill="both")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('Передан параметр ', PARAMETER_1)
        self.mouse_x = 0
        self.mouse_y = 0
        self.w, self.h = 800, 600

        self.geometry("{}x{}".format(self.w, self.h))

        self.surface = ImageSurface(FORMAT_ARGB32, self.w, self.h)

        self.label = Label(self)
        self.label.bind('<Motion>', self.motion)
        self.redraw()
        self.mainloop()

    def motion(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y
        self.redraw()


if len(sys.argv) < 2:
    print("Передайте хотя бы один параметр через командную строку. Например, \npython3 lab.py 8")
    sys.exit()



PARAMETER_1 = sys.argv[1]

## ДОБАВЬТЕ ДОПОЛНИТЕЛЬНЫЕ ПРОВЕРКИ ДЛЯ ПЕРЕДАННОГО ПАРАМЕТРА ЗДЕСЬ

if __name__ == "__main__":
    WindowWithLabel()
