import json
from typing import List, Dict, Any

class AnalytesCalculator:
    def __init__(self, json_file_path: str):
        self.data = self.load_data(json_file_path)
        self.selected_analytes = []

    @staticmethod
    def load_data(file_path: str) -> List[Dict[str, Any]]:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file '{file_path}'.")
            return []

    def search_analytes(self, search_term: str) -> List[Dict[str, Any]]:
        return [item for item in self.data if search_term.lower() in item['Untersuchung'].lower()]

    def update_selected_analytes(self, test: Dict[str, Any], is_checked: bool):
        if is_checked:
            self.selected_analytes.append(test)
        else:
            self.selected_analytes = [a for a in self.selected_analytes if a['Untersuchung'] != test['Untersuchung']]

    def get_roehrchen_types(self) -> set:
        return {a['Röhrchen'] for a in self.selected_analytes 
                if a['Wohin'] == "ZL" and a['Röhrchen'] in ["Heparin-Plasma", "EDTA-Plasma", "EDTA-Vollblut", "Serum", "Harn"]}

    def calculate_sample_volume(self, hct_value: float, filling_volumes: Dict[str, float]) -> Dict[str, Dict[str, float]]:
        if not 0 <= hct_value <= 100:
            raise ValueError("HCT value must be between 0 and 100")

        if not self.selected_analytes:
            raise ValueError("No analytes selected")

        results = {}
        for roehrchen_type in self.get_roehrchen_types():
            result = self.calculate_for_roehrchen_type(roehrchen_type, filling_volumes[roehrchen_type], hct_value)
            results[roehrchen_type] = result

        return results

    def calculate_for_roehrchen_typfrom flask import Flask, render_template, request, jsonify
from analytes_calculator import AnalytesCalculator

app = Flask(__name__)
calculator = AnalytesCalculator('analytes.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sample_volume_calculator')
def sample_volume_calculator():
    groups = create_tabs_and_checkboxes(calculator.data)
    return render_template('sample_volume_calculator.html', groups=groups)

@app.route('/search_analytes', methods=['POST'])
def search_analytes():
    search_term = request.form['searchInput']
    results = calculator.search_analytes(search_term)
    return jsonify(results)

@app.route('/calculate_sample_volume', methods=['POST'])
def calculate_sample_volume():
    data = request.json
    hct_value = data['hct_value']
    filling_volumes = data['filling_volumes']
    selected_analytes = data['selected_analytes']
    
    calculator.selected_analytes = selected_analytes
    results = calculator.calculate_sample_volume(hct_value, filling_volumes)
    return jsonify(results)
from flask import Flask, render_template, request, jsonify
from sample_volume_calculator import create_tabs_and_checkboxes, search_analytes, calculate_sample_volume
from bilirubin_calculator import calculate_corrected_bilirubin

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sample_volume_calculator')
def sample_volume_calculator_route():
    groups = create_tabs_and_checkboxes(search_analytes(''))  # Pass an empty string to get all analytes
    return render_template('sample_volume_calculator.html', groups=groups)

@app.route('/search_analytes', methods=['POST'])
def search_analytes_route():
    search_term = request.form['searchInput']
    results = search_analytes(search_term)
    return jsonify(results)

@app.route('/calculate_sample_volume', methods=['POST'])
def calculate_sample_volume_route():
    data = request.json
    hct_value = data['hct_value']
    filling_volumes = data['filling_volumes']
    selected_analytes = data['selected_analytes']
    
    results = calculate_sample_volume(hct_value, filling_volumes, selected_analytes)
    return jsonify(results)

@app.route('/bilirubin_calculator')
def bilirubin_calculator_route():
    return render_template('bilirubin_calculator.html')

@app.route('/calculate_corrected_bilirubin', methods=['POST'])
def calculate_corrected_bilirubin_route():
    data = request.json
    measured_bilirubin = data['measured_bilirubin']
    hemolysis_index = data['hemolysis_index']
    
    corrected_bilirubin = calculate_corrected_bilirubin(measured_bilirubin, hemolysis_index)
    
    return jsonify({'corrected_bilirubin': corrected_bilirubin})

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/bilirubin_calculator')
def bilirubin_calculator():
    return render_template('bilirubin_calculator.html')

