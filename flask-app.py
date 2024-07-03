from flask import Flask, render_template, request, jsonify
from sample_volume_calculator import calculator, create_tabs_and_checkboxes
from bilirubin_calculator import bilirubin_calc

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sample_volume_calculator')
def sample_volume_calculator_route():
    groups = create_tabs_and_checkboxes(calculator.data)
    return render_template('sample_volume_calculator.html', groups=groups)

@app.route('/search_analytes', methods=['POST'])
def search_analytes_route():
    search_term = request.form['searchInput']
    results = calculator.search_analytes(search_term)
    return jsonify(results)

@app.route('/calculate_sample_volume', methods=['POST'])
def calculate_sample_volume_route():
    data = request.json
    hct_value = data['hct_value']
    filling_volumes = data['filling_volumes']
    calculator.selected_analytes = data['selected_analytes']
    
    results = calculator.calculate_sample_volume(hct_value, filling_volumes)
    return jsonify(results)

@app.route('/bilirubin_calculator')
def bilirubin_calculator_route():
    return render_template('bilirubin_calculator.html')

@app.route('/calculate_corrected_bilirubin', methods=['POST'])
def calculate_corrected_bilirubin_route():
    data = request.json
    measured_bilirubin = data['measured_bilirubin']
    hemolysis_index = data['hemolysis_index']
    
    corrected_bilirubin = bilirubin_calc.calculate_corrected_bilirubin(measured_bilirubin, hemolysis_index)
    
    return jsonify({'corrected_bilirubin': corrected_bilirubin})

if __name__ == '__main__':
    app.run(debug=True)