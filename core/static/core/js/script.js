  // Obtén las referencias a los elementos del contador
var daysElement = document.getElementById('days');
var hoursElement = document.getElementById('hours');
var minutesElement = document.getElementById('minutes');
var secondsElement = document.getElementById('seconds');

function updateTimer() {
  // Establece la fecha de finalización del contador (puedes ajustarla según tus necesidades)
  var countdownDate = new Date("2023-07-03T23:59:59").getTime();

  // Actualiza el contador cada segundo
  setInterval(function() {
    // Obtiene la fecha y hora actual
    var now = new Date().getTime();

    // Calcula la diferencia entre la fecha de finalización y la fecha actual
    var distance = countdownDate - now;

    // Calcula los días, horas, minutos y segundos restantes
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Actualiza los elementos HTML del contador con los valores correspondientes
    
    daysElement.textContent = days;
    hoursElement.textContent = hours;
    minutesElement.textContent = minutes;
    secondsElement.textContent = seconds;

  }, 1000); // Actualiza cada segundo
}

// Llama a la función updateTimer() para iniciar el contador
updateTimer();



