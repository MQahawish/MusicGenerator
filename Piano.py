from tkinter import *
import simpleaudio as sa

# Define the note frequencies
notes = {
    "C3": 130.81,
    "C#3": 138.59,
    "D3": 146.83,
    "D#3": 155.56,
    "E3": 164.81,
    "F3": 174.61,
    "F#3": 185.00,
    "G3": 196.00,
    "G#3": 207.65,
    "A3": 220.00,
    "A#3": 233.08,
    "B3": 246.94,
    "C4": 261.63,
    "C#4": 277.18,
    "D4": 293.66,
    "D#4": 311.13,
    "E4": 329.63,
    "F4": 349.23,
    "F#4": 369.99,
    "G4": 392.00,
    "G#4": 415.30,
    "A4": 440.00,
    "A#4": 466.16,
    "B4": 493.88
}


# Define the function to play a note
def play_note(note):
    wave_obj = sa.WaveObject.from_wave_file("piano_samples/" + note + ".wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()


# Create a window
root = Tk()
root.title("Piano Keyboard")

# Create the piano keys
for i in range(88):
    # Determine the note and octave of the key
    note = "C" + str(i // 12 - 1)
    octave = str(i // 12)

    # Create the key label
    label = f"{note}{octave}"

    # Determine the color of the key (black or white)
    if note[-1] in ["#", "b"]:
        color = "black"
    else:
        color = "white"


    # Define the function to call when the key is pressed
    def callback(note=note):
        play_note(note)


    # Create the key button
    button = Button(root, text=label, bg=color, width=3, command=callback)
    button.grid(row=0, column=i, sticky="ew")

# Run the window
root.mainloop()
