import keras
import pickle
import tensorflow as tf
from sklearn.model_selection import train_test_split
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
from keras.callbacks import ReduceLROnPlateau

with open('seq_and_note.pkl', 'rb') as f:
    sequence_pairs = pickle.load(f)
print("Loaded the data")
# Separate the input_sequences and output_sequences
input_sequences = sequence_pairs[0]
output_sequences = sequence_pairs[1]
print("Seperated the sequences")

# Split the data into batches
print("Splitting to batches")
batch_size = 10000
batches = [(input_sequences[i:i + batch_size], output_sequences[i:i + batch_size])
           for i in range(0, len(input_sequences), batch_size)]

# Define the LSTM model
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(128, input_shape=(50, 4)),
    tf.keras.layers.Dense(4, activation='linear')
])
# Compile the model
model.compile(loss='mse', optimizer='adam')
# Display the model summary
model.summary()


# Define the custom callback
class CustomCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        print(f"\nEpoch {epoch + 1} finished. Loss: {logs['loss']}, Validation Loss: {logs['val_loss']}")


checkpoint = ModelCheckpoint('best_model.h5', monitor='val_loss', verbose=1, save_best_only=True, mode='min')
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=5, verbose=1, min_lr=1e-6)

history_list = []
# Train the model on each batch and save the trained model
for i, (input_batch, output_batch) in enumerate(batches):
    print(f"Training on batch {i + 1}/{len(batches)}...")
    input_train, input_val_test, output_train, output_val_test = train_test_split(input_batch, output_batch,
                                                                                  test_size=0.3, shuffle=False)
    input_val, input_test, output_val, output_test = train_test_split(input_val_test, output_val_test, test_size=0.5,
                                                                      shuffle=False)
    print("Split the data into training, validation, and testing sets")

    # Train the model with the custom callback and ModelCheckpoint
    history = model.fit(input_train, output_train, epochs=100, batch_size=64, validation_data=(input_val, output_val),
                        verbose=1, callbacks=[CustomCallback(), checkpoint, early_stopping, reduce_lr])
    # Append the training history to the list
    history_list.append(history.history)
    # Save the trained model
    model.save('first_LSTM_model_batch{}.h5'.format(i + 1))
    # Reload the saved model before training the next batch
    model = keras.models.load_model('first_LSTM_model_batch{}.h5'.format(i + 1))


final_test_loss = model.evaluate(input_test, output_test, verbose=1)
print(f"Final test loss: {final_test_loss}")
