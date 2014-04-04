import sys

STDIN=open('General.txt','r')
#STDIN = sys.stdin

invalid_lines = ["DEPARTMENT OF TECHNICAL EDUCATION : CHENNAI 600025", \
"ADMISSION TO FIRST YEAR B.E. / B.TECH.  DEGREE COURSES",\
"GENERAL SEAT MATRIX INCLUDED IN ANNA UNIVERSITY SINGLE WINDOW COUNSELLING - 20 !",\
"COLLEGE ",\
"CODE",\
"NAME OF INSTITUTION",\
"BR ",\
"CODE",\
"SANCTIO",\
"NED ",\
"INTAKE  SEATS",\
"2013-14",\
"GQ ",\
"MGT ",\
"SURREN TOTAL ",\
"DER ",\
"SEATS"]

invalid_words = [ 'page ', "from 222"] 

valid_br_code = ['MT','IC','BT','PR','EM','CS','EC','CE','IT','MC','ME','AE', 'EI', 'MF', 'EE', 'CH', 'FT', 'BM', 'TX', 'AU', 'ML']  

def is_number(n):
  try:
    float(n)
    #print n, "is a number!"
    return True
  except:
    #print n, "is NOT a number!"
    return False

def no_invalid_words(myl):
  for e in invalid_words:
    if myl.find(e) != -1:
      return False
  return True
  
def is_college_line(myl):
  # print "Valid c_line?", myl not in invalid_lines and no_invalid_words(myl) and not is_br_line(myl)
  return myl not in invalid_lines and no_invalid_words(myl)

def is_br_line(myl):
  llist = myl.split()
  val = llist[0] in valid_br_code and len(llist) >= 4
  if val:
	  print "valid br_line", myl
  return val

def check_for_numbers(nl):
    res = True
    for i in nl:
        res = res and is_number(i)
    return res
    
def check_for_br_code(b):
  return b != None and not is_number(b) and (len(b) == 2) and (b == b.upper())

def is_valid_ccode(line):
  return len(line) == 4 and (is_number(line) or line[:3] == "NEW")

def process_br_details(d, c=None):
  llist = d
  #print "process_br_details", llist
  
  if llist[0] in valid_br_code:
    c_br_info = {}
    c_br_info['br_code'] =  llist[0]
    c_br_info['in2013'] = int(llist[1])
    c_br_info['GQ'] = int(llist[2])
    if len(llist) == 5:
      c_br_info['MQ_surrender'] = int(llist[3])
      c_br_info['total'] = int(llist[-1])
      c_br_info['avail_for_counsel'] = c_br_info['total']
  else:
    print "*** Invalid branch_code", llist[0]
    return None
  return c_br_info

# checks the line for the pattern "XX NN NN NN NN" or "XX NN NN NN" at the end of the line
# if yes, then the line contains branch information, and returns the relevant branch information as a list
# otherwise, returns None
# e.g. contains_br_info("ashok bakthava SS 33 23 23") -> ['SS', '33', '23', '23']
# e.g. contains_br_info("BR 23 23 23") -> ['BR', '23', '23', '23']
# e.g. contains_br_info("BR 23 we 23") -> None

def contains_br_info(line):
  global mute
  line = line.strip().split()
  num_Elements = len(line)
  
  fourth_from_last, fifth_from_last = None, None
  
  if num_Elements >= 5:
    fifth_from_last = line[-5]
  if num_Elements >= 4:
    fourth_from_last = line [-4]
  
  potential_br_code = check_for_br_code(fourth_from_last)
  if potential_br_code:
    potential_br_code = check_for_numbers(line[-3:-1])
    # print "p_br_code 4", potential_br_code
    if potential_br_code:
        if fourth_from_last not in valid_br_code:
          if not mute: 
            print "*** Potential new branch code, adding to valid_br_codes", fourth_from_last
          valid_br_code.append(fourth_from_last)
        return " ".join(line[-4:])
    else:
        return None
  
  potential_br_code = check_for_br_code(fifth_from_last)
  if potential_br_code:
    potential_br_code = check_for_numbers(line[-4:-1])
    if potential_br_code:
      # print "p_br_code 5", potential_br_code
      if fifth_from_last not in valid_br_code:
        if not mute:
          print "*** Potential new branch code, adding to valid_br_codes", fifth_from_last
        valid_br_code.append(fifth_from_last)
      return " ".join(line [-5:])
    else:
      return None
  return None
  
# returns back a dictionary element containing the college data arriving on the stdin
# otherwise, returns False if nothing valid is available anymore

