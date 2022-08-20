import math

def cross_product(a, b):
    return a[0]*b[1]-a[1]*b[0]

def distance(a, b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def polygon_area(polygon):
    if len(polygon) < 3:
        return 0.0
    area = cross_product(polygon[-1], polygon[0])/2
    for i in range(1, len(polygon), 1):
        area += cross_product(polygon[i-1], polygon[i])/2
    return abs(area)

def vect(a, b):
    #a is the end, b is the begining of the vector
    return (a[0]-b[0], a[1]-b[1])

def sign(x):
    return bool(x > 0)

def check_if_segments_intersect(beg_a, end_a, beg_b, end_b):
    #points beg, end denote beginin and end of a segment
    if (sign(cross_product(vect(end_a, beg_a), vect(beg_b, beg_a))) != sign(cross_product(vect(end_a, beg_a), vect(end_b, beg_a)))) and (sign(cross_product(vect(end_b, beg_b), vect(beg_a, beg_b))) != sign(cross_product(vect(end_b, beg_b), vect(end_a, beg_b)))):
        return 1
    else:
        return 0

def point_in_polygon(point, polygon):
    max_y = polygon[0][1]
    for i in polygon:
        max_y = max(max_y, i[1])
    max_y += 1
    pocet_priesecnikov = check_if_segments_intersect(polygon[0], polygon[-1], point, [point[0]+1, max_y])
    for i in range(1, len(polygon), 1):
        pocet_priesecnikov += check_if_segments_intersect(polygon[i-1], polygon[i], point, [point[0]+1, max_y])
    return bool(pocet_priesecnikov % 2)

def DFS(v, result, sin_poly, mlt_poly, vteper, navs):
    if navs[v[0]][v[1]]:
        return None
    navs[v[0]][v[1]] = 1
    sur = (0,0)
    if v[0] == 0:
        sur = sin_poly[v[1]]
    else:
        sur = mlt_poly[v[0]-1][v[1]]
    result.append(sur)
    if vteper[v[0]][v[1]] != None:
        for i in vteper[v[0]][v[1]]:
            DFS(i, result, sin_poly, mlt_poly, vteper, navs)
            if result[-1] != sur:
                result.append(sur)
    if v[0] == 0:
        if v[1]+1 == len(sin_poly):
            result.append(sin_poly[0])
        DFS((v[0],(v[1]+1)%len(sin_poly)), result, sin_poly, mlt_poly, vteper, navs)
    else:
        if v[1]+1 == len(mlt_poly[v[0]-1]):
            result.append(mlt_poly[v[0]-1][0])
        DFS((v[0],(v[1]+1)%len(mlt_poly[v[0]-1])), result, sin_poly, mlt_poly, vteper, navs)
    
def simplify(polygon, holes):
    #returns simple polygon with polygons from holes as holes
    edges = [(polygon[i], polygon[(i+1)%len(polygon)]) for i in range(len(polygon))]
    points = [(polygon[i],0,i) for i in range(len(polygon))]
    for i in range(len(holes)):
        for j in range(len(holes[i])):
            points.append((holes[i][j],i+1, j))
            edges.append((holes[i][j],holes[i][(j+1)%len(holes[i])]))
    nasledovne_body = [[] for i in range(len(points))]
    visited = [None]*(len(holes)+1)
    visited[0] = 1
    for i in range(len(points)):
        if visited[points[i][1]] == 1:
            continue
        visited[points[i][1]] = 1
        for j in range(len(points)):
            if points[j][1] == points[i][1]:
                continue
            nepretina_sa = 1
            for k in edges:
                if k[0] == points[i][0] or k[0] == points[j][0] or k[1] == points[i][0] or k[1] == points[j][0]:
                    continue
                if check_if_segments_intersect(points[i][0], points[j][0], k[0], k[1]):
                    nepretina_sa = 0
                    break
            if nepretina_sa:
                nasledovne_body[i].append(j)
                nasledovne_body[j].append(i)
                break
    vsun = [None]*(len(holes)+1)
    uz_prejdene = [None]*(len(holes)+1)
    vsun[0] = [None]*len(polygon)
    uz_prejdene[0] = [None]*len(polygon)
    for i in range(1, len(vsun),1):
        vsun[i] = [None]*len(holes[i-1])
        uz_prejdene[i] = [None]*len(holes[i-1])
    for i in range(len(nasledovne_body)):
        if len(nasledovne_body[i]):
            akt_bod = points[i]
            vsun[akt_bod[1]][akt_bod[2]] = [(points[j][1], points[j][2]) for j in nasledovne_body[i]]
    cesta = []
    DFS((0,0), cesta, polygon, holes, vsun, uz_prejdene)
    return cesta

def polygons_to_wsps(polygons):
    graf = [[] for i in range(len(polygons))] #graf[i] ukazuje, ktore polygony priamo obsahuje
    korene = [1 for i in range(len(polygons))]
    obsahy = [(polygon_area(polygons[i]), i) for i in range(len(polygons))]
    obsahy.sort()
    for i in range(len(obsahy)):
        for j in range(i):
            if korene[obsahy[j][1]] and point_in_polygon(polygons[obsahy[j][1]][0], polygons[obsahy[i][1]]):
                korene[obsahy[j][1]] = 0
                graf[obsahy[i][1]].append(obsahy[j][1])
    hlbky = [None]*len(polygons)
    for x, i in reversed(obsahy):
        if korene[i]:
            hlbky[i] = 0
        for j in graf[i]:
            hlbky[j] = (hlbky[i]+1)%2
    final = []
    for i in range(len(hlbky)):
        if not hlbky[i]:
            tmp = [polygons[j] for j in graf[i]]
            final.append(simplify(polygons[i], tmp))
    return final
    
