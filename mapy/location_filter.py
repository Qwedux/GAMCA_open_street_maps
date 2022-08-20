#latest version





import math

class PointV:
    def __init__(self,rec):
        X = (rec.min_lat+rec.max_lat)/2
        Y = (rec.min_lon+rec.max_lon)/2
        W = abs((rec.min_lat-rec.max_lat)/2)
        H = abs((rec.min_lon-rec.max_lon)/2)
        self.x=X
        self.y=Y
        self.w=W
        self.h=H
    def Loc(self,PV):
        if abs(self.x-PV.x)<=abs(self.w+PV.w):
            if abs(self.y-PV.y)<=abs(self.h+PV.h):
                return True

def AproxRectangle(rec,tqs,bb):
    return [math.ceil((rec.min_lat+rec.max_lat-2*bb.min_lat)/2/tqs),math.ceil((rec.min_lon+rec.max_lon-2*bb.min_lon)/2/tqs)]

def RecBounds(rectangle,tqs,bounding_box):
    a = math.floor((rectangle.min_lat-bounding_box.min_lat)/tqs)
    b = math.ceil((rectangle.max_lat-bounding_box.min_lat)/tqs)
    c = math.floor((rectangle.min_lon-bounding_box.min_lon)/tqs)
    d = math.ceil((rectangle.max_lon-bounding_box.min_lon)/tqs)
    return [a,b,c,d]

class Rectangle:
    def __init__(self,min_lat,min_lon,max_lat,max_lon):
        self.min_lat=min_lat
        self.max_lat=max_lat
        self.min_lon=min_lon
        self.max_lon=max_lon
class LocationFilter:
    def __init__(self,
                 typical_query_size,
                 bounding_box,
                 draw_pairs,
                 osm_helper):
        self.typical_query_size=typical_query_size
        self.bounding_box=bounding_box
        self.draw_pairs=draw_pairs
        self.osm_helper=osm_helper
        self.q=[]
        for x in range(math.ceil((bounding_box.max_lat-bounding_box.min_lat)/typical_query_size)+1):
            self.q.append([])
            for y in range(math.ceil((bounding_box.max_lon-bounding_box.min_lon)/typical_query_size)+1):
                self.q[x].append([])
        for pair in self.draw_pairs:
            u=pair[1].approx_location(pair[0],self.osm_helper)
            for rec in u:
                Location = AproxRectangle(rec,self.typical_query_size,self.bounding_box)
                if  (pair not in self.q[Location[0]][Location[1]]):
                    self.q[Location[0]][Location[1]].append(pair)
                    
    def get_pairs(self,rectangle):
        res = []
        rv = PointV(rectangle)
        RectangleBounds = RecBounds(rectangle,self.typical_query_size,self.bounding_box)
        for x in range(max(0,RectangleBounds[0]-1),min(len(self.q),RectangleBounds[1]+2)):
            for y in range(max(0,RectangleBounds[2]-1),min(len(self.q[x]),RectangleBounds[3]+2)):
                for pair in self.q[x][y]:
                    for rec in pair[1].approx_location(pair[0],self.osm_helper):
                        pv = PointV(rec)
                        if rv.Loc(pv) and pair not in res:
                            res.append(pair)
                            break
        #for pair in self.draw_pairs:
        #    for rec in pair[1].approx_location(pair[0],self.osm_helper):
        #        pv = PointV( (rec.min_lat+rec.max_lat)/2, (rec.min_lon+rec.max_lon)/2 , abs((rec.min_lat-rec.max_lat)/2) , abs((rec.min_lon-rec.max_lon)/2) )
        #        if rv.Loc(pv):
        #            res.append(pair)
        #            break
        
        return res


