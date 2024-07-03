class BilirubinCalculator:
    @staticmethod
    def calculate_corrected_bilirubin(measured_bilirubin, hemolysis_index):
        # Implement your bilirubin correction calculation here
        corrected_bilirubin = measured_bilirubin - (0.0024 * hemolysis_index)
        return corrected_bilirubin

# Create a global instance of BilirubinCalculator
bilirubin_calc = BilirubinCalculator()
