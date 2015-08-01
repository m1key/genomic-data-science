import itertools
import re

class Find:
	def __init__(self, sequence, start_positions):
		self.sequence = sequence
		self.start_positions = start_positions
	def __eq__(self, other):
		return self.sequence == other.sequence and self.start_positions == other.start_positions
	def __repr__(self):
		return "Find('%s', %s)" % (self.sequence, self.start_positions)
	__str__ = __repr__

start = 4
target = 12

assert Find("abc", [10]) == Find("abc", [10])
assert Find("abc", [10]) != Find("abc", [11])
assert Find("abc", [10]) != Find("abd", [10])
assert Find("abc", [10, 15]) == Find("abc", [10, 15])
assert Find("abc", [10, 15]) != Find("abc", [10, 16])
find = Find("acgtgact", [10, 14, 19])
assert eval(str(find)) == find

def initial_repeats(dna):
	start = 4
	repeats = []
        for p in itertools.product("ACGT", repeat=start):
                sample = ''.join(p)
                finds = [m.start() for m in re.finditer(sample, dna)]
		if len(finds) > 1:
			repeats.append(Find(sample, finds))
	return repeats

dna = "TACGTAGCAGACGTAGCA"

initial = initial_repeats(dna)

def find_repeats(dna, target, repeats):
	all_candidates = []
	for repeat in repeats:
		candidates = []
		for p in itertools.product("ACGT", repeat=1):
			candidate = repeat.sequence + ''.join(p)
			candidate_length = len(candidate)
			matched = []
			for start_position in repeat.start_positions:
				if dna[start_position:start_position + candidate_length] == candidate:
					matched.append(start_position)
			if len(matched) > 1:
				candidates.append(Find(candidate, matched))
		if len(repeat.sequence) + 1 < target:
			all_candidates.extend(find_repeats(dna, target, candidates))
		else:
			all_candidates.extend(candidates)
	return all_candidates

def finds(x): return len(x.start_positions)

def find_by_sequence(repeats, sequence, unique = False):
	all_finds = [find for find in repeats if find.sequence == sequence]
	if unique:
		contains_one(repeats, sequence)
		return all_finds[0]
	else:
		return all_finds
def contains(repeats, sequence, times):
	assert len(find_by_sequence(repeats, sequence)) == times
def contains_one(repeats, sequence):
	contains(repeats, sequence, 1)
def contains_zero(repeats, sequence):
	contains(repeats, sequence, 0)
def has_start_positions(repeats, sequence, start_position_count):
	assert len(find_by_sequence(repeats, sequence, unique = True).start_positions) == start_position_count
def has_repeats_with_x_start_indeces(repeats, start_indeces_count, count):
	assert len([find for find in repeats if len(find.start_positions) == start_indeces_count]) == count
def has_start_indeces_at(repeats, sequence, start_indeces):
	assert find_by_sequence(repeats, sequence, unique = True).start_positions == start_indeces

with open("all_dna.txt") as f:
	dna = f.read()
	initial = initial_repeats(dna)
	repeats = find_repeats(dna, 12, initial)
	contains_one(repeats, "AAAACGGCACCT") # Occurs twice in the dna.
	contains_zero(repeats, "AAAACGGCTCGG") # Occurs once in the dna, so not a repeat.
	contains_zero(repeats, "AAAACGGCTTAC") # Does not occur in the dna.
	contains_one(repeats, "GCTGCTCGACGC") # Occurs three times in the dna.
	has_start_positions(repeats, "AAAACGGCACCT", 2)
	has_start_positions(repeats, "GCTGCTCGACGC", 3)
	has_start_positions(repeats, "GTATCCCCGAAG", 2)
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
