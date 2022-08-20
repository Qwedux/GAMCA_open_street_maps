from geometry import polygons_to_wsps
import xml.etree.ElementTree as ET


def tag_dict(element):
    tags = element.findall('tag')
    dic = {}
    for tag in tags:
        dic[tag.attrib['k']] = tag.attrib['v']
    return dic

def id_node_dict(element):
    nodes = element.findall('node')
    dic = {}
    for node in nodes:
        dic[node.attrib['id']] = node
    return dic

def id_way_dict(element):
    ways = element.findall('way')
    dic = {}
    for way in ways:
        dic[way.attrib['id']] = way
    return dic

class OsmHelper:

    def __init__(self, element_tree):
        self.tree = element_tree
        self.root = element_tree.getroot()
        self.node_by_id = id_node_dict(self.root)
        self.way_by_id = id_way_dict(self.root)

    def way_node_ids(self, way):
        nodes = way.findall('nd')
        references = []
        for node in nodes:
            references.append(node.attrib['ref'])
        return references
    
    def way_nodes(self, way):
        references = self.way_node_ids(way)
        nodes = []
        for ref in references:
            node = self.node_by_id[ref]
            nodes.append(node)
        return nodes
    
    def way_coordinates(self, way):
        nodes = self.way_nodes(way)
        nodes_coor = []
        for node in nodes:
            node_coor = (float(node.attrib['lat']), float(node.attrib['lon']))
            nodes_coor.append(node_coor)
        return nodes_coor
    
    def multipolygon_to_polygons(self, multipolygon):
        if tag_dict(multipolygon)['type'] != 'multipolygon':
            return []
        members = multipolygon.findall('member')
        members_coor = []
        for member in members:
            if member.attrib['type'] == 'way':
                way = self.way_by_id[member.attrib['ref']]
                coordinates = self.way_coordinates(way)
                members_coor.append(coordinates)
        return members_coor
    
    def multipolygon_to_wsps(self, multipolygon):
        polygons = self.multipolygon_to_polygons(multipolygon)
        wsps = polygons_to_wsps(polygons)
        return wsps
