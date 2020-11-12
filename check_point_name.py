"""
 скрипт ищет ошибки в именах фактических точек gps сравнивая их с проектными.
 если точка имеет имя которого нет у проектных точек или отклонение больше 10м
 то эти точки записываются в файл err_points.txt
на вход нужно 2 файла
1: файл с проектными точками формат: имя, х, у  имя='%03d-%03d' н-р(006-004)
2: файл с реальными точками сохраненный из mapSource в формате txt
"""
import math

points_file = open('proj_point_all.txt', 'r')
prj_points = {}
points_file.readline()
# загрузка проектных точек в словарь
for i, line in enumerate(points_file):
    point = line.split(',')
    pr_pk = point[0].split('-')
    point_name = pr_pk[0] + pr_pk[1]
    prj_points[point_name] = [int(point[1]), int(point[2][0:-1])]
points_file.close()

# парсинг фактических точек из файла txt из MapSource в список
points_file = open('gps.txt', 'r')
real_points = []
for i, line in enumerate(points_file):
    point = line.split('\t')
    if point[0] == 'Waypoint':
        coord = point[4].split(' ')
        if len(coord) == 4: #если координаты в формате UTM и в ячейке строка вида "53 T 589054 4963309"
            coord = [coord[2], coord[3]]        
        real_points.append(["%06d" % int(point[1]), coord])
points_file.close()

err_points = open('err_points.txt', 'w')
# проверка точек на корректность имени и положения(радиус 10м от проектной)
for point in real_points:
    if point[0] in prj_points:
        x_prj, y_prj = prj_points[point[0]]
        x_real, y_real = int(point[1][0]), int(point[1][1])
        dist = math.sqrt((x_prj - x_real) ** 2 + (y_prj - y_real) ** 2)
        if dist < 10:
            continue
    err_points.write('E%s, %d, %d\n' % (point[0], x_real, y_real))
err_points.close()
