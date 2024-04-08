function calculateCorrBilirubin() {
  // Get the values from the input fields
  const gemessenesBili = parseFloat(document.querySelector('input[name="Bili"]').value);
  const haemolyse = parseFloat(document.querySelector('input[name="haem"]').value);

  // Check if haemolyse value is outside the valid range
  if (haemolyse < 31 || haemolyse > 1000) {
      // Display error message
      const resultDiv = document.getElementById('Bili_Result');
      resultDiv.innerHTML = `<p>Der eingegebene Hämolysewert liegt außerhalb der Grenzen, in der die Berechnung zuverlässig funktioniert.</p>`;
      return; // Exit the function early
  }

  // Calculate corrected Bilirubin using the formula
  const biliCorr = (0.334 * Math.pow(haemolyse, 0.334)) * (Math.pow(gemessenesBili, 1.56) * Math.pow(haemolyse, -0.14));

  // Display the result
  const resultDiv = document.getElementById('Bili_Result');
  resultDiv.innerHTML = `<p>Korrigiertes direktes Bilirubin: ${biliCorr.toFixed(2)} mg/dl</p>`;
}
