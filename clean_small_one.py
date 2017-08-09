"""
PROJECT #3
Kasey Cox
May 2017

Code to clean a sample of the OSM XML data, load into a Python 
dictionary, and write as a JSON file.

This code is for testing purposes, not for the final product.
"""

## IMPORTS AND GLOBALS
import xml.etree.cElementTree as ET
import re
import string
import json
OSMFILE = "philadelphia_pennsylvania.osm"
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
ADDRESS = ["housenumber", "postcode", "street", "city", "state"]
NODE_KEYS = ["name", "phone", "cuisine", "amenity", "place"]


## FUNCTIONS
def load_by_line(file_in):
    """
    Takes an OSM XML file.

    Iterparses through the file, processing each node then
    writing that node into a JSON file.
    """
    start = 0
    file_out = "{0}-sample.json".format(file_in)
    with open(file_out, "w") as f:
        for event, element in ET.iterparse(file_in, ("start",)):
            start += 1
            if start >= 1630000:
                if element.tag == "node":
                    
                    entry = process_node(element)
                    f.write(json.dumps(entry) + "\n")
                    if start == 1680000:
                        break


def process_node(element):
    """
    Takes an OSM XML element.
    
    Stores specified, cleaned information into a dictionary entry.

    Returns that dictionary.
    """
    node, crtd, pos, addr = {}, {}, {}, {}
    node_refs = []
    node["type"] = element.tag

    # Get element attributes
    for attribute, value in element.attrib.items():
        if attribute in CREATED:
            crtd[attribute] = value
        elif (attribute == "lat") or (attribute == "lon"):
            # check that all num or - or .
            pos[attribute] = check_val(value, '\-?\d+\.?\d')
        else:
            node[attribute] = value

    # Moving onto subelements
    for tag in element.findall("tag"):
        if tag.attrib['k'].split(":")[0] == "addr":
            temp_key = tag.attrib['k'].split(":")[1]
            if temp_key in ADDRESS:
                if temp_key == "housenumber":
                    addr[temp_key] = check_val(tag.attrib['v'], 
                                        '\d+')
                elif temp_key == "postcode":
                    addr[temp_key] = check_val(tag.attrib['v'], 
                                        '\d+\-?\d*')
                elif temp_key == "street":
                    addr[temp_key] = clean_street(tag.attrib['v'])
                elif temp_key == "city":
                    addr[temp_key] = check_val(tag.attrib['v'], 
                                        '\w+\s?\w*')
                elif temp_key == "state":
                    addr[temp_key] = check_val(tag.attrib['v'], 
                                        '\w+\s?\w*')
        elif tag.attrib['k'] in NODE_KEYS:
            node[tag.attrib['k']] = tag.attrib['v']
            

    node["created"] = crtd
    if len(pos) > 0:
        node["pos"] = [pos["lat"], pos["lon"]]
    if len(addr) > 0:
        node["address"] = addr

    return node


def check_val(val, regex):
    """
    Given a value.

    Checks if the provided value matches the provided regular 
    expression.

    Returns the value if a match exists; else 'Invalid' is returned.
    """
    desired_format = re.compile(regex)
    if desired_format.search(val):
        return val
    else:
        return "Invalid"


def clean_street(street):
    """
    Given a string that represents a street name.

    Checks if the provided street name has any abbreviations.

    Returns the cleaned street name; if no cleaning is needed, the 
    street name is returned as provided.
    """
    suffix_mapping = {"st":"Street", "rd":"Road", "ave":"Avenue", 
                "dr":"Drive", "ct":"Court", "blvd":"Boulevard",
                "ln":"Lane", "pl":"Place", "pkwy":"Parkway",
                "sq":"Square", "trl":"Trail", "ter":"Terrace",
                "cir":"Circle", "hwy":"Highway", "grv":"Grove"}
    directional_mapping = {"n":"North", "s":"South", "e":"East",
                    "w":"West"}
    misc_mapping = {"mt":"Mount"}

    # Check for abbreviations in street name
    if check_val(street, '\s+[a-zA-z]+\.?$') != "Invalid":
        split_street_name = street.split(" ")

        # Check suffix
        suffix = lower_strip_period(split_street_name[-1])
        if suffix in suffix_mapping.keys():
            split_street_name[-1] = suffix_mapping[suffix]

        # Check directional prefix
        dir_prefix = lower_strip_period(split_street_name[0])
        if dir_prefix in directional_mapping.keys():
            split_street_name[0] = directional_mapping[dir_prefix]

        # Check misc abbreviations
        if lower_strip_period(split_street_name[0]) in \
            misc_mapping.keys():
            split_street_name[0] = \
                misc_mapping[lower_strip_period(split_street_name[0])]
        elif lower_strip_period(split_street_name[1]) in \
            misc_mapping.keys():
            split_street_name[1] = \
                misc_mapping[lower_strip_period(split_street_name[1])]

    else:
        return "Invalid Street Name"

    return string.join(split_street_name)


def lower_strip_period(str_val):
    """
    Takes a string.

    Returns the string in its lowercase form with spaces and 
    right-handed periods removed.
    """
    return string.lower(str_val).strip().rstrip(".")


## MAIN
load_by_line(OSMFILE)
