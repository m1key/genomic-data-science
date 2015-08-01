import itertools
import re

class DnaFind:
	def __init__(self, repeat, start_indeces):
		self.repeat = repeat
		self.start_indeces = start_indeces
	def __eq__(self, other):
		return self.repeat == other.repeat and self.start_indeces == other.start_indeces
	def __repr__(self):
		return "DnaFind('%s', %s)" % (self.repeat, self.start_indeces)
	__str__ = __repr__

assert DnaFind("abc", [10]) == DnaFind("abc", [10])
assert DnaFind("abc", [10]) != DnaFind("abc", [11])
assert DnaFind("abc", [10]) != DnaFind("abd", [10])
assert DnaFind("abc", [10, 15]) == DnaFind("abc", [10, 15])
assert DnaFind("abc", [10, 15]) != DnaFind("abc", [10, 16])
a_find = DnaFind("acgtgact", [10, 14, 19])
assert eval(str(a_find)) == a_find

def initial_repeats(dna):
	start = 4
	repeats = []
        for p in itertools.product("ACGT", repeat=start):
                sample = ''.join(p)
                finds = [m.start() for m in re.finditer(sample, dna)]
		if len(finds) > 1:
			repeats.append(DnaFind(sample, finds))
	return repeats

dna = "TACGTAGCAGACGTAGCA"

initial = initial_repeats(dna)

target = 12
def find_repeats(dna, target, repeats):
	all_candidates = []
	for repeat in repeats:
		candidates = []
		for p in itertools.product("ACGT", repeat=1):
			candidate = repeat.repeat + ''.join(p)
			candidate_length = len(candidate)
			matched = []
			for start_position in repeat.start_indeces:
				if dna[start_position:start_position + candidate_length] == candidate:
					matched.append(start_position)
			if len(matched) > 1:
				candidates.append(DnaFind(candidate, matched))
		if len(repeat.repeat) + 1 < target:
			all_candidates.extend(find_repeats(dna, target, candidates))
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
	dna = f.read()
	initial = initial_repeats(dna)
	repeats = find_repeats(dna, 12, initial)
	contains_one(repeats, "AAAACGGCACCT") # Occurs twice in the dna.
	contains_zero(repeats, "AAAACGGCTCGG") # Occurs once in the dna, so not a repeat.
	contains_zero(repeats, "AAAACGGCTTAC") # Does not occur in the dna.
	contains_one(repeats, "GCTGCTCGACGC") # Occurs three times in the dna.
	has_start_indeces(repeats, "AAAACGGCACCT", 2)
	has_start_indeces(repeats, "GCTGCTCGACGC", 3)
	has_start_indeces(repeats, "GTATCCCCGAAG", 2)
	has_start_indeces_at(repeats, "TCGCGACACGTG", [10822, 39880])
	has_start_indeces_at(repeats, "GCGATCGGCGCG", [8850, 12155, 44391])
	assert len(repeats) == 921
	has_repeats_with_x_start_indeces(repeats, 2, 886)
	has_repeats_with_x_start_indeces(repeats, 3, 35)
	has_repeats_with_x_start_indeces(repeats, 4, 0)
	max_occurrences = max(map(finds, repeats))
	assert max_occurrences == 3
	print "All assertions passed."

#	
#	for p in itertools.product("ACGT", repeat=start):
##		sample = ''.join(p)
#		print "Sample:", sample
#		found_times = len([i for i, _ in enumerate(text) if text.startswith(''.join(p), i)]))
#	print "Found times:", found_times
