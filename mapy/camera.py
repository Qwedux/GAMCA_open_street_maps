from location_filter import Rectangle
from math import cos, sin

MAX_ZOOM_LEVEL = 15
earth_r = 2*6378000*3.14
  
def get_typical_view_size(zoom_level):
    return 0.0

class Camera:
    def __init__(self, lattitude=0, longitude=0, zoom_level=0, dimensions=(10,10)):
        self.zoom_level = zoom_level
        self.px_width = dimensions[0]
        self.px_height = dimensions[1]
        self.lat = lattitude
        self.lon = longitude
        self.lvl_change()
    
    def lvl_change(self):
        self.met_per_px = 20/1.5**self.zoom_level
        self.lon_r = earth_r*abs((cos(self.lat*3.14/180)))
        self.lat_r = earth_r
        self.lat_deg_per_px = 360/(self.lat_r)*self.met_per_px
        self.lon_deg_per_px = 360/(self.lon_r)*self.met_per_px
        self.lat_px_per_deg = 1/self.lat_deg_per_px
        self.lon_px_per_deg = 1/self.lon_deg_per_px
        
    def px_to_gps(self, px_point):
        x, y = px_point
        lat = (self.px_height/2 - y)*self.lat_deg_per_px + self.lat
        lon = (x - self.px_width/2)*self.lon_deg_per_px + self.lon
        return (lat , lon)
    
    def gps_to_px(self, gps_point):
        lat, lon = gps_point
        x = (lon - self.lon)*self.lon_px_per_deg + self.px_width/2
        y = -(lat - self.lat)*self.lat_px_per_deg + self.px_height/2
        return (x , y)
            
    def zoom_in(self, px_towards):
        gp_point = self.px_to_gps(px_towards)
        self.zoom_level = min(self.zoom_level+1, MAX_ZOOM_LEVEL)
        self.lvl_change()
        self.move_point_to_pixel(gp_point, px_towards)
    
    def zoom_out(self, px_from):
        gp_point = self.px_to_gps(px_from)
        self.zoom_level = max(self.zoom_level-1, 0)
        self.lvl_change()
        self.move_point_to_pixel(gp_point, px_from)
    
    def center_at(self, new_lat, new_lon):
         self.lat = new_lat
         self.lon = new_lon
    
    def px_per_meter(self):
        return 1/self.met_per_px
    
    def move_point_to_pixel(self, gps_point, pixel):
        x,y = self.px_to_gps(pixel)
        u = gps_point[0] - x
        v = gps_point[1] - y
        self.lat += u
        self.lon += v
    
    def get_rect(self):
        x1 = self.lon - self.px_width/2*self.lon_deg_per_px
        y1 = self.lat - self.px_height/2*self.lat_deg_per_px
        x2 = self.lon + self.px_width/2*self.lon_deg_per_px
        y2 = self.lat + self.px_height/2*self.lat_deg_per_px       
        return Rectangle(y1, x1, y2, x2)
