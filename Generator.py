import keras
import numpy as np
import pretty_midi

MAX_PITCH = 127
MAX_START_TIME = 1387.25
MAX_END_TIME = 1390
MAX_VELOCITY = 127

seed_max_pitch=0
seed_max_start_time=0
seed_max_end_time=0
seed_max_velocity=0


# loading the module
model = keras.models.load_model('first_LSTM_model_batch1.h5')
try:
    midi_data = pretty_midi.PrettyMIDI('AllMidiFiles/(Da Le) Yaleo.mid')
except Exception as e:
    print(f"Error processing {'AllMidiFiles/(Da Le) Yaleo.mid'}: {e}")
piano_notes = []
for instrument in midi_data.instruments:
    if 0 <= instrument.program < 8:  # Piano Family instruments have program numbers 0-7
        piano_notes.extend(instrument.notes)
seed_sequence = [[note.pitch, note.start, note.end, note.velocity] for note in piano_notes]
seed_sequence=seed_sequence[:50]
normalized_sequence = []
for note in seed_sequence:
    pitch = note[0] / MAX_PITCH
    start_time = note[1] / MAX_START_TIME
    end_time = note[2] / MAX_END_TIME
    velocity = note[3] / MAX_VELOCITY
    normalized_sequence.append([pitch, start_time, end_time, velocity])

output_sequence_normalized = []
for i in range(50):
    last_fifty_notes = normalized_sequence  # Get the last 50 elements of `normalized_sequence`
    output_note_normalized = model.predict(np.array([last_fifty_notes]))
    output_sequence_normalized.append(output_note_normalized[0])
    normalized_sequence.append(output_note_normalized[0])

output_sequence_denormalized = []
for note in output_sequence_normalized:
    pitch = round(note[0] * MAX_PITCH)
    start_time = round(note[1] * MAX_START_TIME)
    end_time = round(note[2] * MAX_END_TIME)
    velocity = round(note[3] * MAX_VELOCITY)
    output_sequence_denormalized.append([pitch, start_time, end_time, velocity])

for note in output_sequence_denormalized:
    print(note)
