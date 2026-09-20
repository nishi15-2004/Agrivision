// ==========================================
// AgriMitra Weather JavaScript
// ==========================================


// ==========================================
// Get Current Location
// ==========================================

function getLocation() {

    if (!navigator.geolocation) {

        alert("Geolocation is not supported by your browser.");

        return;

    }

    navigator.geolocation.getCurrentPosition(

        function(position) {

            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            window.location.href =
                `/weather?lat=${latitude}&lon=${longitude}`;

        },

        function(error) {

            alert("Unable to fetch your location.");

        }

    );

}



// ==========================================
// Weather Background Theme
// ==========================================

window.addEventListener("load", function () {

    const weatherIcon = document.querySelector(".weather-card img");

    if (!weatherIcon) return;

    const icon = weatherIcon.src;

    document.body.classList.remove(
        "clear",
        "clouds",
        "rain",
        "drizzle",
        "mist",
        "haze",
        "fog",
        "thunderstorm",
        "night"
    );

    // Night Icons

    if (
        icon.includes("01n") ||
        icon.includes("02n") ||
        icon.includes("03n") ||
        icon.includes("04n") ||
        icon.includes("09n") ||
        icon.includes("10n") ||
        icon.includes("11n") ||
        icon.includes("13n") ||
        icon.includes("50n")
    ) {

        document.body.classList.add("night");
        return;

    }

    // Clear

    if (icon.includes("01d")) {

        document.body.classList.add("clear");

    }

    // Clouds

    else if (

        icon.includes("02d") ||
        icon.includes("03d") ||
        icon.includes("04d")

    ) {

        document.body.classList.add("clouds");

    }

    // Rain

    else if (

        icon.includes("09d") ||
        icon.includes("10d")

    ) {

        document.body.classList.add("rain");

    }

    // Thunderstorm

    else if (

        icon.includes("11d")

    ) {

        document.body.classList.add("thunderstorm");

    }

    // Mist

    else if (

        icon.includes("50d")

    ) {

        document.body.classList.add("mist");

    }

});
// ==========================================
// Card Hover Animation
// ==========================================

const cards = document.querySelectorAll(
    ".info-card, .forecast-card, .weather-card"
);

cards.forEach((card) => {

    card.addEventListener("mouseenter", () => {

        card.style.transform = "translateY(-8px)";

        card.style.transition = "0.3s ease";

    });

    card.addEventListener("mouseleave", () => {

        card.style.transform = "translateY(0)";

    });

});


// ==========================================
// Fade-in Animation
// ==========================================

window.addEventListener("DOMContentLoaded", () => {

    document.body.style.opacity = "0";

    document.body.style.transition = "opacity 0.6s ease";

    setTimeout(() => {

        document.body.style.opacity = "1";

    }, 100);

});


// ==========================================
// Forecast Card Animation
// ==========================================

const forecastCards = document.querySelectorAll(".forecast-card");

forecastCards.forEach((card, index) => {

    card.style.opacity = "0";

    card.style.transform = "translateY(20px)";

    setTimeout(() => {

        card.style.transition = "all 0.5s ease";

        card.style.opacity = "1";

        card.style.transform = "translateY(0)";

    }, index * 120);

});


// ==========================================
// Weather Card Pulse Effect
// ==========================================

const weatherCard = document.querySelector(".weather-card");

if (weatherCard) {

    setInterval(() => {

        weatherCard.animate(

            [
                { transform: "scale(1)" },
                { transform: "scale(1.02)" },
                { transform: "scale(1)" }
            ],

            {
                duration: 2500,
                iterations: 1
            }

        );

    }, 4000);

}


// ==========================================
// Search Input Focus Effect
// ==========================================

const cityInput = document.querySelector(".search-box input");

if (cityInput) {

    cityInput.addEventListener("focus", () => {

        cityInput.style.boxShadow =
            "0 0 15px rgba(46,125,50,0.5)";

    });

    cityInput.addEventListener("blur", () => {

        cityInput.style.boxShadow = "none";

    });

}


// ==========================================
// Footer Year (Optional)
// ==========================================

const footer = document.querySelector(".weather-footer");

if (footer) {

    const year = new Date().getFullYear();

    footer.innerHTML += `<p>© ${year} AgriMitra. All Rights Reserved.</p>`;

}