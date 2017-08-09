"""
PROJECT #3
Kasey Cox
May 2017


Python code to audit OpenStreetMap data of
Philadelphia, Pennsylvania.

Specifically, code for tag attribute auditing.
"""

## IMPORTS AND GLOBALS
import xml.etree.cElementTree as ET
import pprint
import re
osmfile = "philadelphia_pennsylvania.osm"


## FUNCTIONS
def audit_v_format(osmfile, kval):
    """
    Takes an OSM XML file and tag "k" attribute value (kval).

    Sorts the respective "v" values into categories based on
    formatting.

    Returns a dictionary containing formatting categories
    and the number of "v" values that fit into that
    category.
    """
    limit = 0
    lett_undrsc = re.compile(r'^([a-zA-z]|_)*$')
    problemchars = re.compile(r'[=\+/&<>;:\'"\?%#$@\,\.]')
    whitespaces = re.compile(r'\s')
    keys = {"lett_undrsc": 0, "whitespaces": 0, "problemchars": 0, 
            "other": 0}

    for event, element in ET.iterparse(osmfile, events=("start",)):
        if element.tag == "tag":
            if element.attrib["k"] == kval:
                if lett_undrsc.search(element.attrib['v']):
                    # add to letter/underscore category
                    keys["lett_undrsc"] += 1
                elif whitespaces.search(element.attrib['v']):
                    # add to whitespaces
                    keys["whitespaces"] += 1
                elif problemchars.search(element.attrib['v']):
                    # add to problemchars
                    keys["problemchars"] += 1
                else:
                    # add to other
                    keys["other"] += 1
            
            limit += 1
            if limit == 100000:
                break

    return keys

#print audit_v_format(osmfile, 'addr:city')
#pprint.pprint(result)



def audit_kv_pairs(osmfile, kval):
    """
    Takes an OSM XML file, a tag "k" attribute value (kval), 
    and one of three element types (node, way, or relation).

    Returns a set of unique "v" attribute values for that "k".

    Useful for seeing what kinds of values are contained
    in a particular tag.

    TAKES AWHILE TO COMPLETE RUN
    """
    limit = 0
    attrib_contents = set()

    for event, element in ET.iterparse(osmfile, events=("start",)):
        if element.tag == "tag":
            if element.attrib["k"] == kval: 
                    attrib_contents.add(element.attrib["v"])         

    print "'v' attribute values for k='" + str(kval) \
                + "':", attrib_contents, "\n"
    print "No. items:", len(attrib_contents)


#audit_kv_pairs(osmfile, "addr:postcode")
