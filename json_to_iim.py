import json, os, sys

print os.getcwd()
# os.chdir("python/datasets")
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

stockData = '{"c4002214101stn_1 101314am time":"0715","c4002214101stn_1 101314am online_ph":"6.90","c4002214101stn_1 101314am offline_ph":"6.88","c4002214101stn_1 101314am ph_difference":"0.02","c4002214101stn_1 101314am harvest_online_ph":"6.50","c4002214101stn_1 101314am harvest_offline_ph":"6.476","c4002214101stn_1 101314am harvest_ph_difference":"0.03","c4002214101stn_1 101314am offline_pco2":"177.2","c4002214101stn_1 101314am glucose":"0.152","c4002214101stn_1 101314am glutamine":"0.203","c4002214101stn_1 101314am via_cell_density":"42.90","c4002214101stn_1 101314am viability_":"94.2","c4002214101stn_1 101314am ecs_via_cell_density":"2.33","c4002214101stn_1 101314am ecs_viability_":"72.6","c4002214101stn_1 101314am current_hpr_rpm":"45.8","c4002214101stn_1 101314am current_hfr":"0.61","c4002214101stn_1 101314am acd":"42.51","c4002214101stn_1 101314am do2_demand_slpm":"4.61","c4002214101stn_1 101314am max_do2_sp_":"50","c4002214101stn_1 101314am macrosparge_slpm":"6.00","c4002214101stn_1 101314am current_antifoam_rpm":"9.9","c4002214101stn_1 101314am max_do2_sp_adjustment":"","c4002214101stn_1 101314am do2_alarm_adjustment":"","c4002214101stn_1 101314am brx_ph_adjustment":"","c4002214101stn_1 101314am harvest_ph_adjustment":"","c4002214101stn_1 101314am hpr_adjustment":"","c4002214101stn_1 101314am macrosparge_adjustment_slpm":"NA","c4002214101stn_1 101314am antifoam_adjustment":"","c4002214101stn_1 101314am cell_bleed":"1.1","c4002214101stn_1 101314am actual_transonic_flow":"0.61","c4002214101stn_1 101314am cell_sp__perf_rate_cspr":"0.10","c4002214101stn_1 101314am comment__fl":"107"}'



# data = json.loads(getContents(sys.argv[1]))
data = json.loads(stockData)
stockData = json.loads(stockData)


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

book_name = 'C06242-14101'

imacro = ''

imacro += '''VERSION BUILD=8070701 RECORDER=CR
URL GOTO=http://bioweb/TechOps/MFG/Pages/default.aspx
TAG POS=1 TYPE=A ATTR=TXT:PRIMR<SP>Process<SP>Entry<SP>Forms
WAIT SECONDS=2
TAG POS=1 TYPE=INPUT:TEXT FORM=NAME:loginform ATTR=NAME:name CONTENT=jvedder
SET !ENCRYPTION NO
TAG POS=1 TYPE=INPUT:PASSWORD FORM=NAME:loginform ATTR=NAME:password CONTENT=JVedder1_bmrn
TAG POS=1 TYPE=INPUT:SUBMIT FORM=NAME:loginform ATTR=NAME:Login
TAG POS=1 TYPE=INPUT:SUBMIT FORM=NAME:confirmLogin ATTR=NAME:Confirm
WAIT SECONDS=2\n'''

book_name = book_name.upper()
imacro += 'TAG POS=1 TYPE=A ATTR=TXT:' + book_name + '\n'

imacro += "WAIT SECONDS=5\n"
imacro += "TAG POS=1 TYPE=A ATTR=TXT:Daily<SP>Samples<SP>-<SP>" + str(83) + "\n"
imacro += '''WAIT SECONDS=3
FRAME F=2
TAG POS=1 TYPE=DIV ATTR=TXT:Bioreactor<SP>Lot:<SP>lockInput(document.forms[0].book_name)*
TAG POS=1 TYPE=SELECT FORM=ACTION:https://hosting01.discoverant.com:18443/Aegis-PRIMR/PageEntryManager ATTR=ID:product CONTENT=%asb
TAG POS=1 TYPE=INPUT:TEXT FORM=ACTION:https://hosting01.discoverant.com:18443/Aegis-PRIMR/PageEntryManager ATTR=NAME:dt_time CONTENT='''

timeToInsert = formattedDateTime[:10] + "<SP>" + formattedDateTime[11:]
imacro += timeToInsert + '\n'

# print imacro

imacroIDs = ['vcd', 'viability', 'ph', 'glucose', 'avg_cell_density', 'hfr', 'cspr', 'pco2', 'po2', 'lactate', 'osmo', 'ecs_density', 'ecs_viability', 'media_lot']

for id in imacroIDs:

    imacro += 'TAG POS=1 TYPE=INPUT:TEXT FORM=ACTION:https://hosting01.discoverant.com:18443/Aegis-PRIMR/PageEntryManager ATTR=ID:' + id + ' CONTENT='

    try:
        for key in stockData:
            # print stockData
            # print key
            if key.split(" ")[2] == jsonID_to_xmlTag_map[id]:
                print "TRUE"
                imacro += stockData[key]
                break
    except:
        imacro += ''

    imacro += '\n'

imacro += 'TAG POS=1 TYPE=SPAN ATTR=TXT:Check<SP>Form'

print imacro

stockData = '{"c4002214101stn_1 101314am time":"0715","c4002214101stn_1 101314am online_ph":"6.90","c4002214101stn_1 101314am offline_ph":"6.88","c4002214101stn_1 101314am ph_difference":"0.02","c4002214101stn_1 101314am harvest_online_ph":"6.50","c4002214101stn_1 101314am harvest_offline_ph":"6.476","c4002214101stn_1 101314am harvest_ph_difference":"0.03","c4002214101stn_1 101314am offline_pco2":"177.2","c4002214101stn_1 101314am glucose":"0.152","c4002214101stn_1 101314am glutamine":"0.203","c4002214101stn_1 101314am via_cell_density":"42.90","c4002214101stn_1 101314am viability_":"94.2","c4002214101stn_1 101314am ecs_via_cell_density":"2.33","c4002214101stn_1 101314am ecs_viability_":"72.6","c4002214101stn_1 101314am current_hpr_rpm":"45.8","c4002214101stn_1 101314am current_hfr":"0.61","c4002214101stn_1 101314am acd":"42.51","c4002214101stn_1 101314am do2_demand_slpm":"4.61","c4002214101stn_1 101314am max_do2_sp_":"50","c4002214101stn_1 101314am macrosparge_slpm":"6.00","c4002214101stn_1 101314am current_antifoam_rpm":"9.9","c4002214101stn_1 101314am max_do2_sp_adjustment":"","c4002214101stn_1 101314am do2_alarm_adjustment":"","c4002214101stn_1 101314am brx_ph_adjustment":"","c4002214101stn_1 101314am harvest_ph_adjustment":"","c4002214101stn_1 101314am hpr_adjustment":"","c4002214101stn_1 101314am macrosparge_adjustment_slpm":"NA","c4002214101stn_1 101314am antifoam_adjustment":"","c4002214101stn_1 101314am cell_bleed":"1.1","c4002214101stn_1 101314am actual_transonic_flow":"0.61","c4002214101stn_1 101314am cell_sp__perf_rate_cspr":"0.10","c4002214101stn_1 101314am comment__fl":"107"}'

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
    except:
        xml += spacer + openingTag + closingTag

xml += '</PageEntry>'

# placeContents(sys.argv[1] + ".xml", xml)

print xml