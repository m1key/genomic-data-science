import re

class DnaRepeat:
	def __init__(self, repeat, start_indeces):
		self.repeat = repeat
		self.start_indeces = start_indeces
	def __eq__(self, other):
		return self.repeat == other.repeat and self.start_indeces.sort() == other.start_indeces.sort()
	def __repr__(self):
		return "DnaRepeat('%s', %s)" % (self.repeat, self.start_indeces)
	__str__ = __repr__
	def __hash__(self):
		return hash(self.repeat)

assert DnaRepeat("abc", [10]) == DnaRepeat("abc", [10])
assert DnaRepeat("abc", [10]) != DnaRepeat("abc", [11])
assert DnaRepeat("abc", [10]) != DnaRepeat("abd", [10])
assert DnaRepeat("abc", [10, 15]) == DnaRepeat("abc", [10, 15])
assert DnaRepeat("abc", [10, 15]) != DnaRepeat("abc", [10, 16])
a_find = DnaRepeat("acgtgact", [10, 14, 19])
assert eval(str(a_find)) == a_find
assert DnaRepeat("cagt", [20, 30]) == DnaRepeat("cagt", [30, 20])

class DnaSequenceRepeats:
	NUCLEOBASES = ['A', 'C', 'G', 'T']

	def __init__(self, dna_sequence):
		self.dna_sequence = dna_sequence
	
	def find_repeats(self, repeat_size):
		initial_repeats = self._find_initial_repeats()
		return self._find_subsequent_repeats(repeat_size, initial_repeats)

	def _find_initial_repeats(self):
		initial_repeats = []
        	for nucleobase in self.NUCLEOBASES:
			# Find occurrences of nucleobases:
                	start_indeces = [match.start() for match in re.finditer(nucleobase, self.dna_sequence)]
			# If this nucleobase has more than one occurrence, it is itself a repeat of length 1:
			if len(start_indeces) > 1:
				initial_repeats.append(DnaRepeat(nucleobase, start_indeces))
		return initial_repeats
	
	def _find_subsequent_repeats(self, target, repeats):
		all_candidates = []
		if not repeats or len(repeats[0].repeat) == target:
			return repeats
		for repeat in repeats:
			candidates = []
			for nucleobase in self.NUCLEOBASES:
				candidate = repeat.repeat + nucleobase
				candidate_length = len(candidate)
				matched = []
				for start_position in repeat.start_indeces:
					if self.dna_sequence[start_position:start_position + candidate_length] == candidate:
						matched.append(start_position)
				if len(matched) > 1:
					candidates.append(DnaRepeat(candidate, matched))
			all_candidates.extend(self._find_subsequent_repeats(target, candidates))
		return all_candidates

def finds(x): return len(x.start_indeces)

def find_by_repeat(repeats, repeat, unique = False):
	all_finds = [find for find in repeats if find.repeat == repeat]
	if unique:
		contains_one(repeats, repeat)
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

