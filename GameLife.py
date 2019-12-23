# Импортируем библиотку Pygame и Random и инициализируем Pygame
import pygame as pg
import random as rand
from pygame import mixer
pg.init()
mixer.init()
# Создаем переменную Win, которая отвечает за отображения окна игры
win = pg.display.set_mode((1208, 816))
# Задаем имя для нашего игрового окна
pg.display.set_caption('The Life')
# Задаем количетсво игровых клеток
matrix_h = 150
matrix_w = 150
# Создаем переменную ответственную за отрисовку игры
run = True
# Загружаем фоновое изображения игрового стола
fon = pg.image.load('NS_life.jpg')
# indent - расчитывает отступ от начала окна
indent = (600 - (matrix_h * 4))/2
# Константы для определения игрока
player_1 = 1
winout = 0
player_2 = 2
# Переменные, которые ведут подсчет поколения для каждого поля
generation_counter1 = 0
generation1 = 0
generation_counter2 = 0
generation2 = 0
runflag = False
# Счетчик для очков
points1 = 0
points2 = 0
# Путь к коду игроков
algoritm_p1 = 'text1.txt'
algoritm_p2 = 'text2.txt'
# Константы на тик
input_text = '|'
input_tick = 15
# Загрузка звука
button_sound = pg.mixer.Sound('elevator.wav')
# Требование ввода
need_input = False
# coef определяет вероятность появления единиц в рандомном массиве по формуле P=1/(1+coef)
coef = 9

'''Создаем класс кнопок, задаем и присваиваем основные параметры в функции __init__: длина height,
ширина widht, дефолтный цвет кнопки inactive_color и цвет кнопки при нажатии - active_color
создаем в классе функцию отрисовки кнопки и ее параметры: координаты в окне x,y, текст кнопки -
message, и задаем функцию для кнопки, функции конопок прописываются отдельно.

'''
class Button:
    def __init__(self, width, height):
        # задаем размер и цвекта кнопок при навелении и в неактивном состоянии
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 58)
        self.active_color = (23, 204, 58)

    def draw(self, x, y, message, action=None):
        # две переменные получают позицию курсора и информацию о нажатии
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        '''если позиция курсора равна точке из множества точек ограниченного кнопкой,
        иначе-рисует ее другим цветом(неактивным)
        то выполняется отрисовка прямоугольника для кнопки с нужным цветом, 
        а при нажатии на нее выполняет действия и проигрывает звук нажатия'''
        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                #активная кнопка окрашивается и отрисовывается в окне
                pg.draw.rect(win, self.active_color, (x, y, self.width, self.height))
                #при нажатии кнопки проигрывается звук из файла и задержка в 3 мс
                if click[0] == 1 and action is not None:
                    button_sound.play()

                    pg.time.delay(300)
                #срабатывает функция кнопки
                if click[0] == 1 and action is not None:

                    action()
            else:
                #кнопка окрашена как неактивная и отрисовывается в окне
                pg.draw.rect(win, self.inactive_color, (x, y, self.width, self.height))
        else:
            pg.draw.rect(win, self.inactive_color, (x, y, self.width, self.height))
        #параметры текста на кнопке
        print_text(message, x + 10, y + 10)
#задаем стандартный размер кнопки
button = Button(100, 50)


# фунция окна ввода для игрока, с возможностью импортирования алгоритмов в игру
def get_input():
    global input_text, need_input, input_tick
    input_rect = pg.Rect(10, 700, 500, 60)
    pg.draw.rect(win, (168, 169, 170), input_rect)
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    if input_rect.collidepoint(mouse[0], mouse[1]) and click[0]:
        need_input = True
    if need_input:
        for event in pg.event.get():
            if need_input and event.type == pg.KEYDOWN:
                input_text = input_text.replace('|', '')
                input_tick = 15
                if event.key == pg.K_RETURN:
                    press_1()
                    need_input = False
                elif event.key == pg.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 27:
                        input_text += event.unicode
                input_text += '|'
            input_tick -= 1
    if len(input_text):
         print_text(message=input_text, x=input_rect.x + 10, y=input_rect.y + 10, font_size=39)
    input_tick -= 1
    if input_tick == 0:
        input_text = input_text[:-1]
    if input_tick == -15:
        input_text += '|'
        input_tick = 15


# отрисовка тексто по входному сообщению и координатам
def print_text(message, x, y, font_color = (0, 0, 0), font_type = '1488.otf', font_size = 30 ):
    global input_text, need_input
    font_type = pg.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    win.blit(text, (x, y))


'''вывод (добавляет текущще количество активных клеток в матрице и добавляет их к текущему счету,
затем отправляет на отрисовку'''
def output_text_generation(counter_mass):
    global input_text
    points = counter(counter_mass, score_p1)
    print_text(message=str(points), x=10, y=600, font_size=80)

