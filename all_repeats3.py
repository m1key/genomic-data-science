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

start = 4
target = 12

assert Find("abc", [10]) == Find("abc", [10])
assert Find("abc", [10]) != Find("abc", [11])
assert Find("abc", [10]) != Find("abd", [10])
assert Find("abc", [10, 15]) == Find("abc", [10, 15])
assert Find("abc", [10, 15]) != Find("abc", [10, 16])

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

print find_repeats(dna, 7, initial)

def finds(x): return len(x.start_positions)

with open("all_dna.txt") as f:
	dna = f.read()
	initial = initial_repeats(dna)
	print max(map(finds, find_repeats(dna, 12, initial)))

#	
#	for p in itertools.product("ACGT", repeat=start):
##		sample = ''.join(p)
#		print "Sample:", sample
#		found_times = len([i for i, _ in enumerate(text) if text.startswith(''.join(p), i)]))
#	print "Found times:", found_times
