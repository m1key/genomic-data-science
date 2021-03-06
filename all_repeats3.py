import re

class DnaRepeat:
	def __init__(self, repeat_string, start_indeces):
		self.repeat_string = repeat_string
		self.start_indeces = start_indeces
	def __eq__(self, other):
		return self.repeat_string == other.repeat_string and self.start_indeces.sort() == other.start_indeces.sort()
	def __repr__(self):
		return "DnaRepeat('%s', %s)" % (self.repeat_string, self.start_indeces)
	__str__ = __repr__
	def __hash__(self):
		return hash(self.repeat_string)

assert DnaRepeat("abc", [10]) == DnaRepeat("abc", [10])
assert DnaRepeat("abc", [10]) != DnaRepeat("abc", [11])
assert DnaRepeat("abc", [10]) != DnaRepeat("abd", [10])
assert DnaRepeat("abc", [10, 15]) == DnaRepeat("abc", [10, 15])
assert DnaRepeat("abc", [10, 15]) != DnaRepeat("abc", [10, 16])
a_repeat = DnaRepeat("acgtgact", [10, 14, 19])
assert eval(str(a_repeat)) == a_repeat
assert DnaRepeat("cagt", [20, 30]) == DnaRepeat("cagt", [30, 20])

class DnaSequenceRepeats:
	NUCLEOBASES = ['A', 'C', 'G', 'T']

	def __init__(self, dna_sequence):
		self.dna_sequence = dna_sequence
	
	def find_repeats(self, repeat_length):
		nucleobase_repeats = self._find_nucleobase_repeats()
		return self._find_complex_repeats(repeat_length, nucleobase_repeats)

	def _find_nucleobase_repeats(self):
		"""Finds repeats for single (one-character) nucleobases."""
		nucleobase_repeats = []
        	for nucleobase in self.NUCLEOBASES:
			# Find occurrences of nucleobases:
                	start_indeces = [match.start() for match in re.finditer(nucleobase, self.dna_sequence)]
			# If this nucleobase has more than one occurrence, it is itself a repeat of length 1:
			if len(start_indeces) > 1:
				nucleobase_repeats.append(DnaRepeat(nucleobase, start_indeces))
		return nucleobase_repeats
	
	def _find_complex_repeats(self, repeat_length, repeat_candidates):
		"""Finds repeats for complex (multiple-character) sequences.
		
		Args:
			repeat_length (int): Final repeat length to find.
			repeat_candidates (List[DnaRepeat]): potential repeat candidates of
				length <= repeat_length.
		"""
		# If nothing found or we have already reached target length, return:
		if not repeat_candidates or len(repeat_candidates[0].repeat_string) == repeat_length:
			return repeat_candidates
		
		# This array will hold repeat candidates found in this iteration, so 1 character longer than the given ones.
		all_longer_repeat_candidates = []
		for repeat_candidate in repeat_candidates:
			# This array will hold repeat candidates based on the current repeat candidate.
			longer_repeat_candidates_for_this_repeat_candidate = []
			for nucleobase in self.NUCLEOBASES:
				longer_repeat_candidate_string = repeat_candidate.repeat_string + nucleobase
				start_indeces = []
				for start_position in repeat_candidate.start_indeces:
					if self.dna_sequence[start_position:start_position + len(longer_repeat_candidate_string)] == longer_repeat_candidate_string:
						start_indeces.append(start_position)
				# If this longer repeat candidate repeats more than once:
				if len(start_indeces) > 1:
					longer_repeat_candidates_for_this_repeat_candidate.append(DnaRepeat(longer_repeat_candidate_string, start_indeces))
			# Now use the longer candidates to find even longer candidates.
			all_longer_repeat_candidates.extend(self._find_complex_repeats(repeat_length, longer_repeat_candidates_for_this_repeat_candidate))

		return all_longer_repeat_candidates


def find_by_repeat(repeats, repeat_string, unique = False):
	all_finds = [find for find in repeats if find.repeat_string == repeat_string]
	if unique:
		contains_one(repeats, repeat_string)
		return all_finds[0]
	else:
		return all_finds
def contains(repeats, repeat, times):
	assert len(find_by_repeat(repeats, repeat)) == times
def contains_one(repeats, repeat):
	contains(repeats, repeat, 1)
def contains_zero(repeats, repeat):
	contains(repeats, repeat, 0)
def has_start_indeces(repeats, repeat, start_position_count):
	assert len(find_by_repeat(repeats, repeat, unique = True).start_indeces) == start_position_count
def has_no_start_indeces(repeats, repeat):
	assert len(find_by_repeat(repeats, repeat)) == 0
def has_repeats_with_x_start_indeces(repeats, start_indeces_count, count):
	assert len([find for find in repeats if len(find.start_indeces) == start_indeces_count]) == count
def has_start_indeces_at(repeats, repeat, start_indeces):
	assert find_by_repeat(repeats, repeat, unique = True).start_indeces == start_indeces

def finds(x): return len(x.start_indeces)

with open("all_dna.txt") as f:
	dna_sequence_repeats = DnaSequenceRepeats(f.read())
	
	repeats_12 = dna_sequence_repeats.find_repeats(12)
	contains_one(repeats_12, "AAAACGGCACCT") # Occurs twice in the dna.
	contains_zero(repeats_12, "AAAACGGCTCGG") # Occurs once in the dna, so not a repeat.
	contains_zero(repeats_12, "AAAACGGCTTAC") # Does not occur in the dna.
	contains_one(repeats_12, "GCTGCTCGACGC") # Occurs three times in the dna.
	has_start_indeces(repeats_12, "AAAACGGCACCT", 2)
	has_start_indeces(repeats_12, "GCTGCTCGACGC", 3)
	has_start_indeces(repeats_12, "GTATCCCCGAAG", 2)
	has_start_indeces(repeats_12, "CGCGGCGGCCGG", 3)
	has_start_indeces(repeats_12, "CGCGCGGCGGCC", 4)
	has_start_indeces_at(repeats_12, "TCGCGACACGTG", [10822, 39880])
	has_start_indeces_at(repeats_12, "GCGATCGGCGCG", [8850, 12155, 44391])
	has_start_indeces_at(repeats_12, "TCGTCGGCGCCG", [433, 44449, 47459, 48999])
	assert len(repeats_12) == len(set(repeats_12))
	assert len(repeats_12) == 974
	has_repeats_with_x_start_indeces(repeats_12, 3, 36)
	has_repeats_with_x_start_indeces(repeats_12, 2, 935)
	has_repeats_with_x_start_indeces(repeats_12, 4, 3)
	max_occurrences = max(map(finds, repeats_12))
	assert max_occurrences == 4
	
	repeats_1 = dna_sequence_repeats.find_repeats(1)
	assert len(repeats_1) == len(set(repeats_1))
	assert len(repeats_1) == 4
	contains_one(repeats_1, "A")	
	contains_one(repeats_1, "C")
	contains_one(repeats_1, "G")
	contains_one(repeats_1, "T")
	has_start_indeces(repeats_1, "A", 8399)
	has_no_start_indeces(repeats_1, "B")
	has_start_indeces(repeats_1, "C", 16294)
	has_start_indeces(repeats_1, "G", 16569)
	has_start_indeces(repeats_1, "T", 8600)

	print "All assertions passed."

