# AI Workout Generator

An intelligent workout plan generator that uses machine learning to create personalized weekly workout plans based on user preferences, fitness level, and available equipment.

## Features

- **Personalized Workout Plans**: Generates 5-day weekly workout plans tailored to your fitness goals
- **AI-Powered Difficulty Prediction**: Uses a neural network to predict exercise difficulty based on duration, reps, sets, and intensity
- **Multiple Workout Categories**: Supports Cardio, Strength, Flexibility, and HIIT workouts
- **Fitness Level Adaptation**: Adapts plans for Beginner, Intermediate, and Advanced fitness levels
- **Equipment-Based Filtering**: Filters exercises based on available equipment (None, Dumbbells, Resistance Bands, Treadmill)
- **Muscle Group Targeting**: Organizes workouts by muscle groups (Chest, Triceps, Back, Biceps, Legs, Shoulders, Core, Full Body)
- **Interactive UI**: Clean, responsive web interface with collapsible day plans
- **Real-time Difficulty Metrics**: Visual difficulty meters showing exercise intensity levels

## Tech Stack

- **Backend**: Flask (Python)
- **Machine Learning**: TensorFlow/Keras for difficulty prediction
- **Data Processing**: Pandas, NumPy
- **Model Training**: Scikit-learn for data preprocessing
- **Frontend**: HTML, CSS, JavaScript with Font Awesome icons

## Project Structure

```
Ai_workout_generator/
├── Ai_category_generator/
│   ├── app/
│   │   ├── __init__.py          # Flask app initialization
│   │   ├── routes.py            # Main application routes and logic
│   │   ├── static/
│   │   │   └── styles.css       # Styling for the web interface
│   │   └── templates/
│   │       └── index.html       # Main HTML template
│   ├── data/
│   │   └── exercisedata.csv     # Exercise database
│   ├── models/
│   │   ├── difficulty_model.keras  # Trained ML model
│   │   └── time_scaler.save     # Feature scaler for ML model
│   ├── generate_csv.py          # Script to generate workout data
│   ├── model_trainer.py         # Script to train the ML model
│   └── run.py                   # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Ai_workout_generator
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate exercise data** (optional - data already included):
   ```bash
   cd Ai_category_generator
   python generate_csv.py
   ```

5. **Train the ML model** (optional - model already included):
   ```bash
   python model_trainer.py
   ```

## Usage

### Starting the Application

Navigate to the `Ai_category_generator` directory and run:

```bash
cd Ai_category_generator
python run.py
```

The application will start on `http://localhost:5001`

### Using the Web Interface

1. Open your browser and navigate to `http://localhost:5001`
2. Fill in your personal details:
   - Age
   - Weight (kg)
   - Height (cm)
3. Select your workout preferences:
   - Category: Cardio, Strength, Flexibility, or HIIT
   - Fitness Level: Beginner, Intermediate, or Advanced
   - Equipment: None, Dumbbell, Resistance Band, or Treadmill
4. Click "Generate Workout Plan"
5. View your personalized 5-day workout plan with:
   - Exercise details (sets, reps, duration, rest time)
   - Difficulty predictions with visual meters
   - Muscle group targeting
   - Estimated workout time per day

## Machine Learning Model

The application uses a neural network to predict exercise difficulty based on:

- **Features**: Duration (minutes), Reps, Sets, Intensity (1-5 scale)
- **Model Architecture**:
  - Input layer (4 features)
  - Dense layer (64 neurons, ReLU activation)
  - Dropout layer (0.2) for regularization
  - Dense layer (32 neurons, ReLU activation)
  - Output layer (1 neuron for difficulty prediction)
- **Training**: 5000 synthetic samples, 50 epochs, batch size 32
- **Loss Function**: Mean Squared Error
- **Optimizer**: Adam (learning rate 0.001)

## API Endpoints

- `GET /` - Home page with workout generation form
- `POST /generate` - Generates personalized workout plan based on user input

## Development

### Adding New Exercises

To add new exercises, update the `data/exercisedata.csv` file with the following columns:
- Plan ID, Day, Exercise Name, Muscle Group, Workout Type, Fitness Level
- Equipment Needed, Sets, Reps, Rest Time, Duration, AI Category
- Intensity, Superset/Regular, Calories Burned, Workout Notes

### Retraining the Model

If you modify the exercise data significantly, retrain the model:

```bash
cd Ai_category_generator
python model_trainer.py
```

## Security & Privacy

- No API keys or external services required
- All data processing happens locally
- No user data is stored or transmitted
- No sensitive information found in the codebase

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Inspired by the need for personalized workout planning
- Uses TensorFlow for machine learning capabilities
- UI designed with modern web standards