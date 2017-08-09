"""
PROJECT #3
Kasey Cox
May 2017

Python code to audit OpenStreetMap data of Philadelphia, Pennsylvania.

OSM XML file from MapZen.com Metro Extracts:
https://mapzen.com/data/metro-extracts/metro/philadelphia_pennsylvania/101718083/Philadelphia/
"""

## IMPORTS AND GLOBALS
import xml.etree.cElementTree as ET
import pprint
osmfile = "philadelphia_pennsylvania.osm"

def audit_elements(osmfile):
    """
    An audit of all top level element names.

    Takes an OSM XML file and returns a
    dictionary containing tag names and their
    respective count.

    {"tag_name": 4, "tag_name2": 3, ....}
    """
    key_list, count_list = [], []
    for event, element in ET.iterparse(osmfile, events=("start",)):
        if element.tag not in key_list:
            # initialize in key_list and count_list
            key_list.append(element.tag)
            count_list.append(1)
        else:
            # increment count
            count_list[key_list.index(element.tag)] += 1
        break

    # Populate dictionary
    tags = {}
    for key, count in zip(key_list, count_list):
        tags[key] = count

    return tags

"""
Results of audit_tags(osmfile):
{'node': 3113088, 'nd': 3809113, 'bounds': 1, 'member': 59516, 
'tag': 1794166, 'osm': 1, 'way': 324733, 'relation': 4946}
"""


def audit_attribs(osmfile):
    """
    Finds attributes found in distinct top
    level tags (found using audit_tags function).
    
    Because the file is very large, limited to the
    first 10,000 lines when testing.

    Takes osmfile and returns a dictionary:
    {   
        "node": {set([attrib1, attrib2, ...]), 
                "subtag attributes": set([attrib1, ...])},
        "way": {set([attrib1, attrib2, ...]), 
                "nd": set([attrib1, attrib2, ...]),
                "subtag attributes":set([attrib1, attrib2, ...])},        
        "relation": {set([attrib1, attrib2, ...]),
                    "member": set([attrib1, attrib2, ...]),
                    "subtag attributes": set([attrib1, attrib2, ...])}
    }
    """
    limit = 0
    audit = {}
    node_attribs, node_subtag_attribs = set(), set()
    way_attribs, way_subtag_attribs, nd_attribs = set(), set(), set()
    relation_attribs, member_attribs = set(), set() 
    rel_subtag_attribs = set()

    for event, element in ET.iterparse(osmfile, events=("start",)):   
        if element.tag == "node":
            for node_attr in element.attrib.keys():
                node_attribs.add(node_attr)
            for subtag in element.iter("tag"):
                # for subtags in node
                for subtag_attr in subtag.attrib.keys():
                    node_subtag_attribs.add(subtag_attr)
        elif element.tag == "way":
            for way_attr in element.attrib.keys():
                way_attribs.add(way_attr)
            for way_subtag in element.iter("tag"):
                # for subtags in way
                for way_subtag_attr in way_subtag.attrib.keys():
                    way_subtag_attribs.add(way_subtag_attr)
            for nd in element.iter("nd"):
                # for nd's in way
                for nd_attr in nd.attrib.keys():
                    nd_attribs.add(nd_attr)
        elif element.tag == "relation":
            for relation_attr in element.attrib.keys():
                relation_attribs.add(relation_attr)
            for member in element.iter("member"):
                # for members in relation
                for member_attr in member.attrib.keys():
                    member_attribs.add(member_attr)
            for rel_subtag in element.iter("tag"):
                # for subtags in relation
                for rel_subtag_attr in rel_subtag.attrib.keys():
                    rel_subtag_attribs.add(rel_subtag_attr)

        """       
        limit += 1
        if limit == 10000:
            break
        """

    audit["node"] = {"attributes":node_attribs, "subtag attributes": 
					node_subtag_attribs}
    audit["way"] = {"attributes":way_attribs, 
					"subtag attributes":way_subtag_attribs,
                    "nd attributes":nd_attribs}
    audit["relation"] = {"attributes":relation_attribs, 
						"member attributes":member_attribs,
						"subtag attributes":rel_subtag_attribs}

    return audit


