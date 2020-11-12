"""
Программа получает на вход таблицу координат точек начала и конца профилей формата 
НомерПР, Хнач, Yнач, Xкон, Yкон
и заполняет профиля точами через заданный интервал
на выходе таблица точек с координатами. Название точки формата НомерПР-НомерТочки
"""
import math


def calc_point(pk_number, pr, pr_len, POINT_STEP, result_file):
    """формир-ся имя точки, рассчитываются ее координаты и записываются в файл"""
    point_name = "%03d-%04d" % (pr['pr'], pk_number)
    seg_len = pk_number * POINT_STEP
    x_point = int(pr['xst'] + (((pr['xend'] - pr['xst']) / pr_len) * seg_len))
    y_point = int(pr['yst'] + (((pr['yend'] - pr['yst']) / pr_len) * seg_len))
    result_file.write('%s, %d, %d\n' % (point_name, x_point, y_point))


POINT_STEP = 5  # шаг между точками
POINT_FACTOR = 1 # частота точек в конечной таблице(например для каждой второй POINT_FACTOR=2)
coord_table = open('coord_koncov.csv')
source_ponit_db = []
coord_table.readline()
for line in coord_table:
    sep_line = line.split(';')
    source_ponit_db.append({'pr': int(sep_line[0]),
                            'xst': float(sep_line[1]),
                            'yst': float(sep_line[2]),
                            'xend': float(sep_line[3]),
                            'yend': float(sep_line[4])})
pr_point_db = []
result_file = open('point_coord.txt', 'w')
result_file.write('Name, X, Y\n')
for pr in source_ponit_db:
    pr_len = math.sqrt((pr['xend'] - pr['xst']) ** 2 + (pr['yend'] - pr['yst']) ** 2)
    pk_amount = int((pr_len + 5) // POINT_STEP)  # к длине профиля добавляется 5м. если точка измер-я нах-ся в пределах 5м за контуром площади мы его делаем
    print('pr_number=%d, pr_len=%d, pk_amount=%d' % (pr['pr'], pr_len, pk_amount))
    for i, pk_number in enumerate(range(0, pk_amount + 1, POINT_FACTOR)):
        calc_point(pk_number, pr, pr_len, POINT_STEP, result_file)
    if pk_amount % POINT_FACTOR:  # условие нужно для записи последнего пикета если кол-во пикетов не кратно POINT_FACTOR.
        calc_point(pk_amount, pr, pr_len, POINT_STEP, result_file)
result_file.close()
