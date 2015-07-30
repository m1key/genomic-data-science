with open("all_dna.txt") as f:
	text = f.read()

	word = "ACA"
	print len([i for i, _ in enumerate(text) if text.startswith(word, i)])