"""
Results of audit_attribs(osmfile) with pretty print:
{'node': {'attributes': set(['changeset',
                             'id',
                             'lat',
                             'lon',
                             'timestamp',
                             'uid',
                             'user',
                             'version']),
          'subtag attributes': set(['k', 'v'])},
 'relation': {'attributes': set(['changeset',
                                 'id',
                                 'timestamp',
                                 'uid',
                                 'user',
                                 'version']),
              'member attributes': set(['ref', 'role', 'type']),
              'subtag attributes': set(['k', 'v'])},
 'way': {'attributes': set(['changeset',
                            'id',
                            'timestamp',
                            'uid',
                            'user',
                            'version']),
         'nd attributes': set(['ref']),
         'subtag attributes': set(['k', 'v'])}}
"""

import re
def audit_k_formats(osmfile):
    """
    Takes an OSM XML file.

    Audits tag "k" attributes based on format.

    Returns a dictionary of those formats and
    the respective counts of attributes that
    fall into that format.
    """
    limit = 0
    lett_undrsc = re.compile(r'^([a-z]|_)*$')
    single_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
    problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
    keys = {"lett_undrsc": 0, "single_colon": 0, "problemchars": 0, 
            "other": 0}

    for event, element in ET.iterparse(osmfile, events=("start",)):
        if element.tag == "tag":
            if lett_undrsc.search(element.attrib['k']):
                # add to letter/underscore category
                keys["lett_undrsc"] += 1
            elif single_colon.search(element.attrib['k']):
                # add to single_colon
                keys["single_colon"] += 1
            elif problemchars.search(element.attrib['k']):
                # add to problemchars
                keys["problemchars"] += 1
            else:
                # add to other
                keys["other"] += 1


        limit += 1
        if limit == 10000:
            break


    return keys

#print audit_k_formats(osmfile)

"""
Results of audit_key_type(osmfile):
{'problemchars': 9, 'other': 182007, 'single_colon': 660267, 
'lett_undrsc': 951883}

'lett_undrsc':
OK, leave as is.

single colon:
left_side:right_side# ----> left_side:{right_side1:rs_value1, 
right_side2:rs_value2}

Problemchars:
set(['Price and Price Elder Law', 'tiger.source:tlid', 'fuel:2.14', 
'max speed', 'store number', 'service area'])
- those with spaces can have the spaces replaced with underscores
> - uppercase characters can be made lowercase
> - for k='tiger.source:tlid', v="survey"; replace k with 'source'
> - for k='fuel:2.14', v='yes'; ignore this, meaning is ambiguous

Examples of other:
set(['gnis:ST_alpha', 'gnis:County_num', 'gnis:ST_num', 'FIXME', 
'gnis:Class', 'gnis:County', 'TODO'])
> - In this scenario, 'other' seems to include k attributes with 
spaces, uppercase letters, and/or two colons
> - uppercase characters can be made lowercase
> - for single colon entries, left side will constitute a dictionary 
and the right value will be the keys in that dictionary; 
left_side:right_side# ----> left_side:{right_side1:rs_value1, 
									    right_side2:rs_value2}
"""


def k_tag_counts(osmfile):
    """
    Audits tags' "k" attributes.

    Takes an OSM XML file and returns a dictionary 
    containing tag "k" attributes and their respective count.

    {"k_key": 4, "k_key": 3, ....}

    Because the file is very large, lines read are 
    limited when testing.
    """
    limit = 0
    k_vals, k_counts = [], []

    for event, element in ET.iterparse(osmfile, events=("start",)):
        if element.tag == "tag":
            if element.attrib["k"] not in k_vals:
                # initialize in key_list and count_list
                k_vals.append(element.attrib["k"])
                k_counts.append(1)
            else:
                # increment count
                k_counts[k_vals.index(element.attrib["k"])] += 1          

            limit += 1
            if limit == 90000:
                break

    # Populate dictionary
    tag_ks = {}
    for key, count in zip(k_vals, k_counts):
        tag_ks[key] = count

    return tag_ks

result = k_tag_counts(osmfile)
#print result
#pprint.pprint(result)
#print result["place"]

"""
 ...
 'abandoned': 1,
 'abandoned:building': 1,
 'abandoned:railway': 1,
 'access': 7,
 'addr:city': 71,
 'addr:country': 1,
 'addr:county': 1,
 'addr:housename': 5,
 'addr:housenumber': 93,
 'addr:postcode': 80,
 'addr:state': 1197,
 'addr:street': 105,
  ...
 'traffic_calming': 43,
 'traffic_signals': 111,
 'traffic_signals:direction': 4,
 'traffic_signals:sound': 1,
 'train': 14,
 'type': 2,
 'url': 15,
"""
