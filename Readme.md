### DNAMelting
Predicting DNA melting temperature from sequence, strand concentration, and salt concentration.

Using the SantaLucia melting temperatures as ground truth. I'll try a variety of models, as
a way to better learn pytorch (or tensorflow, whichever will be more convenient).

# To-do
1. [DONE] Gather SantaLucia.py, which I wroteyears ago, from the oxDNA repository.
2. Write a program that creates a database of sequences, strand concentrations
   salt concentrations and melting temperatures to use during training and validation.
   All sequences from 6-meres to 8-meres are a good amount.
3. Write a first wrapper that one-hot encodes the sequences, base by base, and uses a
   fully connected network to make a prediction.
4. Try doing the same by one-hot encoding base-pair steps.
5. Try doing something fancier, like encoding a recurring neural network or using
   embeddings.