def process_c_info(cl):
  c_code, c_name, c_address  = None, None, None
  mangled = False
  c_lines = ""
    
  for i, line in enumerate(cl.split("\n")):
    lline = line.strip().split()
    if not len(lline):
      continue
    
    #if len(lline) <= 1:
    c_lines = c_lines + line + " "
  
    first = lline[0]
    if not c_code:
      if len(lline) != 1:
        mangled = True
      if is_valid_ccode(first):
        c_code = first
      
  if len(cl.split("\n")) == 1:
    c_lines  = cl.split("\n")
  
  c_lines = c_lines.strip('\t\n')
  space = c_lines.find(" ")
  comma = c_lines.find(",", space+1)
  c_name, c_address = c_lines[space+1:comma], c_lines[comma+2:]
  
  try:
    if c_code and not mangled: 
      c_data = {'c_code':c_code, 'c_name':c_name, 'c_address':c_address}
    elif c_code: 
      c_data = {'c_code':c_code}
    #print "*** College_data for {0} retrieved for BR {1}".format( c_data['c_code'], c_br_info['br_code'])
    return c_data, mangled
  except:
      #print "*** Error reading college info data", cl
      # Should never come here. Need to fix this...!
      pass
  
  return None, None

  
def read_college_data():
  c_data, c_br_info, mangled = None, None, False
  c_info_list = ""
  
  i = 0
  while True:
    line = STDIN.readline()
    i += 1
    #print "Line read", line
    if len(line):
      info = contains_br_info(line)
      #print "read_college_data2::info: ", info
      if info:
        c_br_info = process_br_details(info.split())
        if i == 1 or i == 2:
          c_info_list += line
          #c_info_list
        break
      else:
        c_info_list += line
    else:
      break
   
    
  if c_info_list != "":
    #print "read_college_data2:", c_info_list
    c_data, mangled = process_c_info(c_info_list)
  
  if not c_data or not c_br_info:
    #print "*** Error getting college data"
    pass
  return c_data, c_br_info, mangled
  

###########################################
#
# main program starts here
#
#
############################################  
db = {}
count = 0
mcount = 0
ccount = 0

# Change this to False if you want to print various diagnostic messages
mute = True

while True:

  cdata, br_info, mangled = read_college_data()
  if not cdata:
    break
    
  c_code = cdata['c_code']
  br_code = br_info['br_code']
  #print "MAIN: c_code, br_code", c_code, br_code
  
  if c_code not in db:
    db[c_code] = {}
    db[c_code]['br_info'] = [br_info]
    if not mangled:
      db[c_code]['c_name'] = cdata['c_name']
      db[c_code]['address'] = cdata['c_address']
      if not mute:
        print "***** New entry for {0} with branch {1}".format(cdata['c_name'], br_code)
    else:
      if not mute:
        print "***** New mangled entry for {0} with branch {1}".format(c_code, br_code)
      mcount += 1
    ccount += 1
  else:
    db[c_code]['br_info'].append(br_info)
    if not mute: 
      print "***** Entry appended for {0} with branch {1}".format(c_code, br_code)
    if 'c_name' not in db[c_code]:
      if not mangled:
        db[c_code]['c_name'] = cdata['c_name']
        db[c_code]['address'] = cdata['c_address']
        if not mute: 
          print "***** Updated for {0} with branch {1}".format(cdata['c_name'], br_code)
      else:
        #print "*** Incomplete DB entry for ", c_code
        mcount += 1
  count += 1 
  
print "Total: {0} colleges, read {1}({2} mangled) branch entries into DB successfully".format(ccount, count, mcount)
print "Total number of branch types:", len(valid_br_code), sorted(valid_br_code)
  
# Calculate some statistics and reporting based on Surrenders
# and Surrender percentages

def college_details(id):
  print db[id]
  if id in db:
    for e in db[id]:
      if e == "br_info":
		    for b in db[id][e]:
		      print b
      else:
        print e, db[id][e]
    #return db[id]
	return True
  
  else:
    print "ID: ", id, "not found in DB"
    return False


def calculate_and_rank(mute=True):
  max = 0
  maxc = 0
  
  for c in db:
    surrendered = 0
    total = 0
    gq = 0
    css, cst, cgq = 0,0,0
    
    for i in db[c]['br_info']:  
      total += i['in2013']
      gq += i['GQ']
      if 'MQ_surrender' in i:
        surrendered += i['MQ_surrender']
        if i['br_code'] in ['CS', 'IT', 'EC']:
          css += i['MQ_surrender']
          cst += i['in2013']
          cgq += i['GQ']
    
    # store the number of management seats in Circuit branches
    db[c]['cmq'] = cst-cgq
    
    # store the 'mqp' - management quota surrender percentage
    if (total-gq):
      db[c]['mqp'] = 100.0*surrendered/(total - gq)
      if db[c]['mqp'] >= max and not mute:
        print "New max found at", c, max
        max = db[c]['mqp']
    # store the 'mqc' - mgmt circuit seats surrender percentage
    if (cst-cgq):
      db[c]['mqc'] = 100.0* css/(cst-cgq)
      if db[c]['mqc'] >= max and not mute:
        print "New max_c found at", c, maxc
        maxc = db[c]['mqc']
  

