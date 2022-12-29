import tkinter as tk
from tkinter.ttk import Combobox, Frame, Scale, Style
from tkinter import StringVar, IntVar, DoubleVar

from testsFunctions import Spherical, Rastrigin, Ackley, Beale, Booth, Bukin, Three_humpCamel, Holder_table, McCormick, Shaffer

from main import Evolution

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Параметры передающиеся в алгоритм светлячков для запуска алгоритма
class Settings():
    def __init__(self):
        self.testFunction = Spherical()
        self.populationSize = 25
        self.iteration = 100
        self.influence = 30
        self.lowerBound = 70
        self.jitter = 0.3

# Инцииация графической части
class InitGuiVar():
    def __init__(self, settings):
        self.settings = settings
        self.initGuiVar()

    # Инициация динамических переменных для библиотеки Tkinter
    def initGuiVar(self):
        self.varSelectTestFunction = StringVar()
        self.varSelectTestFunction.trace_add("write", self.changeTestFunction)
        
        self.varPopulationSize = IntVar()
        self.varPopulationSize.set(self.settings.populationSize)
        self.varPopulationSize.trace_add("write", self.changePopulationSize)

        self.varIteration = IntVar()
        self.varIteration.set(self.settings.iteration)
        self.varIteration.trace_add("write", self.changeIteration)

        self.varSliderEra = StringVar()
        self.varSliderEra.set("Поколение: ")

        self.varInfluence = DoubleVar()
        self.varInfluence.set(30.0)

        self.varLowerBound = DoubleVar()
        self.varLowerBound.set(70.0)

        self.varJitter = DoubleVar()
        self.varJitter.set(0.3)

    # Обработка тестовых функций
    def changeTestFunction(self, v, i, m):
        value = self.varSelectTestFunction.get()
        print(value)

        if value == "Сферическая":
            self.settings.testFunction = Spherical()
            print("Выбрана функция сферическая")
        if value == "Растригина":
            self.settings.testFunction = Rastrigin()
            print("Выбрана функция растригина")
        if value == "Экли":
            self.settings.testFunction = Ackley()
        if value == "Била":
            self.settings.testFunction = Beale()
        if value == "Стенда":
            self.settings.testFunction = Booth()
        if value == "Букина":
            self.settings.testFunction = Bukin()
        if value == "Три горба":
            self.settings.testFunction = Three_humpCamel()
        if value == "Таблица Холдера":
            self.settings.testFunction = Holder_table()
        if value == "Кормика":
            self.settings.testFunction = McCormick()
        if value == "Шафера":
            self.settings.testFunction = Shaffer()
        
        self.updateEvolution()
        try:
            drawStartArea()
        except NameError:
            pass

    # Отслеживание изменения популяции в GUI и изменения настроек
    def changePopulationSize(self, v, i, m):
        self.settings.populationSize = self.varPopulationSize.get()
        print(self.settings.populationSize)
        self.updateEvolution()

    # Отслеживание изменения итераций (эпох) в GUI и изменения настроек
    def changeIteration(self, v, i, m):
        self.settings.iteration = self.varIteration.get()
        print(self.settings.iteration)
        self.updateEvolution()

    # Переназначает настройки объекту эволюции
    def updateEvolution(self):
        global e
        e = Evolution(ss)


# Создание главного окна, настроек и объекта эволюции
window = tk.Tk()
ss = Settings()
e = Evolution(ss)
s = InitGuiVar(ss)

# Настраиваем стилистику главного окна
window.style = Style()
#window.style.theme_use("alt")
window.option_add( "*font", "clearlyu 12" )
window.title("Лабораторная работа Сиренко В. Н. ИИС-Tg11 2022")
window.geometry('1010x850')


titleFrame = Frame(window)
canvasFrame = Frame(window)
frame = Frame(titleFrame)

# Выбор тестовой функции
label = tk.Label(frame, text="Тестовая функция: ")
label.grid(column=0, row=0)


