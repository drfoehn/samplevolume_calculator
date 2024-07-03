import json

class AnalytesCalculator:
    def __init__(self, json_file_path):
        self.data = self.load_data(json_file_path)
        self.selected_analytes = []

    @staticmethod
    def load_data(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def search_analytes(self, search_term):
        return [item for item in self.data if search_term.lower() in item['Untersuchung'].lower()]

    def calculate_sample_volume(self, hct_value, filling_volumes):
        if not 0 <= hct_value <= 100:
            raise ValueError("HCT value must be between 0 and 100")

        if not self.selected_analytes:
            raise ValueError("No analytes selected")

        results = {}
        for roehrchen_type in self.get_roehrchen_types():
            result = self.calculate_for_roehrchen_type(roehrchen_type, filling_volumes[roehrchen_type], hct_value)
            results[roehrchen_type] = result

        return results

    def calculate_for_roehrchen_type(self, roehrchen_type, filling_volume, hct_value):
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

    def get_roehrchen_types(self):
        return {a['Röhrchen'] for a in self.selected_analytes 
                if a['Wohin'] == "ZL" and a['Röhrchen'] in ["Heparin-Plasma", "EDTA-Plasma", "EDTA-Vollblut", "Serum", "Harn"]}

def create_tabs_and_checkboxes(analytes_data):
    groups = {}
    for item in analytes_data:
        if item['Gruppe'] not in groups:
            groups[item['Gruppe']] = []
        groups[item['Gruppe']].append(item)
    return groups

# Create a global instance of AnalytesCalculator
calculator = AnalytesCalculator('analytes.json')