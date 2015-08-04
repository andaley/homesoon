import json


fin = open('cl-data.json').read()
parsed_json = json.loads(fin)  # returns list

list_of_dicts = parsed_json[0] # returns list of 4000 dicts

nested_dict = list_of_dicts[0] # sample dict containing posting information

# for key, value in nested_dict.items():
#     print 'Key: %s, Value: %s'% (key, value)

# PostedDate, Latitude, Longitude, and PostingID, work

# Testing the Craigslist data by iterating through list of dictionaries up to the 10th index.
i = 0
while i < 25:
    posting = list_of_dicts[i]
    for key, value in posting.items():
        print 'Key: %s, Value: %s'% (key, value)
    i += 1

# TODO: ignore all objects without a posting URL


# Index o {
# u'PostingID': u'5136224119,5140650178,5143330116,5143790666,5143831051,5135440092,5137929313,5138391377,5139052168,5139544401,5143169297,5146014137',
#  u'url': u'/jsonsearch/apa/?geocluster=102577758894&key=5s0KuyMFKfWJpRTc74ebRw',
#  u'GeoCluster': u'102577758894',
#  u'Longitude': -122.415756078327,
#  u'NumPosts': 12,
#  u'Latitude': 37.789259488482,
#  u'PostedDate': u'1438143822'}
