from location_filter import Rectangle
from osm_helper import tag_dict  
    

class RoadArtist:
    def __init__(self):
        pass
    
    def wants_element(self, element, osm_helper):
        if (element.tag == 'way'):
            tags = tag_dict(element)
            if ('highway' in tags):
                return True

        else:
            return False

    
    def draws_at_zoom(self, element, zoom, osm_helper):
        
   
        return True

    def draw_element(self, element, osm_helper, camera, image_draw):
        coordinates = osm_helper.way_coordinates(element)
        tags = tag_dict(element)
        road_type = tags.get("highway")
        px_coordinates = []
        for coordinate in coordinates: 
            px_coordinates.append(camera.gps_to_px(coordinate))
            if (road_type == 'footway'):
                image_draw.line(px_coordinates, 'yellow', 1)
                
            elif (road_type == 'motorway'):
                image_draw.line(px_coordinates, 'red', 5)
                
            elif (road_type == 'primary'):
                image_draw.line(px_coordinates, 'red', 3)
                
            elif (road_type == 'track'):
                image_draw.line(px_coordinates, 'green', 3)
                
            elif (road_type == 'motorway_link'):
                image_draw.line(px_coordinates, 'teal', 5)
            
            elif (road_type == 'secondary'):
                image_draw.line(px_coordinates, 'red', 2)
                        
            else:
                image_draw.line(px_coordinates, None, 1)
        return 
    
    def draw(self, elements, osm_helper, camera, image_draw):
        layers = []
        for element in elements:
            tags = tag_dict(element)
            layer = tags.get("layer")
            if (layer == None):
                layers.append((element, 1))
            else:
                layers.append((element, layer))
        for j in range(5):
            i = j - 2
            for element, layer in layers:
                if int(layer) == i:
                    self.draw_element(element, osm_helper, camera, image_draw)
 
   

             
    
    def approx_location(self, element, osm_helper):
        rectangles = []
        chunks = []
        coordinates = osm_helper.way_coordinates(element)
        for i in range(0, len(coordinates), 100):
            chunks.append(coordinates[i:i + 100])
        for chunk in chunks:
            Xcoord = []
            Ycoord = []
            for x, y in chunk:
                Xcoord.append(x)
                Ycoord.append(y)
            rectangles.append(Rectangle(min(Xcoord), min(Ycoord), max(Xcoord), max(Ycoord)))
        return rectangles

        
     























































       
