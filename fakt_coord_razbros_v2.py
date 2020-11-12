"""
программа определяет координаты фактических точек измерений
распределяя их между фактически записанными.
на вход принимает файл gps.txt сохраненный из mapsource в текстовом формате.
"""
from math import sqrt
from operator import itemgetter 

L_PK = 5 #расстояние между пикетами

def points_from_mapsource(src_file_name):
    """ парсинг фактических точек из файла txt из MapSource в список """
    points_file = open(src_file_name, 'r')
    points = []
    for line in points_file:
        point = line.split('\t')
        if point[0] == 'Waypoint':
            coord = point[4].split(' ')
            if len(coord) == 4: # если координаты в формате UTM и в ячейке строка вида "53 T 589054 4963309"
                coord = [coord[2], coord[3]]
            """
            if len(point[1]) == 6: # для имен точек 3 симв профиль, 3 - пикет
                points.append([int(point[1][0:3]), int(point[1][3:6]), coord])
            elif len(point[1]) == 5: # для имен точек 2 симв профиль, 3 - пикет
                points.append([int(point[1][0:2]), int(point[1][2:5]), coord])
            elif len(point[1]) == 7: # для имен точек 2 симв профиль, 3 - пикет
                points.append([int(point[1][0:3]), int(point[1][3:7]), coord])
            """
            # проверка имени точки
            if not list(filter(lambda s: s not in ('1234567890-'), point[1])):
                # and len(point[1].split('-')) == 2:
                # pr, pk = point[1].split('-')
                pr, pk = point[1][:-4], point[1][-4:]
                #points.append([int(pr), (int(pk)*4),coord])
                points.append([int(pr), (int(pk)),coord])                
            else:
                print("ошибка в имени точки ", point[1])
    points_file.close()
    points.sort(key=itemgetter(0,1))
    print("файл %s с точками прочитан" % src_file_name)
    return points

def points_from_x_y_name(src_file_name):
    """ парсинг точех из файла формата ' x; y; name /n ' в список
        в name правые 3 символа профиль левые 4 - пк
        :return: points : [[pr:int, pk:int, coord: [x:float, y:[float]], ...]
    """
    points_file = open('pnts.txt', 'r')
    if points_file: print('файл {} открыт'.format(points_file))
    points = []
    for line in points_file:
        point = line.split(';')
        coord = (float(point[0]), float(point[1]))
        points.append([(int(point[2])//10000), int(point[2][3:7]), coord])
    points_file.close()
    points.sort(key=itemgetter(0,1))
    print("файл %s с точками прочитан" % src_file_name)
    return points

def calc_points(points):
    """
    Рассчитывает коодинаты промежуточных точек.
    points : [[pr:int, pk:int, coord: [x:float, y:[float]], ...]
    return: all_points : [[pr:int, pk:int, coord: [x:float, y:[float]], ...]
    """
    all_points = []
    for i in range(1, len(points)):
        x0, y0 = int(points[i-1][2][0]), int(points[i-1][2][1])
        x1, y1 = int(points[i][2][0]), int(points[i][2][1])
        dist = sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)  # расстояние между точками по координатам
        qnt = (points[i][1] - points[i - 1][1])  # кол-во точек между точками с известными координатами
        dist_pk = qnt * L_PK  # расстояние между точками по номерам пикетов
        if (points[i][0] == points[i-1][0]) and (dist_pk - 40 < dist < dist_pk + 30):
            # 2е условие нужно для пр которые делались кусками с разных сторон
            # и имеют соотвественно нумерацию вразброс.
            # print('i=', i,'point', points[i], 'i-1=', points[i-1])
            step_x = (x1 - x0) / qnt
            step_y = (y1 - y0) / qnt
            for j in range(qnt):
                n = points[i-1][1] + j
                x = x0 + step_x * j
                y = y0 + step_y * j
                all_points.append([points[i][0], n, x, y])
        else:
            all_points.append([points[i-1][0], points[i-1][1], x0, y0])
    all_points.append([points[-1][0], points[-1][1], int(points[-1][2][0]), int(points[-1][2][1])])
    print("точки рассчитаны")
    return all_points

def make_result_file(rslt_file_name, all_points):
    """Записывает точки в файл"""
    all_points_file = open(rslt_file_name, 'w')
    for point in all_points:
        # point_name = "%02d-%03d" % (point[0], point[1])
        # point_name = point[0] * 1000 + point[1]
        point_name = point[0] * 10000 + point[1]
        # point_name2 = '%02d-%04.2f' % (point[0], point[1] / 4)
        # all_points_file.write('%s, %s, %.2f, %.2f\n' % (point_name, point_name2, point[2], point[3]))
        all_points_file.write('%06d, %.2f, %.2f\n' % (point_name, point[2], point[3]))
    all_points_file.close()
    print("и записаны в файл", rslt_file_name)

source_file_name = r'd:\!work\!2020_altay\magn_all.txt'
result_file_name = r'd:\!work\!2020_altay\all_points_lokot_magn.txt'

print('открываем файл')
points = points_from_mapsource(source_file_name)
#points = points_from_x_y_name(source_file_name)
all_points = calc_points(points)
make_result_file(result_file_name,all_points)