def fetch_city(dn):
  surrendered = 0
  total = 0
  gq = 0
  css, cst, cgq = 0, 0, 0
  for c in db:
    if 'address' in db[c]: 
      address = db[c]['address']
    else:
      print "ERROR*** No address for", c
      continue
    if address.find(dn) != -1:
      for i in db[c]['br_info']:
        total += i['in2013']
        gq += i['GQ']
        if 'MQ_surrender' in i:
          #print c, dn, i['MQ_surrender'], i['in2013']
          surrendered += i['MQ_surrender']
          if i['br_code'] in ['CS', 'IT', 'EC']:
          #print c, dn, i['br_code'], i['MQ_surrender'], i['in2013']-i['GQ']
            css += i['MQ_surrender']
            cst += i['in2013']
            cgq += i['GQ']
  
  ###################################
  #  Print  the values that have been calculated
  ###################################
  if len(dn.strip()) == 0:
    dn = "ALL"
  mqsp = 100.0*surrendered/(total -gq)
  print dn.ljust(12), "GRAND".rjust(7), " --- %6i %8i %8i" % (surrendered, total-gq, total), str("%3.1f" % mqsp).rjust(5)
  mqc = 100.0*css/(cst -cgq)
  print dn.ljust(12), "CSE-L".rjust(7), " --- %6i %8i %8i" % (css, cst-cgq, cst), str("%3.1f" % mqc).rjust(5) 

	
print "DISTRICT                Surrender     MQ     Total MQSP"
print "---------"

fetch_city("Chennai")
fetch_city("Kancheepuram")
fetch_city("Coimbatore")
fetch_city("Salem")
fetch_city("Erode")
fetch_city("Sivagangai")
fetch_city("Namakkal")
fetch_city("Madurai")
fetch_city("Tirunelveli")
fetch_city("District")
fetch_city(" ")
print "----------" 

  
def fetch_college(cn, mute=0):
  for c in db:
    #print "c", c, type(c)
    if db[c]['c_name'].find(cn) != -1:
      surrendered = 0
      total = 0
      gq = 0
      css, cst, cgq = 0, 0, 0
      for i in db[c]['br_info']:
        total += i['in2013']
        gq += i['GQ']
        
        if 'MQ_surrender' in i:
        
          surrendered += i['MQ_surrender']
        
          if 'CS' in i['br_code'] or 'IT' in i['br_code'] or 'EC' in i['br_code']:
            #print c, cn, i['br_code'], i['MQ_surrender'], i['in2013']- i['GQ']
            css += i['MQ_surrender']
            cst += i['in2013']
            cgq += i['GQ']
      
      if 'mqp' in db[c]:
        if not mute: print cn[:15].ljust(17), "GRAND".rjust(5), "-- %4i %6i %6i" % (surrendered, total-gq, total), str("%3.1f" % db[c]['mqp']).rjust(5)

      if 'mqc' in db[c]:
        if not mute: print cn[:15].ljust(17), "CSE-L".rjust(5), "-- %4i %6i %6i" % (css, cst-cgq, cst), str("%3.1f" % db[c]['mqc']).rjust(5)
      
      if 'mqp' and 'mqc' in db[c]:
        store_in_cache(c, db[c]['c_name'], surrendered, db[c]['mqp'], db[c]['mqc'])
        return c, surrendered, db[c]['mqp'], db[c]['mqc']
      else:
        store_in_cache(c, db[c]['c_name'], surrendered)
        return c, surrendered
      
  return None


calculate_and_rank()

cache = None 

def store_in_cache(c,n,s,mqp=0, mqc=0):
  global cache
  
  if not cache:
    
    #cache[c]['surrender'] = s
    #cache[c]['mqp'] = mqp
    #cache[c]['mqc'] = mqc
    cache = [(c, n, s, mqp, mqc)]
  else:
    cache.append((c, n, s, mqp, mqc))
  
"""
Sort tuples by term frequency, and then alphabetically.
"""
def tuple_sort (a, b):
  
  if a[3] < b[3]:
    return 1
  elif a[3] > b[3]:
    return -1
  else:
    return cmp(a[1], b[1])