combo1 = Combobox(frame, textvariable=s.varSelectTestFunction)
combo1['values'] = ["Сферическая", "Растригина", "Экли", "Била", "Стенда", "Букина", "Три горба", "Таблица Холдера", "Кормика", "Шафера"]
combo1.current(0)
combo1.grid(column=1, row=0)

# Размер популяции
label2 = tk.Label(frame, text="Количество светлячков: ")
label2.grid(column=3, row=0, padx=5)

ePopulationSize = tk.Entry(frame, width=30, textvariable=s.varPopulationSize)
ePopulationSize.grid(column=4, row=0)

# Итераций
label3 = tk.Label(frame, text="Поколение: ")
label3.grid(column=3, row=1, padx=5)

eIteration = tk.Entry(frame, width=30, textvariable=s.varIteration)
eIteration.grid(column=4, row=1)

mutationFrame = Frame(titleFrame)
label5 = tk.Label(mutationFrame, textvariable=s.varSliderEra)
label5.grid(column=2, row=0, pady=5)

# Влияние
lInfluence = tk.Label(mutationFrame, text="Фактор влияния:")
lInfluence.grid(column=3, row=0, pady=5)

eInfluence = tk.Entry(mutationFrame, width=30, textvariable=s.varInfluence)
eInfluence.grid(column=4, row=0, pady=5)

# Нижняя граница
lLowerBound = tk.Label(mutationFrame, text="Нижняя граница:")
lLowerBound.grid(column=3, row=1, pady=5)

eLowerBound = tk.Entry(mutationFrame, width=30, textvariable=s.varLowerBound)
eLowerBound.grid(column=4, row=1, pady=5)

# Джиттер
lJitter = tk.Label(mutationFrame, text="Джиттер:")
lJitter.grid(column=3, row=2, pady=5)

eJitter = tk.Entry(mutationFrame, width=30, textvariable=s.varJitter)
eJitter.grid(column=4, row=2, pady=5)


frame.grid(column=0, row=0, pady=5)


##### код эволюции
# Запускает алгоритм светлячков
def runEvolution():
    global e, ss
    print("Старт эволюции!")
    ss.influence = s.varInfluence.get()
    ss.lowerBound = s.varLowerBound.get()
    ss.jitter = s.varJitter.get()

    e = Evolution(ss)
    e.run()

# Отображает стартовую 3D представления фитнесс функции выбранной
canvas = None
def drawStartArea():
    global canvas
    if canvas:
        canvas.get_tk_widget().pack_forget()
    # canvas = FigureCanvasTkAgg(e.drawHromoByStep(), canvasFrame)
    canvas = FigureCanvasTkAgg(e.drawInitArea(), canvasFrame)
    canvas.get_tk_widget().pack()

# Обновляет вид графика при перемещении слайдера, служит для отображения выбранного шага эпохи
def updateSlider(arg):
    #print(arg)
    step = int((ss.iteration / 100)  * float(arg))
    #print(f"Slider! {step}")
    s.varSliderEra.set("Поколение: "+str(step))
    global canvas
    if canvas:
        canvas.get_tk_widget().pack_forget()
    canvas = FigureCanvasTkAgg(e.drawGlowwormsByStep(
        step
    ), canvasFrame)
    canvas.get_tk_widget().pack()
# Размещаем фреймы в фреймы для построения GUI
# Кнопка запуска эволюции
btnStartEvolution = tk.Button(titleFrame,
                              text="Запустить светлячков",
                              command=runEvolution)
btnStartEvolution.grid(column=1, row=0, padx=20)

frameSlider=Frame(titleFrame)
slider=Scale(frameSlider, from_=0, to=100, orient='horizontal', length = 980,
             command=updateSlider)
slider.grid(column=0, row=0)
lSlider=tk.Label(frameSlider, text="0..100")

mutationFrame.grid(column=0, row=1, sticky=tk.W+tk.E, columnspan=3)
frameSlider.grid(column=0, row=2, sticky=tk.W+tk.E, columnspan=3)

titleFrame.grid(column=0, row=0)
canvasFrame.grid(column=0, row=1)

drawStartArea()
# Бесконечный цикл
window.mainloop()