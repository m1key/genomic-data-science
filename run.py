from Bio.Blast import NCBIWWW
fasta_string = open("sequence.fa").read()
result_handle = NCBIWWW.qblast("blastn", "nt", fasta_string)

from Bio.Blast import NCBIXML
blast_record = NCBIXML.read(result_handle)

for alignment in blast_record.alignments:
	for hsp in alignment.hsps:
		if hsp.expect >= 0.00000000000005: continue
		
		print('****Alignment****')
		print ( 'sequence:' , alignment.title )
		print ( 'length:' , alignment.length )
		print ('e value:',format(hsp.expect, '.100f')     )
		print ( hsp.query )
		print ( hsp.match )
		print ( hsp.sbjct ) #from Bio.Seq import Seq

