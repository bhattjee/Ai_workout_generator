import pandas as pd
import itertools

# Define categories, levels, equipment, and muscle groups
categories = ['Cardio', 'Strength', 'Flexibility', 'HIIT']
levels = ['Beginner', 'Intermediate', 'Advanced']
equipment = ['None', 'Dumbbells', 'Resistance Bands', 'Treadmill']
muscle_groups = ['Full Body', 'Core', 'Legs', 'Back', 'Shoulders', 'Arms', 'Chest']

# Define exercise templates for each muscle group
exercise_templates = {
    'Full Body': [
        {'name': 'Jumping Jacks', 'duration': 30, 'reps': 15, 'sets': 5, 'description': 'A full-body exercise that improves cardiovascular fitness.', 'equipment': 'None'},
        {'name': 'Burpees', 'duration': 10, 'reps': 25, 'sets': 3, 'description': 'A full-body exercise that combines squats, push-ups, and jumps.', 'equipment': 'None'},
        {'name': 'Rowing', 'duration': 30, 'reps': 30, 'sets': 5, 'description': 'Full-body cardio using a rowing machine.', 'equipment': 'None'},
        {'name': 'Elliptical', 'duration': 30, 'reps': 20, 'sets': 5, 'description': 'Low-impact cardio using an elliptical machine.', 'equipment': 'None'},
        {'name': 'Treadmill Incline Walk', 'duration': 20, 'reps': '-', 'sets': 1, 'description': 'Walking on an inclined treadmill to increase intensity and target different muscles.', 'equipment': 'Treadmill'}
    ],
    'Core': [
        {'name': 'Plank', 'duration': 5, 'reps': '-', 'sets': 3, 'description': 'A core-strengthening exercise held for 30 seconds.', 'equipment': 'None'},
        {'name': 'Russian Twists', 'duration': 5, 'reps': 20, 'sets': 3, 'description': 'Targets core muscles with a twisting motion.', 'equipment': 'None'},
        {'name': 'Bird Dogs', 'duration': 5, 'reps': 12, 'sets': 3, 'description': 'Strengthens core and improves balance.', 'equipment': 'None'},
        {'name': 'Dead Bugs', 'duration': 5, 'reps': 15, 'sets': 3, 'description': 'Strengthens core muscles.', 'equipment': 'None'},
        {'name': 'Superman Hold', 'duration': 5, 'reps': '-', 'sets': 3, 'description': 'Strengthens lower back and glutes.', 'equipment': 'None'}
    ],
    'Legs': [
        {'name': 'Dumbbell Squats', 'duration': 10, 'reps': 15, 'sets': 3, 'description': 'Strengthens lower body muscles using dumbbells.', 'equipment': 'Dumbbells'},
        {'name': 'Lunges', 'duration': 10, 'reps': 12, 'sets': 3, 'description': 'Strengthens legs and improves balance.', 'equipment': 'None'},
        {'name': 'Box Jumps', 'duration': 15, 'reps': 15, 'sets': 4, 'description': 'Explosive exercise that builds power in the lower body.', 'equipment': 'None'},
        {'name': 'Step-Box Jumps', 'duration': 20, 'reps': 30, 'sets': 5, 'description': 'A cardio exercise that strengthens legs using a platform.', 'equipment': 'None'},
        {'name': 'Treadmill Sprints', 'duration': 20, 'reps': 30, 'sets': 4, 'description': 'High-intensity sprints on a treadmill.', 'equipment': 'Treadmill'}
    ],
    'Back': [
        {'name': 'Deadlifts', 'duration': 10, 'reps': 10, 'sets': 3, 'description': 'Strengthens lower back and legs using dumbbells.', 'equipment': 'Dumbbells'},
        {'name': 'Bent-Over Rows', 'duration': 10, 'reps': 12, 'sets': 3, 'description': 'Strengthens upper back using dumbbells.', 'equipment': 'Dumbbells'},
        {'name': 'Pull-Ups', 'duration': 10, 'reps': 8, 'sets': 3, 'description': 'Strengthens back and biceps using a pull-up bar.', 'equipment': 'None'},
        {'name': 'Chin-Ups', 'duration': 10, 'reps': 8, 'sets': 3, 'description': 'Strengthens back and biceps using a pull-up bar.', 'equipment': 'None'},
        {'name': 'Renegade Rows', 'duration': 10, 'reps': 12, 'sets': 3, 'description': 'Strengthens back and core using dumbbells.', 'equipment': 'Dumbbells'}
    ],
    'Shoulders': [
        {'name': 'Shoulder Press', 'duration': 10, 'reps': 10, 'sets': 3, 'description': 'Strengthens shoulders using dumbbells.', 'equipment': 'Dumbbells'},
        {'name': 'Arnold Press', 'duration': 10, 'reps': 10, 'sets': 3, 'description': 'A shoulder exercise that targets all deltoid heads.', 'equipment': 'Dumbbells'},
        {'name': 'Front Raises', 'duration': 10, 'reps': 12, 'sets': 3, 'description': 'Strengthens front deltoids using dumbbells.', 'equipment': 'Dumbbells'},
        {'name': 'Lateral Raises', 'duration': 10, 'reps': 12, 'sets': 3, 'description': 'Strengthens side deltoids using dumbbells.', 'equipment': 'Dumbbells'},
        {'name': 'Overhead Press', 'duration': 10, 'reps': 10, 'sets': 3, 'description': 'Strengthens shoulders using dumbbells.', 'equipment': 'Dumbbells'}
    ],
    'Arms': [
        {'name': 'Bicep Curls', 'duration': 10, 'reps': 12, 'sets': 3, 'description': 'Strengthens biceps using dumbbells.', 'equipment': 'Dumbbells'},
        {'name': 'Tricep Dips', 'duration': 10, 'reps': 10, 'sets': 3, 'description': 'Strengthens triceps using body weight.', 'equipment': 'None'},
        {'name': 'Dips', 'duration': 10, 'reps': 10, 'sets': 3, 'description': 'Strengthens triceps and chest using parallel bars.', 'equipment': 'None'},
        {'name': 'Wrist Stretch', 'duration': 10, 'reps': '-', 'sets': 3, 'description': 'Stretches wrist muscles.', 'equipment': 'None'},
        {'name': 'Kettlebell Swings', 'duration': 10, 'reps': 15, 'sets': 3, 'description': 'Strengthens lower body and core using a kettlebell.', 'equipment': 'Dumbbells'}
    ],
    'Chest': [
        {'name': 'Chest Flys', 'duration': 10, 'reps': 12, 'sets': 3, 'description': 'Strengthens chest muscles using dumbbells.', 'equipment': 'Dumbbells'},
        {'name': 'Push-Ups', 'duration': 5, 'reps': 10, 'sets': 3, 'description': 'Strengthens upper body and core muscles.', 'equipment': 'None'},
        {'name': 'Dips', 'duration': 10, 'reps': 10, 'sets': 3, 'description': 'Strengthens triceps and chest using parallel bars.', 'equipment': 'None'},
        {'name': 'Cobra Stretch', 'duration': 10, 'reps': '-', 'sets': 3, 'description': 'Stretches chest and abdomen.', 'equipment': 'None'},
        {'name': 'Goblet Squats', 'duration': 10, 'reps': 12, 'sets': 3, 'description': 'Strengthens legs using a kettlebell.', 'equipment': 'Dumbbells'}
    ]
}

