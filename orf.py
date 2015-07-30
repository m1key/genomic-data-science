import re
dna = "ATGCCCTAG"

def get_orfs(dna):
	candidates = []
	start = 0
	while (dna.find('ATG', start) > -1):
		start = dna.find('ATG', start)
		print start
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

print get_orfs(dna)
print
print get_orfs("AATGCCCTAG")
print
print get_orfs("CTATGCCCTAG")
print
print get_orfs("CTATGCCCTAGAAAAAATGA")
print
print get_orfs("CTATGCCCATAGAAAAAATGA")
print
for orf in get_orfs("CTATGCCCTAGAAAAAATGA"):
	print "%d - %s" % (len(orf), orf)
