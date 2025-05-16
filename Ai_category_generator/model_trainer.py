import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, losses
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os
import sys

# This script generates synthetic workout data, preprocesses it, builds a neural network model using TensorFlow,
# trains it to predict workout difficulty, and saves both the trained model and scaler for future use.

# Fix Unicode output for Windows to avoid encoding issues
sys.stdout.reconfigure(encoding='utf-8')

# Ensure the 'models' directory exists for saving the trained model
os.makedirs('models', exist_ok=True)

# Set seed for reproducibility
np.random.seed(42)
n_samples = 5000  # Define the number of samples for our synthetic dataset

# Generate synthetic workout data with realistic distributions
# Using normal distribution with mean and standard deviation for each feature
# Clip values to ensure they fall within realistic ranges

data = {
    'Duration (minutes)': np.clip(np.random.normal(30, 15, n_samples), 5, 60),  # Workout duration
    'Reps': np.clip(np.random.normal(12, 6, n_samples), 5, 30).astype(int),      # Number of repetitions
    'Sets': np.clip(np.random.normal(3, 1, n_samples), 1, 5).astype(int),       # Number of sets
    'Intensity': np.clip(np.random.normal(3, 1, n_samples), 1, 5)               # Intensity level (scale 1-5)
}

# Compute workout difficulty based on a weighted formula
# Difficulty is a combination of duration, reps, sets, and intensity
# The formula ensures that difficulty stays between 1 and 5

data['Difficulty'] = (
    0.3 * (data['Duration (minutes)'] / 10) +  # Duration contributes 30%
    0.2 * (data['Reps'] / 5) +                # Reps contribute 20%
    0.2 * data['Sets'] +                      # Sets contribute 20%
    0.3 * data['Intensity']                   # Intensity contributes 30%
)
data['Difficulty'] = np.clip(data['Difficulty'], 1, 5)  # Ensure difficulty is within range

# Convert dictionary to Pandas DataFrame
df = pd.DataFrame(data)

# Split the dataset into features (X) and target (y)
X = df[['Duration (minutes)', 'Reps', 'Sets', 'Intensity']]
y = df['Difficulty']

# Split data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the feature values for better model performance
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Fit on training data
X_test_scaled = scaler.transform(X_test)        # Transform test data using the same scaler

# Define a simple neural network model for predicting workout difficulty
model = tf.keras.Sequential([
    layers.Input(shape=(4,)),    # Input layer with 4 features
    layers.Dense(64, activation='relu'),  # First hidden layer with 64 neurons and ReLU activation
    layers.Dropout(0.2),         # Dropout layer to prevent overfitting
    layers.Dense(32, activation='relu'),  # Second hidden layer with 32 neurons
    layers.Dense(1)              # Output layer with a single neuron (predicts difficulty)
])

# Compile the model using Mean Squared Error loss and Adam optimizer
model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),  # Adam optimizer with a learning rate of 0.001
    loss=losses.MeanSquaredError(),            # Mean Squared Error as the loss function
    metrics=['mae']                             # Track Mean Absolute Error (MAE) during training
)

# Train the model using training data
history = model.fit(
    X_train_scaled, y_train,       # Training data
    epochs=50,                     # Train for 50 epochs
    batch_size=32,                  # Mini-batch size of 32
    validation_data=(X_test_scaled, y_test),  # Validation set for monitoring performance
    verbose=1  # Show training progress
)

# Save the trained model and scaler for future predictions
model.save('models/difficulty_model.keras')  # Save the model in TensorFlow format
joblib.dump(scaler, 'models/time_scaler.save')  # Save the feature scaler

# Print success message and final model accuracy
print("[SUCCESS] Models trained and saved successfully")
print(f"Final MAE: {history.history['val_mae'][-1]:.2f}")  # Show final validation MAE
