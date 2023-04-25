# MusicGenerator
Program that generates music using machine-learning

* Data set :
   The ADL Piano MIDI is a dataset of 11,086 piano pieces from different genres. This dataset is based on the Lakh MIDI dataset, which is a collection on 45,129 unique MIDI files that have been matched to entries in the Million Song Dataset. Most pieces in the Lakh MIDI dataset have multiple instruments, so for each file the authors of ADL Piano MIDI dataset extracted only the tracks with instruments from the "Piano Family" (MIDI program numbers 1-8). This process generated a total of 9,021 unique piano MIDI files. Theses 9,021 files were then combined with other approximately 2,065 files scraped from publicly-available sources on the internet. All the files in the final collection were de-duped according to their MD5 checksum.


* Modules:

  * Midi : it's purpose is to preprocess the data to a sortable input shape and type to fee to the model.

  * LTSM : The model script , it should run the model on an input and output a sequence of piano playing , that is playable in audio (converting from midi to audiuo

  * Generator : this module should as the user for input using a piano simulation in python where the user keeps entering input until it's enough input to feed to the model , and then plays the output from the model in the window after asking the user to press the play button




