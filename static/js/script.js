console.log("Welcome to AgriMitra");
const languageSelect = document.getElementById("languageSelect");


languageSelect.addEventListener("change", function(){

    let language = this.value;

    loadLanguage(language);

});



function loadLanguage(language){

fetch(`languages/${language}.json`)

.then(response => response.json())

.then(data => {


document.getElementById("welcome").innerHTML = data.welcome;


document.getElementById("description").innerHTML = data.description;


document.getElementById("explore").innerHTML = data.explore;


document.getElementById("home").innerHTML = data.home;


document.getElementById("weather").innerHTML = data.weather;


document.getElementById("disease").innerHTML = data.disease;


document.getElementById("schemes").innerHTML = data.schemes;


document.getElementById("compensation").innerHTML = data.compensation;


document.getElementById("help").innerHTML = data.help;


});

}
// Get User Location

function getLocation() {

    if (navigator.geolocation) {

        navigator.geolocation.getCurrentPosition(showPosition, showError);

    } else {

        alert("Geolocation is not supported by this browser.");

    }
}

function showPosition(position) {

    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    window.location.href = `/weather?lat=${latitude}&lon=${longitude}`;

}

function showError(error) {

    alert("Location permission denied.");

}