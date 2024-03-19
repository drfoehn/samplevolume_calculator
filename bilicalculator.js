function calculateCorrBilirubin() {
    // Get the values from the input fields
    const gemessenesIndBili = parseFloat(document.querySelector('input[name="indBili"]').value);
    const haemolyse = parseFloat(document.querySelector('input[name="haem"]').value);
  
    // Calculate corrected Bilirubin using the formula
    const biliCorr = (0.334 * Math.pow(haemolyse, 0.334)) * (Math.pow(gemessenesIndBili, 1.56) * Math.pow(haemolyse, -0.14));
  
    // Display the result
    const resultDiv = document.getElementById('indBili_Result');
    resultDiv.innerHTML = `<p>Korrigiertes indirektes Bilirubin: ${biliCorr.toFixed(2)} mg/dl</p>`;
  }