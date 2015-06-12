#!/usr/bin/env python
"""Fetch GenBank entries for given accessions. 

Adapted from https://www.biostars.org/p/66921/

USAGE:
cat <file> | python acc2gb.py <email> > <output>

or

python acc2gb.py <email> <file>

(this is easier for debugging)

where:
<file> is the name of a file containing accession numbers to download
<email> is the email address associated with your NCBI account
<output> is the name of the file you'd like to write the results to

DEPENDENCIES:
Biopython
"""

import sys
from Bio import Entrez,SeqIO
import pprint
import re

#define email for entrez login
db           = "nuccore"
Entrez.email = sys.argv[1]

#get accession numbers out of stdin
if sys.argv[2] :
    accs = [line.rstrip('\n') for line in open(sys.argv[2])]
else :
    accs = [ l.strip() for l in sys.stdin if l.strip() ]


#fetch
sys.stderr.write( "Fetching %s entries from GenBank: %s\n" % (len(accs), ", ".join(accs[:10])))
                  
pp = pprint.PrettyPrinter(indent=4)

for i,acc in enumerate(accs):
  try:
    sys.stderr.write( " %9i %s          \r" % (i+1,acc))  
    handle = Entrez.efetch(db=db, rettype="gbwithparts", id=acc)
    for record in SeqIO.parse(handle,"gb"):
        print "Name %s, %i features" % (record.name, len(record.features))
        for f in record.features:
            if f.type == 'CDS' and f.qualifiers['product']:
                    cas = re.search("(Cas3|Cas10|Cas9)", f.qualifiers['product'][0] )
                    if cas and cas.group(0): 
                        print "Location %s Product %s" % (f.location, f.qualifiers['product'])
            
    handle.close()

  except:
    sys.stderr.write( "Error! Cannot fetch: %s        \n" % acc) 

    
