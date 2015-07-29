from Bio import SeqIO
import sys

if len(sys.argv) == 2:
	file_name = sys.argv[1]
else:
	file_name = 'dna.example.fasta'

print 'File name: [%s]' % file_name

records = list(SeqIO.parse(file_name, 'fasta'))

records.sort(key = lambda record : len(record))

print 'There are [%d] records in the file.' % len(records)

for record in records:
	print 'The length of [%s] is [%d].' % (record.id, len(record))
