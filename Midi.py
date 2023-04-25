import os
import pickle
import numpy as np
import pretty_midi



midi_directory = 'AllMidiFiles'


# getting note info from one midi file
def extract_note_data(midi_path):
    try:
        midi_data = pretty_midi.PrettyMIDI(midi_path)
    except Exception as e:
        print(f"Error processing {midi_path}: {e}")
        return None

    piano_notes = []
    for instrument in midi_data.instruments:
        if 0 <= instrument.program < 8:  # Piano Family instruments have program numbers 0-7
            piano_notes.extend(instrument.notes)
    note_data = [[note.pitch, note.start, note.end, note.velocity] for note in piano_notes]
    print(f"got data for {midi_path}")
    return note_data


# getting notes info of all the midi files
def get_all_notes_data(midi_directory):
    all_files_note_data = []
    for file in os.listdir(midi_directory):
        midi_path = os.path.join(midi_directory, file)
        note_data = extract_note_data(midi_path)
        if note_data:
            all_files_note_data.append(note_data)
    print(f"Got all notes data for {midi_directory}")
    return all_files_note_data


# saving the data so that I can use it later , without needing to preprocess again
def save_data_to_pickle(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
    print(f"Saved data to {filename}")


# loading the data so that I saved in pickle
def load_data_from_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    print(f"Loaded data from {filename}")
    return data


def preprocess_data(note_data, sequence_length=100):
    # Flatten note_data (assuming it is a list of lists)
    flattened_note_data = [note for song in note_data for note in song]

    # Find the maximum values for pitch, start_time, end_time, and velocity
    max_pitch = max(note[0] for note in flattened_note_data)
    max_start_time = max(note[1] for note in flattened_note_data)
    max_end_time = max(note[2] for note in flattened_note_data)
    max_velocity = max(note[3] for note in flattened_note_data)

    # Normalize the data
    normalized_data = [
        [
            note[0] / max_pitch,
            note[1] / max_start_time,
            note[2] / max_end_time,
            note[3] / max_velocity
        ] for note in flattened_note_data
    ]

    # Create input-output sequences in a single loop
    input_sequences = []
    output_sequences = []
    print("Making ",len(normalized_data) - sequence_length," pairs:")
    for i in range(len(normalized_data) - sequence_length):
        input_sequences.append(normalized_data[i:i + sequence_length])
        output_sequences.append(normalized_data[i + sequence_length])
        print(f"Pairs left to do: {len(normalized_data)-sequence_length-i}")

    # Convert to numpy arrays
    input_sequences = np.array(input_sequences)
    output_sequences = np.array(output_sequences)

    return input_sequences, output_sequences


data = load_data_from_pickle("data.pkl")
sequences, notes = preprocess_data(data, 50)
save_data_to_pickle((sequences, notes), "seq_and_note.pkl")
print(sequences[0])
print(notes[0])