# Define muscle groups for each day
muscle_groups = {
    'Monday': 'Chest',
    'Tuesday': 'Back',
    'Wednesday': 'Legs',
    'Thursday': 'Shoulders',
    'Friday': 'Arms',
    'Saturday': 'Core'
}

# Generate static workout plans
workout_plans = []

for category in categories:
    for level in levels:
        for eq in equipment:
            plan_id = f"{category}_{level}_{eq}"
            daily_plans = {}
            exercises_per_day = 4  # Number of exercises per day

            for day, muscle_group in muscle_groups.items():
                # Filter exercises for the muscle group
                muscle_exercises = [template for template in exercise_templates[muscle_group] if template['equipment'] == eq]
                # Select up to 4 exercises for the day
                daily_exercises = muscle_exercises[:exercises_per_day]
                daily_plans[day] = daily_exercises

            # Flatten the daily plans into a single list of exercises
            for day, exercises in daily_plans.items():
                for exercise in exercises:
                    workout_plans.append({
                        'plan_id': plan_id,
                        'day': day,
                        'exercise_name': exercise['name'],
                        'category': category,
                        'duration': exercise['duration'],
                        'equipment_required': eq,
                        'difficulty_level': level,
                        'reps': exercise['reps'],
                        'sets': exercise['sets'],
                        'description': exercise['description'],
                        'muscle_group': muscle_group
                    })

# Create DataFrame
workout_plans_df = pd.DataFrame(workout_plans)

# Save to CSV
workout_plans_df.to_csv('data/workout_plans.csv', index=False)

print("CSV file generated successfully!")