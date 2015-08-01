import json


fin = open('cl-data.json').read()
parsed_json = json.loads(fin)

useful_dict = parsed_json[0]
print type(useful_dict)
# print useful_dict

print type(useful_dict[0])
print 'Index o', useful_dict[0]

for d in useful_dict:
    print d['PostedDate']

# PostedDate, Latitude, Longitude, and PostingID, work


# Index o {
# u'PostingID': u'5136224119,5140650178,5143330116,5143790666,5143831051,5135440092,5137929313,5138391377,5139052168,5139544401,5143169297,5146014137',
#  u'url': u'/jsonsearch/apa/?geocluster=102577758894&key=5s0KuyMFKfWJpRTc74ebRw',
#  u'GeoCluster': u'102577758894',
#  u'Longitude': -122.415756078327,
#  u'NumPosts': 12,
#  u'Latitude': 37.789259488482,
#  u'PostedDate': u'1438143822'}


# [[{"Ask":"4095","ImageThumb":"http:\/\/images.craigslist.org\/00R0R_rbbDV8fOzp,0:00101_id4Wdg7G4Vt,0:00H0H_6QPFUVzhVen,0:00P0P_hutUiqbKfK,0:00G0G_dZEAXHTKtci,0:00e0e_5kHe1MDU253,0:00m0m_YYoboLO3M3,0:00d0d_eEsiPeDf9Qn_50x50c.jpg","Latitude":37.324476,"PostingTitle":"Your 3 bedroom home, ready NOW with a special","PostedDate":"1438385562","Longitude":-121.971828,"PostingURL":"\/\/sfbay.craigslist.org\/sby\/apa\/5150641297.html","Bedrooms":"3","CategoryID":"1","PostingID":"5150641297"}
#
# ,{"Longitude":-122.223872512748,"NumPosts":2,"PostedDate":"1438385549","GeoCluster":"102587075736","PostingID":"5145542605,5146875914","url":"\/jsonsearch\/apa\/?geocluster=102587075736&key=E23s6PbyAdDY5kSkRZN6NQ","Latitude":38.0531065531255},
#
# {"Longitude":-122.224044,"PostingURL":"\/\/sfbay.craigslist.org\/eby\/apa\/5146879148.html","Ask":"1400","Bedrooms":"3","ImageThumb":"http:\/\/images.craigslist.org\/00f0f_79fT2tZYW9t,0:00a0a_6YrkqHzb41y,0:00B0B_9Sn3PI3T301,0:00Q0Q_fTH59PBqh1n,0:00v0v_kRjNht8rXj8,0:00V0V_cenD78vVxlz,0:00T0T_lwC18mNQCU1,0:00Y0Y_6Sodehi6nyb,0:00z0z_25o2wqtSaKy,0:00505_1UFgloQulOU,0:01717_lu2nYAOGNWb,0:00B0B_5wu3TI8645V,0:00o0o_5g9a5P4m3o2_50x50c.jpg","PostingID":"5146879148","CategoryID":"1","Latitude":38.053163,"PostingTitle":"Spacious Updated 3\/1 in quiet Crockett neighborhood","PostedDate":"1438385529"},
#
# {"Ask":"2695","ImageThumb":"http:\/\/images.craigslist.org\/00707_gAgQM0SzQae,0:00S0S_aSVj8nrU686,0:00n0n_fgOfdDOWXH4,0:00H0H_kzUuPN2yMmd,0:00f0f_lSxKRHNkhUc,0:00808_2JolCXlyOw9,0:01313_cQWZr1I3z0x,0:00H0H_6KIl4F3LYhD,0:00V0V_hlYM9bZOUM1_50x50c.jpg","Latitude":37.562883,"PostingTitle":"2BR\/2BACondo\/Forest Park Elementary-Furnished Kitchen","PostedDate":"1438385522","Longitude":-122.049521,"PostingURL":"\/\/sfbay.craigslist.org\/eby\/apa\/5150640435.html","Bedrooms":"2","CategoryID":"1","PostingID":"5150640435"}
