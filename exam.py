from Bio import SeqIO
import sys
import re

if len(sys.argv) == 2:
	file_name = sys.argv[1]
else:
	file_name = 'dna.example.fasta'

print 'File name: [%s]' % file_name

records = list(SeqIO.parse(file_name, 'fasta'))

records.sort(key = lambda record : len(record))

print 'There are [%d] records in the file.' % len(records)

def get_orfs(dna):
        candidates = []
        start = 0
        while (dna.find('ATG', start) > -1):
                start = dna.find('ATG', start)
                candidates.append(' '.join(re.findall('...', dna[start:])))
                start += 1

        matches = []

        for candidate in candidates:
		for terminator in ['TAA', 'TAG', 'TGA']:
                        end = 1;
                        while(candidate[3:].find(terminator, end) > -1):
                                end = candidate.find(terminator, end)
                                matches.append(candidate[:end+3].replace(" ", ""))
                                end += 1
        return matches

with open('all_dna.txt', 'w') as f:
	for record in records:
		print
		print 'The length of [%s] is [%d].' % (record.id, len(record.seq))
		for orf in get_orfs(str(record.seq)):
			print "Length: %d, Start: %d, Sequence: %s" % (len(orf), str(record.seq).find(orf), orf)
		f.write(str(record.seq) + "\n")