#выводит кол-во пикселей первого алгоритма
def output_text1p(counter_mass):
    global score_p1, generation1, generation_counter1, points1
    if generation_counter1 > generation1:
        points1 = counter(counter_mass, score_p1)
        score_p1 = points1
        generation1 = generation1 + 1
    print_text(message=str(points1), x=10, y=600, font_size=80)

#выводит кол-во пикселей второго алгоритма
def output_text2p(counter_mass):
    global score_p2, generation2, generation_counter2, points2
    if generation_counter2 > generation2:
        points2 = counter(counter_mass, score_p2)
        score_p2 = points2
        generation2 = generation2 + 1
    print_text(message=str(points2), x=618, y=600, font_size=80)


''' 
это функция добавления случайных нулей и единиц в массив с определенной вероятностью,
которая регулируется coef - определяет вероятность появления единиц в рандомном массиве
по формуле P=1/(1+coef), где P - коэффициент появления единиц.
создается копия входного массива, осуществляется проход по всем элементам 
подмассивов в массиве, создается массив vyborka в котором регулируется вероятность
и в зависимости от частоты встречаемости элемента в vyborke регулируется
частота встречаемости конкретного элемента в элементах подмассива входного массива 
итоговый массив выводится
'''


def rand_mass(m):
    new_mass = m
    a = -1
    for p_m in m:
        a += 1
        i = -1
        for elem in p_m:
            i += 1
            vyborka = [1] + coef * [0]
            new_mass[a][i] = rand.choice(vyborka)
    return new_mass
# создается рандомный массив и присваивается двум игрокам, описывает старт игры
matrix = [[0] * matrix_h for i in range(matrix_w)]
new_matrix_p1 = rand_mass(matrix)
new_matrix_p2 = new_matrix_p1
score_p1 = 0
score_p2 = 0


def otrisovka(our_mass, player):
    this_mass = our_mass
    a = -1
    for p_m in our_mass:
        a += 1
        i = -1
        for elem in p_m:
            if player == 1:
                if this_mass[a][i] == 1:
                    g_rect = pg.Rect(indent + a * 4, indent + i * 4, 4, 4)
                    pg.draw.rect(win, (0, 204, 34), g_rect)
            else:
                if player == 2:
                    if this_mass[a][i] == 1:
                        g_rect = pg.Rect(608 + indent + a * 4, indent + i * 4, 4, 4)
                        pg.draw.rect(win, (0, 204, 34), g_rect)
            i += 1


#функция первой кнопки, выполняет шаг в игре жизнь для двух алгоритмов

def press_x1():
    global new_matrix_p1, new_matrix_p2, generation_counter1, generation_counter2
    generation_counter1 = generation_counter1 + 1
    generation_counter2 = generation_counter2 + 1
    new_matrix_p1 = ns_life(new_matrix_p1, matrix_h, matrix_h)
    new_matrix_p2 = ns_life(new_matrix_p2, matrix_h, matrix_h)

#функция первой кнопки, выполняет 20 шагов в игре жизнь для двух алгоритмов
def press_x20():
    global new_matrix_p1, new_matrix_p2, generation_counter1, generation_counter2
    x20 = 20
    while x20 > 0:
        print(x20)
        x20 -= 1
        generation_counter1 = generation_counter1 + 1
        generation_counter2 = generation_counter2 + 1
        new_matrix_p1 = ns_life(new_matrix_p1, matrix_h, matrix_h)
        new_matrix_p2 = ns_life(new_matrix_p2, matrix_h, matrix_h)

#загружает алгоритм первого плеера
def press_p1():
    global algoritm_p1
    algoritm_p1 = input_text.replace('|', '')

#загружает алгоритм второго плеера
def pressp2():
    global algoritm_p2
    algoritm_p2 = input_text.replace('|', '')


def press_reset():
    # конпка сброса матриц до нового рандомного состояния и сброс всех счетчиков
    global new_matrix_p1, new_matrix_p2,points1, points2, matrix, score_p1, score_p2, generation_counter1, generation1, generation2, generation_counter2, winout
    score_p1 = 0
    score_p2 = 0
    points1 = 0
    points2 = 0
    new_matrix_p1 = rand_mass(matrix)
    new_matrix_p2 = new_matrix_p1
    generation_counter1 = 0
    generation1 = 0
    generation_counter2 = 0
    generation2 = 0
    winout = '0'


def press_winner():
    global points1, points2, winout
    winout=0
    if points1>points2:
        winout = '(1) '
        winout += str( points1 - points2)
    elif points1<points2:
        winout = '(2) '
        winout += str(points2 - points1)
    else :
        winout = '(draw) '
        winout += str(points2)


def press_start():
    global new_matrix_p1, new_matrix_p2, generation_counter1, generation_counter2, runflag
    runflag = True

def press_stop():
    global runflag
    runflag = False


''' счетчик активных клеток на матрице. Входящие данные:двумерный массив - mass и счетчик очков
 - score, все единицы из каждого подмассива, при проходе, суммируются и результат возвращается'''
