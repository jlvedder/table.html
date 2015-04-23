import json, os

print os.getcwd()
os.chdir("python/datasets")
print os.getcwd()

def getContents(fileName):

    file = open(fileName, 'r')
    contents = file.read()
    file.close()

    return contents

def placeContents(fileName, contents):

    file = open(fileName, 'w')
    file.write(contents)
    file.close()



import sys

data = json.loads(getContents(sys.argv[1]))

print data

xml = '<?xml version="1.0" encoding="utf-8"?>\n<PageEntry PRIMRVersion="2.0">\n'

xmlSequence = ['book_name', 'facility', 'product', 'form_type', 'dt_time', 'cell_day', 'brx_day', 'vcd', 'viability', 'ph', 'glucose', 'glutamine', 'avg_cell_density', 'hfr', 'cspr', 'harvest_ph', 'pco2', 'po2', 'do2', 'lactate', 'glutamate', 'osmo', 'ecs_density', 'ecs_viability', 'media_lot', 'loadinfo']

jsonID_to_xmlTag_map = {'book_name':'book_name', 'dt_time':'dt_time', 'glucose':'glucose','vcd':'via_cell_density','viability':'viability_','ph':'offline_ph','avg_cell_density':'acd','hfr':'current_hfr','cspr':'cell_sp__perf_rate_cspr','pco2':'offline_pco2', 'ecs_density':'ecs_via_cell_density', 'ecs_viability':'ecs_viability_', }


masterID = ""

for id in data:
    masterID = id
    break

print "masterID:" + masterID
# masterID = "c4002214101stn_1 101314am comment__fl"

book_name = masterID[0:masterID.index("stn")]
book_name = book_name[0:6] + "-" + book_name[6:]
print "book_name:" + book_name

data[masterID.split(" ")[0] + " " + masterID.split(" ")[1] + " " + "book_name"] = book_name


# dt_time MM/DD/YYYY HR:MM (24 hour clock), from 101314/AM 0715, 101314/PM 0715

# masterID = "c4002214101stn_1 101314am comment__fl"

date = masterID.split(" ")[1] # 101314am
hrMins = data[masterID.split(" ")[0] + " " + masterID.split(" ")[1] + " time"] 
# date = 101314pm
# hrMins = 0817

# MM/DD/YYYY HR:MM

formattedDate = date[0:2] + "/" + date[2:4] + "/20" + date[4:6]
formattedTime = hrMins[0:2] + ":" + hrMins[2:4]

formattedDateTime = formattedDate + " " + formattedTime
print "formattedDateTime:", formattedDateTime

data[masterID.split(" ")[0] + " " + masterID.split(" ")[1] + " " + "dt_time"] = formattedDateTime

'''
{ 'c4002214105stn_7 101214am time': '0817',
  'c4002214105stn_7 101214am online_ph': '6.90',
  'c4002214105stn_7 101214am offline_ph': '6.88',
  'c4002214105stn_7 101214am ph_difference': '0.02',
  'c4002214105stn_7 101214am harvest_online_ph': '6.50',
  'c4002214105stn_7 101214am harvest_offline_ph': '6.49',
  'c4002214105stn_7 101214am harvest_ph_difference': '0.01',
  'c4002214105stn_7 101214am offline_pco2': '177.7',
  'c4002214105stn_7 101214am glucose': '0.090',
  'c4002214105stn_7 101214am glutamine': '0.145',
  'c4002214105stn_7 101214am via_cell_density': '36.00',
  'c4002214105stn_7 101214am viability_': '91.7',
  'c4002214105stn_7 101214am ecs_via_cell_density': '1.70',
  'c4002214105stn_7 101214am ecs_viability_': '75.9',
  'c4002214105stn_7 101214am current_hpr_rpm': '45.4',
  'c4002214105stn_7 101214am current_hfr': '0.60',
  'c4002214105stn_7 101214am acd': '36.14',
  'c4002214105stn_7 101214am do2_demand_slpm': '5.07',
  'c4002214105stn_7 101214am max_do2_sp_': '50',
  'c4002214105stn_7 101214am macrosparge_slpm': '6.10',
  'c4002214105stn_7 101214am current_antifoam_rpm': '9.9',
  'c4002214105stn_7 101214am max_do2_sp_adjustment': 'NA',
  'c4002214105stn_7 101214am do2_alarm_adjustment': 'NA',
  'c4002214105stn_7 101214am brx_ph_adjustment': 'NA',
  'c4002214105stn_7 101214am harvest_ph_adjustment': 'NA',
  'c4002214105stn_7 101214am hpr_adjustment': 'NA',
  'c4002214105stn_7 101214am macrosparge_adjustment_slpm': 'NA',
  'c4002214105stn_7 101214am antifoam_adjustment': 'NA',
  'c4002214105stn_7 101214am cell_bleed': '0.4',
  'c4002214105stn_7 101214am actual_transonic_flow': '0.61',
  'c4002214105stn_7 101214am cell_sp__perf_rate_cspr': '0.12',
  'c4002214105stn_7 101214am comment__fl': '4' }
'''


# book_name, eg. C40022-14101
#
# id = ""
#
# for id in data:
#     sampleID = id
#
# book_name = sampleID.split(" ")[0]
# book_name = book_name[0:book_name.index("stn")]
#
# data["a b book_name"] = book_name

# facility is not included in the table

# product is not included in the table

# form_type is not included in the table, [Steady State, Batch, Growth]

# dt_time MM/DD/YYYY HR:MM (24 hour clock), from 101314/AM 0715, 101314/PM 0715

# cell_day', 'brx_day' are automatically populated

# harvest_ph is no longer taken

# po2 should be added to the table

# do2 is automatically populated

# lactate should be added to the table

# glutamate, glutamine we don't need (no longer being recorded for this campaign)

# osmo should be added to the table

# media_lot should be added to the table

spacer = '    '
for element in xmlSequence:
    print element
    openingTag = "<" + element + ">"
    closingTag = "</" + element + ">\n"
    try:
        for id in data:
            if id.split(" ")[2] == jsonID_to_xmlTag_map[element]:
                xml += spacer + openingTag + data[id] + closingTag
                break
        # if jsonID_to_xmlTag_map[element] in data:
        #     xml += spacer + openingTag + data[element] + closingTag
        # else:
        #     xml += spacer + openingTag + closingTag
    except:
        xml += spacer + openingTag + closingTag

xml += '</PageEntry>'

placeContents(sys.argv[1] + ".xml", xml)

print xml