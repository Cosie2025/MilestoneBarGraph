from flask import Flask, request, jsonify, send_file
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__, static_folder='static')

# Define X-Axis Labels
MILESTONES = ["A0 - A1", "A1 - A2", "A2 - B1"]

def create_milestone_chart(durations, filename):
    y_values = durations  # Y-axis values (months)
    x_values = np.arange(len(MILESTONES))  # X-axis positions
    
    # Create the bar chart
    fig, ax = plt.subplots(figsize=(6, 4))  # Set figure size
    bars = ax.bar(x_values, y_values, color=["#FF5733", "#33FF57", "#3357FF"], alpha=0.8)
    
    # Add labels and titles
    ax.set_xticks(x_values)
    ax.set_xticklabels(MILESTONES, fontsize=10)
    ax.set_yticks(range(1, max(y_values) + 2))  # Adjust Y-axis limits dynamically
    ax.set_ylabel("Months", fontsize=12)
    ax.set_title("Milestone Progress Chart", fontsize=14)
    
    # Display values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.2, str(height), ha='center', fontsize=10, fontweight='bold')
    
    static_dir = os.path.join(os.getcwd(), "static")
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    img_path = os.path.join(static_dir, filename)
    plt.savefig(img_path, format='jpeg', bbox_inches='tight', pad_inches=0.5)
    plt.close(fig)
    return img_path

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    try:
        data = request.json
        durations = [
            data.get("A0_A1", 0),
            data.get("A1_A2", 0),
            data.get("A2_B1", 0)
        ]
        
        if not all(isinstance(duration, (int, float)) for duration in durations):
            return jsonify({'error': 'All values must be numeric'}), 400

        # Generate unique filename to avoid cache issues
        filename = f"milestone_chart_{np.random.randint(100000)}.jpeg"
        image_path = create_milestone_chart(durations, filename)

        # Return image directly with correct MIME type
        return send_file(image_path, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return jsonify({"message": "Milestone Chart API is running. Use POST /generate_chart to generate charts."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# requirements.txt
# Flask
# matplotlib
# numpy
# gunicorn