def counter(mass, score):
    for i in mass:
        for a in i:
            if a == 1:
                score += 1
    return score


'''входные данные: массив - m, в котором необходимо сделать шаг в игре жизнь;
ширина массива - m_w(кол-во массивов в изначальном массиве);
длина массива - m_h(кол-во элементов одного подмассива из массивов в изначальном массиве)
создаем копию массива и вводим счетчики: очков - point_score и столбов со строками - a,i.
смотрим на элементы в строчках, за каждый проход циклов прибавляем по единице к 
соответствующим параметрам изначального массива(длинна,ширина)
создаем вспомогательный массив - new_m, тех же параметров, но забитый нулями, для последующего 
отображения новых пикселей.
осуществляем проверку пикселей следующим образом: закрепляем один пиксель
и смотрим на 8 его соседей, в соответсвии с правилами игры жизнь либо добавляем,
либо удаляем, либо сохраняем пиксель.
сами пиксели порождены циклическими группами, факторизуя координаты по высоте и 
ширине изначального массива,соответствено, получаем нужные циклические группы.
цель такого подхода в том, что в таком случае пиксель не ограничен в своем 
движении и может выходить как бы за пределы поля, а появляться в другой стороне
согласно правилам циклической группы.
после добавлений/удалений/сохранений закрепленных пикселей переносим их в массив 
забитый нулями и возвращаем итоговый массив.
'''


def ns_life(m, m_h, m_w):
    m_dublikate = m
    new_m = [[0] * m_h for i in range(m_w)]
    point_score = 0
    a = -1
    for stolb in m:
        a += 1
        i = -1
        for stroka in stolb:
            i += 1
            if m_dublikate[(a + 1) % m_w][(i + 1) % m_h] == 1:
                point_score += 1
            if m_dublikate[(a - 1) % m_w][(i + 1) % m_h] == 1:
                point_score += 1
            if m_dublikate[(a + 1) % m_w][(i - 1) % m_h] == 1:
                point_score += 1
            if m_dublikate[(a + 1) % m_w][(i) % m_h] == 1:
                point_score += 1
            if m_dublikate[(a) % m_w][(i + 1) % m_h] == 1:
                point_score += 1
            if m_dublikate[(a - 1) % m_w][(i) % m_h] == 1:
                point_score += 1
            if m_dublikate[(a) % m_w][(i - 1) % m_h] == 1:
                point_score += 1
            if m_dublikate[(a - 1) % m_w][(i - 1) % m_h] == 1:
                point_score += 1
            if point_score == 3:
                new_m[a][i] = 1
            if ((point_score < 2) or (point_score > 3)):
                new_m[a][i] = 0
            if point_score == 2:
                new_m[a][i] = m_dublikate[a][i]
            point_score = 0
    return new_m


def draw_fon():
    global new_matrix_p1, new_matrix_p2
    rect1 = pg.Rect(0, 0, 1208, 600)
    rect_pp1 = pg.Rect(indent, indent, matrix_h * 4, matrix_h * 4)
    rect_pp2 = pg.Rect(indent + 608, indent, matrix_h * 4, matrix_h * 4)
    rect_bord_mid = pg.Rect(600, 0, 8, 600)
    pg.draw.rect(win, (135, 132, 106), rect1)
    pg.draw.rect(win, (0, 0, 0), rect_pp1)
    pg.draw.rect(win, (0, 0, 0), rect_pp2)
    pg.draw.rect(win, (255, 255, 255), rect_bord_mid)
    if generation_counter1 > 0:
        f1 = (open(algoritm_p1, 'r', encoding='utf-8'))
        exec(f1.read())
        f2 = (open(algoritm_p2, 'r', encoding='utf-8'))
        exec(f2.read())
    output_text1p(new_matrix_p1)
    output_text2p(new_matrix_p2)
    otrisovka(new_matrix_p1, player_1)
    otrisovka(new_matrix_p2, player_2)
    print_text(str(generation_counter1), x=1100, y=700, font_size=80)
    print_text(message=str(winout), x=830, y=630, font_size=50)



def draw_window():
    win.blit(fon, (0, 0))
    button.draw(690, 710, 'x_1', action=press_x1)
    button.draw(550, 710, 'x_20', action=press_x20)
    button.draw(10, 770, 'player 1', action=press_p1)
    button.draw(210, 770, 'player 2', action=press_p2)
    button.draw(830, 710, 'reset', action=press_reset)
    button.draw(970, 710, 'winner', action=press_winner)
    button.draw(550, 770, 'start', action=press_start)
    button.draw(690, 770, 'stop', action=press_stop)

#проверяет неймтапл
if __name__ == "__main__":
    while run:
    # Отрисовываем окно
        draw_window()
        draw_fon()
    # generation(generation_counter)
        get_input()
        pg.display.update()
    # создаем массив событий на выход
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False