import itertools
import re

class DnaFind:
	def __init__(self, repeat, start_indeces):
		self.repeat = repeat
		self.start_indeces = start_indeces
	def __eq__(self, other):
		return self.repeat == other.repeat and self.start_indeces.sort() == other.start_indeces.sort()
	def __repr__(self):
		return "DnaFind('%s', %s)" % (self.repeat, self.start_indeces)
	__str__ = __repr__
	def __hash__(self):
		return hash(self.repeat)

assert DnaFind("abc", [10]) == DnaFind("abc", [10])
assert DnaFind("abc", [10]) != DnaFind("abc", [11])
assert DnaFind("abc", [10]) != DnaFind("abd", [10])
assert DnaFind("abc", [10, 15]) == DnaFind("abc", [10, 15])
assert DnaFind("abc", [10, 15]) != DnaFind("abc", [10, 16])
a_find = DnaFind("acgtgact", [10, 14, 19])
assert eval(str(a_find)) == a_find
assert DnaFind("cagt", [20, 30]) == DnaFind("cagt", [30, 20])

class DnaSequenceRepeats:
	def __init__(self, dna_sequence):
		self.dna_sequence = dna_sequence
	
	def find_repeats(self, repeat_size):
		initial_repeats = self._find_initial_repeats()
		if repeat_size == 1:
			return initial_repeats
		return self._find_subsequent_repeats(repeat_size, initial_repeats)

	def _find_initial_repeats(self):
		initial_repeat_length = 1
		initial_repeats = []
        	for sample_repeat_tuple in itertools.product("ACGT", repeat = initial_repeat_length):
                	sample_repeat = ''.join(sample_repeat_tuple)
			# Find overlapping matches:
                	finds = [match.start() for match in re.finditer('(?=%s)' % sample_repeat, self.dna_sequence)]
			# If this sample repeat has more than one occurrence, it could possibly be an even longer match:
			if len(finds) > 1:
				initial_repeats.append(DnaFind(sample_repeat, finds))
		return initial_repeats
	
	def _find_subsequent_repeats(self, target, repeats):
		all_candidates = []
		for repeat in repeats:
			candidates = []
			for p in itertools.product("ACGT", repeat=1):
				candidate = repeat.repeat + ''.join(p)
				candidate_length = len(candidate)
				matched = []
				for start_position in repeat.start_indeces:
					if self.dna_sequence[start_position:start_position + candidate_length] == candidate:
						matched.append(start_position)
				if len(matched) > 1:
					candidates.append(DnaFind(candidate, matched))
			if len(repeat.repeat) + 1 < target:
				all_candidates.extend(self._find_subsequent_repeats(target, candidates))
			else:
				all_candidates.extend(candidates)
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

	print "All assertions passed."

