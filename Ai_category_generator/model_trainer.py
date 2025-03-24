import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, losses
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os
import sys

# Fix Unicode output for Windows
sys.stdout.reconfigure(encoding='utf-8')

# Create models directory
os.makedirs('models', exist_ok=True)

# Generate realistic sample data
np.random.seed(42)
n_samples = 5000

data = {
    'Duration (minutes)': np.clip(np.random.normal(30, 15, n_samples), 5, 60),
    'Reps': np.clip(np.random.normal(12, 6, n_samples), 5, 30).astype(int),
    'Sets': np.clip(np.random.normal(3, 1, n_samples), 1, 5).astype(int),
    'Intensity': np.clip(np.random.normal(3, 1, n_samples), 1, 5)
}

# Calculate realistic difficulty (target)
data['Difficulty'] = (
    0.3 * (data['Duration (minutes)'] / 10) +
    0.2 * (data['Reps'] / 5) +
    0.2 * data['Sets'] +
    0.3 * data['Intensity']
)
data['Difficulty'] = np.clip(data['Difficulty'], 1, 5)

df = pd.DataFrame(data)

# Split data
X = df[['Duration (minutes)', 'Reps', 'Sets', 'Intensity']]
y = df['Difficulty']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Build model
model = tf.keras.Sequential([
    layers.Input(shape=(4,)),  # Proper input layer
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(32, activation='relu'),
    layers.Dense(1)
])

# Use MeanSquaredError directly
model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss=losses.MeanSquaredError(),  # Changed to class-based loss
    metrics=['mae']
)

# Train
history = model.fit(
    X_train_scaled, y_train,
    epochs=50,
    batch_size=32,
    validation_data=(X_test_scaled, y_test),
    verbose=1  # Changed to see progress
)

# Save models
model.save('models/difficulty_model.keras')
joblib.dump(scaler, 'models/time_scaler.save')

print("[SUCCESS] Models trained and saved successfully")
print(f"Final MAE: {history.history['val_mae'][-1]:.2f}")