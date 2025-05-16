from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import losses
import joblib
import os
import sys

# Fix Unicode output for Windows
sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

# Configure TensorFlow to be less verbose
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Difficulty labels
DIFFICULTY_LABELS = {
    1: "Very Easy",
    2: "Easy",
    3: "Moderate",
    4: "Hard",
    5: "Very Hard"
}

# Day configurations
DAY_PLANS = {
    1: {'name': 'Monday', 'muscle_groups': ["Chest", "Triceps"], 'display_name': "Chest & Triceps"},
    2: {'name': 'Tuesday', 'muscle_groups': ["Back", "Biceps"], 'display_name': "Back & Biceps"},
    3: {'name': 'Wednesday', 'muscle_groups': ["Legs", "Shoulders"], 'display_name': "Legs & Shoulders"},
    4: {'name': 'Thursday', 'muscle_groups': ["Core", "Full Body"], 'display_name': "Core & Full Body"},
    5: {'name': 'Friday', 'muscle_groups': ["Cardio", "Flexibility"], 'display_name': "Cardio & Flexibility"}
}

# Load models
try:
    with tf.keras.utils.custom_object_scope({'MeanSquaredError': losses.MeanSquaredError}):
        difficulty_model = tf.keras.models.load_model('models/difficulty_model.keras')
    time_scaler = joblib.load('models/time_scaler.save')
    print("[SUCCESS] Models loaded successfully")
except Exception as e:
    print(f"[ERROR] Model loading failed: {str(e)}")
    difficulty_model = None
    time_scaler = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Get user input
    user_data = {
        'age': request.form.get('age'),
        'weight': request.form.get('weight'),
        'height': request.form.get('height'),
        'category': request.form.get('category', 'Select'),
        'level': request.form.get('level', 'Select'),
        'equipment': request.form.get('equipment', 'Select')
    }

    # Validate inputs
    if any(v == 'Select' for v in [user_data['category'], user_data['level'], user_data['equipment']]):
        return render_template('index.html', error_message="Please select valid options for category, level, and equipment.")

    # Get the base directory of the project
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # Construct the correct path
    csv_path = os.path.join(BASE_DIR, "data", "exercisedata.csv")


    try:
        exercises_df = pd.read_csv(csv_path)
    except Exception as e:
        return render_template('index.html', error_message=f"Could not load exercise data: {str(e)}")

    # Filter exercises
    ai_category = f"{user_data['category']} + {user_data['level']} + {user_data['equipment']}"
    filtered_exercises = exercises_df[exercises_df['AI Category'] == ai_category]
    
    if filtered_exercises.empty:
        return render_template('index.html', error_message="No exercises found for the selected criteria.")

    # Process workout plan
    daily_plans = {}
    for day_num, day_info in DAY_PLANS.items():
        day_key = f"Day {day_num} - {day_info['name']}"
        day_exercises = filtered_exercises[filtered_exercises['Muscle Group'].isin(day_info['muscle_groups'])]
        
        if day_exercises.empty:
            day_exercises = filtered_exercises.sample(min(5, len(filtered_exercises)))
        if len(day_exercises) > 5:
            day_exercises = day_exercises.sample(5)

        exercises_list = []
        day_total_time = 0
        
        for _, exercise in day_exercises.iterrows():
            # Predict difficulty
            difficulty = None
            if difficulty_model:
                try:
                    # Get required features
                    duration = float(exercise.get('Duration (minutes)', 30))
                    reps = float(exercise.get('Reps', 10))
                    sets = float(exercise.get('Sets', 3))
                    intensity = float(exercise.get('Intensity', 3))
                    
                    features = np.array([[duration, reps, sets, intensity]])
                    
                    if time_scaler:
                        features = time_scaler.transform(features)
                    
                    pred = difficulty_model.predict(features, verbose=0)[0][0]
                    clamped_pred = max(1, min(5, pred))
                    difficulty = {
                        'value': round(clamped_pred),
                        'percent': int((clamped_pred/5)*100),
                        'label': DIFFICULTY_LABELS.get(round(clamped_pred), "Moderate")
                    }
                except Exception as e:
                    print(f"Difficulty prediction failed: {e}")

            exercises_list.append({
                'exercise_name': exercise['Exercise Name'],
                'muscle_group': exercise['Muscle Group'],
                'sets': exercise['Sets'],
                'reps': exercise['Reps'],
                'duration': exercise['Duration (minutes)'],
                'rest_time': exercise['Rest Time (seconds)'],
                'intensity': exercise['Intensity'],
                'difficulty': difficulty,
                'workout_notes': exercise['Workout Notes']
            })
            day_total_time += exercise['Duration (minutes)']

        # Adjust time based on level
        time_factor = 1.2 if user_data['level'] == 'Beginner' else 0.9 if user_data['level'] == 'Advanced' else 1.0

        daily_plans[day_key] = {
            'exercises': exercises_list,
            'muscle_groups': day_info['display_name'],
            'total_time': round(day_total_time * time_factor),
            'is_recommended': False
        }

    return render_template('index.html',
                         daily_plans=daily_plans,
                         user_data=user_data,
                         has_recommendations=False)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)