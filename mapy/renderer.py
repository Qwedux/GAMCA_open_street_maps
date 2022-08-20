import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
import artists
import osm_helper
import location_filter

class Renderer:
    def __init__(self,camera,element_tree):
        #init camera
        self.camera = camera
        zoom = camera.zoom_level
        
        #init el. tree and osm
        self.element_tree = element_tree
        root = self.element_tree.getroot()
        elements = root.getchildren()
        self.osm = osm_helper.OsmHelper(self.element_tree)
        
        #init artists
        self.artisti = artists.get_artists()
        
        artisti = self.artisti
        osm = self.osm
        draw_pairs = []
        for artist in artisti:
            for element in elements:
                if artist.wants_element(element,osm) == True:
                    if artist.draws_at_zoom(element,zoom,osm) == True:
                        draw_pairs.append([element,artist])

        #find map dimensions
        self.minlat = float(root.find('bounds').get('minlat'))
        self.maxlat = float(root.find('bounds').get('maxlat'))
        self.minlon = float(root.find('bounds').get('minlon'))
        self.maxlon = float(root.find('bounds').get('maxlon'))

        #create location_filter
        max_dimensions = location_filter.Rectangle(self.minlat, self.minlon, self.maxlat, self.maxlat)
        typical_querry_size = camera.px_to_gps([camera.get_rect().max_lon // 100, 0])[0]
        self.l_filter = location_filter.LocationFilter(typical_querry_size,max_dimensions,draw_pairs,osm)

    def center_camera(self):
        center_lat = self.maxlat - ((self.maxlat-self.minlat) / 2)
        center_lon =  self.maxlon - ((self.maxlon-self.minlon) / 2)
        self.camera.center_at(center_lat,center_lon)

    def render(self):
        camera = self.camera
        bounding_box = camera.get_rect()

        #create image to be drawn at
        image = Image.new('RGB',[camera.px_width,camera.px_height],color = (0, 0, 0))
        image_draw = ImageDraw.Draw(image)

        #init locatio_filter
        l_filter = self.l_filter
        pairs = l_filter.get_pairs(bounding_box)
        pairs_to_draw = {}

        #init artists and their elements
        for artist in self.artisti:
            pairs_to_draw[artist] = []
            for i in range(len(pairs)):
                if pairs[i][1] == artist:
                    pairs_to_draw[artist].append(pairs[i][0])
        
        #draw elements on image       
        for artist in self.artisti:
            artist.draw(pairs_to_draw.get(artist),self.osm,camera,image_draw)

        return image
            
            
        