@app.route('/calculate_corrected_bilirubin', methods=['POST'])
def calculate_corrected_bilirubin():
    data = request.json
    measured_bilirubin = data['measured_bilirubin']
    hemolysis_index = data['hemolysis_index']
    
    # Implement your bilirubin correction calculation here
    corrected_bilirubin = measured_bilirubin - (0.0024 * hemolysis_index)
    
    return jsonify({'corrected_bilirubin': corrected_bilirubin})

def create_tabs_and_checkboxes(analytes_data):
    groups = {}
    for item in analytes_data:
        if item['Gruppe'] not in groups:
            groups[item['Gruppe']] = []
        groups[item['Gruppe']].append(item)
    return groups

if __name__ == '__main__':
    app.run(debug=True)e(self, roehrchen_type: str, filling_volume: float, hct_value: float) -> Dict[str, float]:
        total_probenmenge = 0
        highest_totvolumen = 0
        is_urine_sample = False

        for analyte in self.selected_analytes:
            if analyte['Röhrchen'] == roehrchen_type:
                probenmenge = float(analyte['Mindestprobenmenge (Pipettiermenge) \nin µl']) if analyte['Mindestprobenmenge (Pipettiermenge) \nin µl'] else 0
                totvolumen = float(analyte['Benötigtes Totvolumen \nin µl']) if analyte['Benötigtes Totvolumen \nin µl'] else 0

                highest_totvolumen = max(highest_totvolumen, totvolumen)
                total_probenmenge += probenmenge

                if 'harn' in roehrchen_type.lower():
                    is_urine_sample = True

        if is_urine_sample:
            total_volume = total_probenmenge + highest_totvolumen
            plasma_volume = total_volume
        else:
            hct_fraction = hct_value / 100
            plasma_volume = total_probenmenge + highest_totvolumen
            total_volume = plasma_volume / (1 - hct_fraction)

        warning = total_volume > filling_volume

        return {
            "volume": total_volume,
            "hct_value": hct_value,
            "highest_totvolumen": highest_totvolumen,
            "plasma_volume": plasma_volume,
            "warning": warning
        }

def create_tabs_and_checkboxes(analytes_data):
    groups = {}
    for item in analytes_data:
        if item['Gruppe'] not in groups:
            groups[item['Gruppe']] = []
        groups[item['Gruppe']].append(item)
    
    return groups

def print_tabs_and_checkboxes(groups):
    for group, tests in groups.items():
        print(f"Tab: {group}")
        for test in tests:
            print(f"  [ ] {test['Untersuchung']}")
        print()

def simulate_user_interaction(calculator):
    # Simulating user selecting some analytes
    selected_tests = ["Anti Xa Heparinmonitoring", "Fibrinogen", "Kreatinin (+eGFR) im Blut"]
    for test in selected_tests:
        matching_tests = [t for t in calculator.data if t['Untersuchung'] == test]
        if matching_tests:
            calculator.update_selected_analytes(matching_tests[0], True)
    
    # Print selected analytes
    print("Selected Analytes:")
    for analyte in calculator.selected_analytes:
        print(f"- {analyte['Untersuchung']}")
    print()

    # Get and print Röhrchen types
    roehrchen_types = calculator.get_roehrchen_types()
    print("Röhrchen types:", roehrchen_types)
    print()

    # Simulate filling volume selection
    filling_volumes = {roehrchen: 500 for roehrchen in roehrchen_types}

    return filling_volumes

def main():
    calculator = AnalytesCalculator('analytes.json')
    
    # Create and print tabs and checkboxes
    groups = create_tabs_and_checkboxes(calculator.data)
    print_tabs_and_checkboxes(groups)

    # Simulate user interaction
    filling_volumes = simulate_user_interaction(calculator)

    # Calculate and print results
    try:
        results = calculator.calculate_sample_volume(40, filling_volumes)
        for roehrchen, result in results.items():
            print(f"\nResults for {roehrchen}:")
            print(f"Required plasma volume: {result['plasma_volume']:.2f} µl")
            print(f"Dead volume: {result['highest_totvolumen']:.2f} µl")
            print(f"Required total blood volume: {result['volume']:.2f} µl")
            if result['warning']:
                print("WARNING: Required volume exceeds maximum filling volume of the tube.")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()