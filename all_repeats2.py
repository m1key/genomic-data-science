import itertools

with open("all_dna.txt") as f:
	text = f.read()

	for p in itertools.product("ACGT", repeat=7):
		print "%s %d" % (''.join(p), len([i for i, _ in enumerate(text) if text.startswith(''.join(p), i)]))
