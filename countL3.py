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
col = { 'section': 0,
        'gmt_id' : 1,
        'satisfied_by': 5,
        'satisfies': 6
      }

# input and output csv files
file_in="oad.csv"
file_out="oad_metrics.csv"

# ======================================================


reader = csv.reader(open(file_in, "r"), delimiter=',', quotechar='\"')
writer = csv.writer(open(file_out, "w"))
section=""

# Variable that is set when first valid row is read
init=False

# Print the header of output csv
writer.writerow(['section', '# of reqs', '# of reqs containing satisfies links', '# of reqs containing satisfied by links',
       '# of reqs solely with satisfies links', '# of reqs solely with satisfied by links',
       '# of reqs with both satisfies and satisfied by links',
       '# of reqs with no one link', 'total # of satisfies links', 'total # of satisfied by links'])

# Loop on input rows
for i,row in enumerate(reader):

    # Skip lines which is not concerning a requirement
    # (the first condition is because the last rows of exported view from DOORS)
    if len(row) <= 1 or row[col['gmt_id']][0:3] != 'REQ':
        print('Skiped row')
        continue

    # Get the current section (this solution is because they are of type #.##.#.#-#)
    curr_section = row[col['section']].split('.')[0] + '.' + row[col['section']].split('.')[1].split('-')[0]

    # If section number has chenged, it is need to record the data in the output csv and reset 
    # the variables
    if curr_section != section:

    # Do the process of writing a line in output csv
        if init: # and i < 100:
            print("="*30)
            print('section: ' + str(section))
            print('# of reqs: ' + str(nreq))
            print('# of req with satisfies links: ' + str(nreq_only_satisfies + nreq_both_satisfy))
            print('# of req with satisfied by links: ' + str(nreq_only_satisfied + nreq_both_satisfy))   
            print('-'*30)     
            print('# of req solely with satisfies links: ' + str(nreq_only_satisfies))
            print('# of req solely with satisfied by links: ' + str(nreq_only_satisfied))
            print('# of req with both satisfies and satisfied by links: ' + str(nreq_both_satisfy))
            print('# of req with no one links: ' + str(nreq - nreq_only_satisfies - nreq_only_satisfied - nreq_both_satisfy))
            print('-'*30)     
            print('total # of satisfies links: ' + str(total_satisfies))
            print('total # of satisfied by links: ' + str(total_satisfied))
            print("="*30)
            writer.writerow([section, nreq, nreq_only_satisfies + nreq_both_satisfy,
                nreq_only_satisfied + nreq_both_satisfy, nreq_only_satisfies,
                nreq_only_satisfied, nreq_both_satisfy, nreq - nreq_only_satisfies - nreq_only_satisfied - nreq_both_satisfy, total_satisfies, total_satisfied])
        
        section = curr_section
        print('New section: ' + str(section))

        total_satisfies=0           # variable for total satisfies links inside a section
        total_satisfied=0           # variable for total satisfied by links inside a section
        nreq_only_satisfies=0       # variable for the number of req in section with solely satisfies links
        nreq_only_satisfied=0       # variable for the number of req in section with solely satisfied by links
        nreq_both_satisfy=0         # variable for the number of req in section with both links
        nreq=0                      # variable for total number of req in section
        init=True


    nreq+=1
    if row[col['satisfied_by']].split('\n') != ['']:
        links_satisfied=len(row[col['satisfied_by']].split('\n'))
    else:
        links_satisfied=0
        
    if row[col['satisfies']].split('\n') != ['']:
        links_satisfies=len(row[col['satisfies']].split('\n'))
    else:
        links_satisfies=0

    if links_satisfied != 0 and links_satisfies != 0:
        nreq_both_satisfy+=1
    elif links_satisfied != 0:
        nreq_only_satisfied+=1
    elif links_satisfies != 0:
        nreq_only_satisfies+=1
    
    total_satisfied+=links_satisfied
    total_satisfies+=links_satisfies

    # Lines below are justa verbose for checking satisfied by links computation
    print(section)
    print(row[col['satisfied_by']])
    print(links_satisfied)
    print(total_satisfied)
    print("-"*30)
#    writer.writerow(row)


# print and record the last row to the output csv
print("="*30)
print('section: ' + str(section))
print('# of reqs: ' + str(nreq))
print('# of req with satisfies links: ' + str(nreq_only_satisfies + nreq_both_satisfy))
print('# of req with satisfied by links: ' + str(nreq_only_satisfied + nreq_both_satisfy))   
print('-'*30)     
print('# of req solely with satisfies links: ' + str(nreq_only_satisfies))
print('# of req solely with satisfied by links: ' + str(nreq_only_satisfied))
print('# of req with both satisfies and satisfied by links: ' + str(nreq_both_satisfy))
print('# of req with no one links: ' + str(nreq - nreq_only_satisfies - nreq_only_satisfied - nreq_both_satisfy))
print('-'*30)     
print('total # of satisfies links: ' + str(total_satisfies))
print('total # of satisfied by links: ' + str(total_satisfied))
print("="*30)
writer.writerow([section, nreq, nreq_only_satisfies + nreq_both_satisfy,
    nreq_only_satisfied + nreq_both_satisfy, nreq_only_satisfies,
    nreq_only_satisfied, nreq_both_satisfy, nreq - nreq_only_satisfies - nreq_only_satisfied - nreq_both_satisfy, total_satisfies, total_satisfied])

