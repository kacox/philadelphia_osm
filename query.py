"""
PROJECT #3
Kasey Cox
May 2017

Code to query a local instance of MongoDB that contains cleaned OSM 
XML data for Philadelphia, Pennsylvania.
"""


## IMPORTS AND GLOBALS
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client.test

## FUNCTION(S)
def agg_query(pipeline):
    """
    Takes an aggregation pipeline (list).

    Queries the database and returns the
    result of the query.
    """
    return db.osmdata.aggregate(pipeline)


###### MAIN ##########################################
## Number of unique users contributing to nodes
user_query = [  {"$group": {"_id":"$created.uid", "unique_users": 
                            {"$addToSet":"$_id"}}},
                {"$project":{"_id":0, 
                            "total_users":{"$size":"$unique_users"}}},
                {"$sort":{"total_users":-1}},
                {"$limit":1}
             ]
#for results in agg_query(user_query):
    #print results

"""
Results:
{u'total_users': 764695}
"""

## Finding number of schools in Philadelphia
# Finding amenity values related to schools:
amenity_query = [   {"$match":{"address.city":"Philadelphia"}},
                    {"$group":{"_id":"$amenity", 
                                "names":{"$addToSet":"$name"}}},
                    {"$project":{"_id":0, "amenity":"$_id"}}
                ]
#for amenity_type in agg_query(amenity_query):
    #print amenity_type
"""
Results:
...
{u'amenity': u'parking_entrance'}
{u'amenity': u'library'}
{u'amenity': u'kindergarten'}
...
{u'amenity': u'school'}
{u'amenity': u'pub'}
{u'amenity': None}
{u'amenity': u'bar'}
{u'amenity': u'pharmacy'}
{u'amenity': u'restaurant'}

Comment:
School amenity names (visual inspection): "kindergarten", "school"
"""

kinder_school_query = [ {"$match":{"amenity":{"$in":["kindergarten", 
                                                        "school"]}, 
                                    "address.city":"Philadelphia"}},
                        {"$project":{"_id":0, "name":"$name"}}
                      ]
#for kinder_school in agg_query(kinder_school_query):
    #print kinder_school
"""
Results:
{u'name': u'C.W. Henry Elementary School'}
{u'name': u'Norwood Fontbonne Academy - Norwood Campus'}
{u'name': u'Saint Francis de Sales School'}
{u'name': u'Mastery Charter School: Hardy Williams Campus'}
{u'name': u'Hallahan Catholic Girls High School'}
{u'name': u'Greene Street Friends School'}
{u'name': u'Politz Hebrew Academy'}
{u'name': u'Laboratory Charter School'}
{u'name': u'Totally Tots Inc.'}
{u'name': u"Saint Martin's School"}

Comment:
There are definitely more than 10 schools in Philadelphia. It is 
possible that they were never tagged as schools explicitly. How many 
schools are there in Philadelphia when searching by name rather than 
by amenity tag?
"""

## Text queries in "name" field
school_query = [    {"$match":{"$text":{"$search":"School"}}},
                    {"$group":{"_id":"$address.city", 
                                "count":{"$sum":1}}},
                    {"$match": {"$or":[{"_id":"Philadelphia"}, 
                                        {"_id":"philadelphia"}, 
                                        {"_id":None}] }}
               ]

academy_query = [   {"$match":{"$text":{"$search":"Academy"}}},
                    {"$group":{"_id":"$address.city", 
                                "count":{"$sum":1}}},
                    {"$match": {"$or":[{"_id":"Philadelphia"}, 
                                        {"_id":"philadelphia"}, 
                                        {"_id":None}] }}
                ]
#print '\nEntries with "School"'
#for thing in agg_query(school_query):
    #print thing
#print '\nEntries with "Academy"'
#for thing2 in agg_query(academy_query):
    #print thing2

"""
Results:
Entries with "School"
{u'count': 8, u'_id': u'Philadelphia'}
{u'count': 1456, u'_id': None}
{u'count': 1, u'_id': u'philadelphia'}

Entries with "Academy"
{u'count': 2, u'_id': u'Philadelphia'}
{u'count': 106, u'_id': None}

Comment:
It is clear that there is a disconnect between proper amenity tagging 
and places that are schools.

There are potentially Philadelphia schools in results that do not have 
a city tagged to it (None).
"""

## Most popular cuisine in area
cuisine_query = [   {"$group":{"_id":"$cuisine", "count":{"$sum":1}}},
                    {"$project":{"_id":0, 
                                    "name":"$_id", 
                                    "count":"$count"}},
                    {"$sort":{"count":-1}},
                    {"$limit":10}
                ]
#for cuisine_type in agg_query(cuisine_query):
    #print cuisine_type

"""
Results:
{u'count': 3112260, u'name': None}
{u'count': 155, u'name': u'pizza'}
{u'count': 66, u'name': u'burger'}
{u'count': 64, u'name': u'chinese'}
{u'count': 62, u'name': u'coffee_shop'}
{u'count': 57, u'name': u'italian'}
{u'count': 54, u'name': u'sandwich'}
{u'count': 53, u'name': u'mexican'}
{u'count': 43, u'name': u'american'}
{u'count': 19, u'name': u'asian'}

Comment:
Pizza is a type of Italian food. "italian" has 57 counts and "pizza" 
has 155.

Italian cuisine comfortably leads the popularity list with 212 counts.
"""

## Restaurants nearest to the airport
airport_query = [   {"$match":{"$text":{"$search":"International"}}}]

"""
Comment:
No Philadelphia International Airport entry (the major airport in the 
area); tried with [{"$match":{"$text":{"$search":"International"}] as 
well as "Airport" as a key word.

Inserted a document for this node.
"""

philly_intrntl = {"address":{"city":"Philadelphia", "state":"PA"}, 
                    "pos":[39.871944, -75.241111],
                    "name":"Philadelphia International Airport",
                    "amenity":"airport"}

#db.osmdata.insert(philly_intrntl)

## db.osmdata.ensureIndex({"pos":"2d"})        # In the Mongo shell

pos_query = [   {"$geoNear": {"near":[39.871944, -75.241111], 
                                "distanceField":"dist.calculated", 
                                "query": {"amenity": 
                                            {"$in": ["restaurant", 
                                                        "bar", "pub", 
                                                        "fast_food", 
                                                        "bar;pub"]} }}},
                {"$limit":1}
            ]
agg_query(pos_query)

for item in agg_query(pos_query):
    print item

"""
Result:
{u'amenity': u'fast_food', u'dist': {u'calculated': 
0.004474988617863642}, u'name': u"Green Leaf's", u'created': 
{u'changeset': u'34171919', u'version': u'1', u'user': u'dbaron', 
u'timestamp': u'2015-09-21T21:25:08Z', u'uid': u'481533'}, 
u'pos': [39.8754277, -75.2383022], 
u'_id': ObjectId('592c5021ab26e56b372c57a4'), u'type': u'node', 
u'id': u'3753512142'}

Comment:
A quick Google map search confirms that Green Leaf's is a restaurant 
nearby Philadelphia International Airport.
"""
