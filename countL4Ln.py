#!/usr/bin/python3
#
#
# Generate metrics for satisfies and satisfied by links
#
#
# BEFORE RUN:
# Check parameters between ============... at the beginning of
# this script. Change them if they are not correct.
#
#
# 2020/09/17
#
# Daniel Bednarski Ramos
# daniel.bednarski.ramos@gmail.com
#
#
# TO DO
# 1) Read subsection names from csv (it is needed to add "Name"
#    attribute to the view)
#
#

import csv


# ======================================================

# column numbers where the attributes below are found
col = { 'section': 2,
        'gmt_id' : 1,
        'id'     : 0,
        'satisfied_by': 6,
        'satisfies': 5,
        'artifact_type': 4,
        'name': 3
      }

# input and output csv files
file_in="GMT-REQ-00161-M1 Subsystem_L4_20201103.csv"
file_out="GMT-REQ-00161-M1 Subsystem_L4_20201103_out.csv"

# ======================================================


reader = csv.reader(open(file_in, "r"), delimiter=',', quotechar='\"')
writer = csv.writer(open(file_out, "w"))

# Variable that is set when first valid row is read
#init=False

#nsatisfies=0
#nsatisfiedby=0
lines_withlink=[]
lines_withoutlink=[]
n_withlink=0
n_withoutlink=0

# Loop on input rows
for i,row in enumerate(reader):

    # Skip lines which is not concerning a requirement
    # (the first condition is because the last rows of exported view from DOORS)
    if len(row) <= 1 or row[col['artifact_type']] not in ('Subsystem Requirement', 'Lower Level Requirement'):
        print(row)
        print('Skiped row')
        continue

    # Get the current section (this solution is because they are of type #.##.#.#-#)
#    curr_section = row[col['section']].split('.')[0] + '.' + row[col['section']].split('.')[1].split('-')[0]

    # If section number has chenged, it is need to record the data in the output csv and reset 
    # the variables
#    if curr_section != section:

    # Do the process of writing a line in output csv
    #    if init: # and i < 100:
    print("="*30)
#    print('section: ' + str(section))
    print(row)
    req_id = row[col['id']]
    req_name = row[col['name']]
    req_type = row[col['artifact_type']]
#    print(row[col['satisfies']])
    links = row[col['satisfies']].split('\n')

    for j,link in enumerate(links):

        idx1=link.find(' {LINK')

        if idx1 == -1:
            lines_withoutlink += [[req_id, req_name, req_type, '', '']]
            n_withoutlink+=1

        else:
            idx2 = link.find(':')
            link_id = link[0:idx2]
            link_name = link[idx2+2:idx1]
            idx3 = link_id.find('.')
            print(link_id)
            print(link_name)
            if idx3 != -1:
#                print('**********************'*40)
#                print(idx3)
                module_id = link[0:idx3]
                link_id = link_id[idx3+1:idx2]
#                print(link_id)
            if j == 0:
                n_withlink+=1
                lines_withlink+=[[req_id, req_name, req_type, link_id, link_name]]
            else:
                lines_withlink+=[['', '', '', link_id, link_name]]
 
    print(req_id)
    print(req_name)
#    print("WITH LINK")
#    print(lines_withlink)
#    print(n_withlink)
#    print("WITHOUT LINK")
#    print(lines_withoutlink)
#    print(n_withoutlink)
   
    print("-"*50)


writer.writerow(['','M1 SYSTEM (L4) REQUIREMENTS AND SATISFIES LINKS','','',''])
writer.writerow(['','','','',''])
writer.writerow(['###', 'Reqs without satisfies link (TOTAL NUMBER: {})'.format(n_withoutlink),'','',''])
writer.writerow(['ID', 'Name', 'Req Type', '',''])
writer.writerows(lines_withoutlink)
writer.writerow(['','','','',''])
writer.writerow(['###', 'Reqs with satisfies link (TOTAL NUMBER: {})'.format(n_withlink),'','',''])
writer.writerow(['ID', 'Name', 'Req Type', 'Satisfies (ID)', 'Satisfies (Name)'])
writer.writerows(lines_withlink)

# print and record the last row to the output csv
