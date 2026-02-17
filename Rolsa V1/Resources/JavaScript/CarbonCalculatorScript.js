document.addEventListener("DOMContentLoaded", function() {
  const calculateButton = document.getElementById("calculate"); //sets variable for calculating 
  const distanceInput = document.getElementById("distance"); //sets variable for distance 
  const emissionInput = document.getElementById("emission"); //sets variable for emission factor
  const carbonScore = document.getElementById("carbon-score"); //sets variable for carbon score display

  calculateButton.addEventListener("click", function() {
    const distance = parseFloat(distanceInput.value); //gets distance value
    const emissionFactor = parseFloat(emissionInput.value); //gets emission factor value

    if (!isNaN(distance) && !isNaN(emissionFactor)) { //checks to make sure they are filled
      const carbon = distance * emissionFactor; 
      carbonScore.textContent = "Carbon Score: " + carbon.toFixed(2) + " CO2e";
    } else {
      carbonScore.textContent = "Carbon Score: Invalid Input";
    }
  });
});