def sort_and_print_cache():
  cache.sort(tuple_sort)
  print 
  print"---------- SORTED COLLEGE INFO (above) based on Surrender %"
  print"  ID           COLLEGE     SURR  SP   CP"
  for stuple in cache:
    if stuple[2]:
      print stuple[0], stuple[1][:21].ljust(12), "%4i" % stuple[2], str("%3.1f" % stuple[3]).rjust(5), str("%3.1f" % stuple[4]).rjust(5)

print"COLLEGE WISE           Surrender    MQ  total MQSP"
print"----------"
fetch_college("KGISL")
fetch_college("PSG")
fetch_college("Sona")
fetch_college("Sri Sairam Enginering")
fetch_college("Rajalakshmi")
fetch_college("R M K")
fetch_college("S K P")
fetch_college("Bannari")
fetch_college("Kumaraguru")
fetch_college("Chettinad")
fetch_college("Muthayammal")
fetch_college("Park College")
fetch_college("Tamilnadu College")
fetch_college("Sri Shakthi Institute")
fetch_college("Adithya ")
fetch_college("INFO ")
fetch_college("K P R")
fetch_college("Sriguru")
fetch_college("Kalaignar")
fetch_college("Kathir")
fetch_college("Sri Eshwar")
fetch_college("Dr. Mahalingam")
fetch_college("Sri Krishna College of Enginering and Technology")
fetch_college("Sri Krishna College of Technology")
fetch_college("VLB ")
fetch_college("Jansons ")
fetch_college("C M S College of Engineering and Technology")
fetch_college("P P G ")
fetch_college("Suguna ")
fetch_college("S N S College")
fetch_college("S N S College of Tech")
fetch_college("Ramakrishna Institute")
fetch_college("Sri Ramakrishna Engineering")

sort_and_print_cache()



def read_college_data_backup():
  c_data, c_br_info = None, None
  
  # Need flags to anticipate mangled data
  # For example, 
  #   - 1131 Vel Tech, Avadi-Alamathi Road, Chennai 600062 CE 60 30 0 30
  #   Theni Kammavar Sangam College of Technology, 
  #   - 5988 Theni Main Road, Koduvillarpatti Post, 
  #   Theni District 625534
  one_line_data, mangled = False, False
  
  # look for a 4 digit college code as the beginning of a data packet
  while True:
    line = STDIN.readline()
    #print "Line read", line
    if len(line):
      # print "length of line", len(line)
      line = line.strip()
      if is_valid_ccode(line):
        c_code = line
        #print "College code secured:", c_code
        break
      elif len(line) >= 1:
        line = line.split()
        val = line[0]
        if len(val) == 4 and is_number(val):
          c_code = val
          mangled = True
          #print "*** Mangled data. Assuming college_code:", c_code, line
          c_br_info = process_br_details(line[-5:], c_code)
          if c_br_info:
            one_line_data = True
            #print "*** Mangled branch data. Assuming branch info:", c_code, c_br_info
          break
      elif len(line.strip()) != 0:
        print "*** Expecting 4 digit College-ID. Read:", line
        print "*** Ignoring line, going onto next line..."
		    # pass
    else:
      break
  
  
  # Now, read the next 2 or 3 lines for name of college and address, only if the data is properly formed
  if not one_line_data: 
    line, br_info = get_valid_college_lines(None, mangled)
		
    if mangled:
      pass
      #print "Line", line.strip()
      #print "br_info", br_info.strip()
    
    if line and br_info:
      #print "Line read", line,
      if len(line):
        line = line.strip('\t\n')
        comma = line.find(",")
        c_name, c_address = line[:comma], line[comma+1:]
        #print "College name secured:", c_name
        #print "College address secured:", c_address
    
      # line 3
      c_br_info = process_br_details(br_info.split(), c_code)
      if c_br_info == None:
        print "Error in reading branch details for", c_code, c_name
      else: 
        pass
        #print "College branch secured:", c_br_info
  
  # consolidate all the data read into one structure
  # If data is mangled, just take college code and branch info
  try:
    if not mangled: 
      c_data = {'c_code':c_code, 'c_name':c_name, 'c_address':c_address}
    else: 
      c_data = {'c_code':c_code}
      #print "*** College_data for {0} retrieved for BR {1}".format( c_data['c_code'], c_br_info['br_code'])
  except:
    if line:
      print "*** Error reading data", c_data, c_br_info, mangled
    # Otherwise, reached end of file
    #  and c_data, c_br_info, mangled = None, False, False
  return c_data, c_br_info, mangled
