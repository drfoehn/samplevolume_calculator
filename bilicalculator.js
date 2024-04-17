function calculateCorrBilirubin() {
  // Get the values from the input fields
  const gemessenesBili = parseFloat(document.querySelector('input[name="Bili"]').value);
  const haemolyse = parseFloat(document.querySelector('input[name="haem"]').value);

  // Check if haemolyse value is outside the valid range
  if (haemolyse < 20 || haemolyse > 120) {
      // Display error message
      const resultDiv = document.getElementById('Bili_Result');
      resultDiv.innerHTML = `<p>Der eingegebene Hämolysewert liegt außerhalb der Grenzen, in der die Berechnung zuverlässig funktioniert.</p>`;
      return; // Exit the function early
  }

  // Define the coefficients for the regression formula
  const coeffX2 = 0.000006; // x² coefficient
  const coeffX = -0.0041; // x coefficient
  const intercept = -0.0856; // Intercept

  // Calculate corrected Bilirubin using the new regression formula
  const corrFactor = (coeffX2 * Math.pow(haemolyse, 2)) + (coeffX * haemolyse) + intercept;
  const biliCorr = gemessenesBili - (corrFactor * gemessenesBili);

  // Display the result
  const resultDiv = document.getElementById('Bili_Result');
  resultDiv.innerHTML = `<p>Korrigiertes direktes Bilirubin: ${biliCorr.toFixed(2)} mg/dl</p>`;
}

