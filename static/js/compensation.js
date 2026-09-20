// ==========================================
// AGRIVISION COMPENSATION JAVASCRIPT
// ==========================================


// ==========================================
// LOAD STATES
// ==========================================

async function loadStates() {

    const stateSelect = document.getElementById("state");

    try {

        const response = await fetch(
            "/api/compensation/states"
        );

        const data = await response.json();

        stateSelect.innerHTML =
            '<option value="">Select State / UT</option>';

        data.states.forEach(state => {

            const option =
                document.createElement("option");

            option.value = state.id;
            option.textContent = state.name;

            stateSelect.appendChild(option);

        });

    } catch (error) {

        stateSelect.innerHTML =
            '<option value="">Unable to load states</option>';

        showError(
            "Unable to load states. Please restart the Flask server."
        );
    }
}


// ==========================================
// LOAD DISTRICTS
// ==========================================

async function loadDistricts() {

    const stateId =
        document.getElementById("state").value;

    const districtSelect =
        document.getElementById("district");

    districtSelect.innerHTML =
        '<option value="">Loading districts...</option>';

    if (!stateId) {

        districtSelect.innerHTML =
            '<option value="">Select State First</option>';

        return;
    }

    try {

        const response = await fetch(
            `/api/compensation/districts/${stateId}`
        );

        const data = await response.json();

        districtSelect.innerHTML =
            '<option value="">Select District</option>';

        data.districts.forEach(district => {

            const option =
                document.createElement("option");

            option.value = district.id;
            option.textContent = district.name;

            districtSelect.appendChild(option);

        });

    } catch (error) {

        districtSelect.innerHTML =
            '<option value="">Unable to load districts</option>';

        showError(
            "Unable to load districts."
        );
    }
}


// ==========================================
// LOAD CROPS
// ==========================================

async function loadCrops() {

    const cropSelect =
        document.getElementById("crop");

    try {

        const response = await fetch(
            "/api/compensation/crops"
        );

        const data = await response.json();

        cropSelect.innerHTML =
            '<option value="">Select Crop</option>';

        let currentCategory = null;
        let group = null;

        data.crops.forEach(crop => {

            if (crop.category !== currentCategory) {

                currentCategory = crop.category;

                group =
                    document.createElement("optgroup");

                group.label = crop.category;

                cropSelect.appendChild(group);
            }

            const option =
                document.createElement("option");

            option.value = crop.id;

            option.textContent = crop.name;

            group.appendChild(option);

        });

    } catch (error) {

        cropSelect.innerHTML =
            '<option value="">Unable to load crops</option>';

        showError(
            "Unable to load crops."
        );
    }
}


// ==========================================
// LOAD DAMAGE TYPES
// ==========================================

async function loadDamageTypes() {

    const damageSelect =
        document.getElementById("damage");

    try {

        const response = await fetch(
            "/api/compensation/damage-types"
        );

        const data = await response.json();

        damageSelect.innerHTML =
            '<option value="">Select Damage Type</option>';

        data.damage_types.forEach(damage => {

            const option =
                document.createElement("option");

            option.value = damage.id;

            option.textContent = damage.name;

            damageSelect.appendChild(option);

        });

    } catch (error) {

        damageSelect.innerHTML =
            '<option value="">Unable to load damage types</option>';

        showError(
            "Unable to load damage types."
        );
    }
}


// ==========================================
// DAMAGE CHANGE
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const damageSelect =
            document.getElementById("damage");

        damageSelect.addEventListener(
            "change",
            function () {

                if (this.value) {

                    loadActionGuide(
                        this.value
                    );

                } else {

                    resetActionGuide();

                }

            }
        );

    }
);


// ==========================================
// LOAD ACTION GUIDE
// ==========================================

async function loadActionGuide(
    damageTypeId
) {

    const title =
        document.getElementById("action-title");

    const subtitle =
        document.getElementById("action-subtitle");

    const icon =
        document.getElementById("action-icon");

    const firstSteps =
        document.getElementById("first-steps");

    const evidence =
        document.getElementById("evidence-list");

    const report =
        document.getElementById("report-text");


    title.textContent =
        "Loading guidance...";

    subtitle.textContent =
        "Please wait.";

    firstSteps.innerHTML =
        "<li>Loading...</li>";

    evidence.innerHTML =
        "<li>Loading...</li>";

    report.textContent =
        "Loading...";


    try {

        const response = await fetch(
            `/api/compensation/action-guide/${damageTypeId}`
        );

        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error || "Guide unavailable"
            );

        }


        const guide = data.guide;


        // TITLE

        icon.textContent =
            guide.icon;

        title.textContent =
            guide.title;

        subtitle.textContent =
            "Here is what you should do after this type of crop damage.";


        // FIRST STEPS

        firstSteps.innerHTML = "";

        guide.first_steps.forEach(step => {

            const li =
                document.createElement("li");

            li.textContent =
                step;

            firstSteps.appendChild(li);

        });


        // EVIDENCE

        evidence.innerHTML = "";

        guide.evidence.forEach(item => {

            const li =
                document.createElement("li");

            li.textContent =
                item;

            evidence.appendChild(li);

        });


        // REPORTING

        report.textContent =
            guide.report;


        // SCROLL TO GUIDE

        document.getElementById(
            "action-guide"
        ).scrollIntoView({
            behavior: "smooth",
            block: "center"
        });


    } catch (error) {

        title.textContent =
            "Guidance unavailable";

        subtitle.textContent =
            "Please try again.";

        firstSteps.innerHTML =
            "<li>Unable to load guidance.</li>";

        evidence.innerHTML =
            "<li>Please verify the selected damage type.</li>";

        report.textContent =
            "Please check the applicable official government or insurance process.";

    }
}


// ==========================================
// RESET ACTION GUIDE
// ==========================================

function resetActionGuide() {

    document.getElementById(
        "action-icon"
    ).textContent = "🚨";

    document.getElementById(
        "action-title"
    ).textContent =
        "What Should You Do First?";

    document.getElementById(
        "action-subtitle"
    ).textContent =
        "Select a damage type to get step-by-step guidance.";

    document.getElementById(
        "first-steps"
    ).innerHTML =
        "<li>Select a damage type above to see what you should do first.</li>";

    document.getElementById(
        "evidence-list"
    ).innerHTML =
        "<li>Photos and documents may be useful for assessment.</li>";

    document.getElementById(
        "report-text"
    ).textContent =
        "Select a damage type to see reporting guidance.";
}


// ==========================================
// FIND COMPENSATION
// ==========================================

async function findCompensation() {

    const state =
        document.getElementById("state");

    const district =
        document.getElementById("district");

    const crop =
        document.getElementById("crop");

    const damage =
        document.getElementById("damage");


    const stateId = state.value;
    const districtId = district.value;
    const cropId = crop.value;
    const damageId = damage.value;


    // VALIDATION

    if (!stateId ||
        !districtId ||
        !cropId ||
        !damageId) {

        showError(
            "Please select State, District, Crop and Damage Type."
        );

        return;
    }


    hideError();


    try {

       const url =
    `/api/compensation?state_id=${stateId}&district_id=${districtId}&crop_id=${cropId}&damage_type_id=${damageId}`;


        const response =
            await fetch(url);


        const data =
            await response.json();


        if (!response.ok) {

            showError(
                data.error ||
                "Unable to find compensation information."
            );

            return;
        }


        displayCompensation(
            data.compensation
        );


    } catch (error) {

        showError(
            "Unable to connect to the compensation service."
        );

    }
}


// ==========================================
// DISPLAY COMPENSATION
// ==========================================

function displayCompensation(
    compensation
) {

    const result =
        document.getElementById("result");


    if (!compensation) {

        result.style.display =
            "block";

        document.getElementById(
            "show-location"
        ).textContent =
            getSelectedLocation();

        document.getElementById(
            "show-crop"
        ).textContent =
            getSelectedText("crop");

        document.getElementById(
            "show-damage"
        ).textContent =
            getSelectedText("damage");

        document.getElementById(
            "show-scheme"
        ).textContent =
            "No specific record found";

        document.getElementById(
            "show-eligibility"
        ).textContent =
            "No specific information available.";

        document.getElementById(
            "show-coverage"
        ).textContent =
            "Please verify applicable government/insurance rules.";

        document.getElementById(
            "show-claim"
        ).textContent =
            "Contact the applicable authority or insurer.";

        result.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

        return;
    }


    result.style.display =
        "block";


    document.getElementById(
        "show-location"
    ).textContent =
        `${compensation.state_name}, ${compensation.district_name}`;


    document.getElementById(
        "show-crop"
    ).textContent =
        compensation.crop_name || getSelectedText("crop");


    document.getElementById(
        "show-damage"
    ).textContent =
        compensation.damage_type_name;


    document.getElementById(
        "show-scheme"
    ).textContent =
        compensation.scheme_name || "-";


    document.getElementById(
        "show-eligibility"
    ).textContent =
        compensation.eligibility || "-";


    document.getElementById(
        "show-coverage"
    ).textContent =
        compensation.coverage || "-";


    document.getElementById(
        "show-claim"
    ).textContent =
        compensation.claim_process || "-";


    result.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


// ==========================================
// SELECT DAMAGE FROM DAMAGE CARD
// ==========================================

function selectDamage(damageId) {

    const damageSelect =
        document.getElementById("damage");

    damageSelect.value =
        damageId;


    loadActionGuide(
        damageId
    );

    document.getElementById(
        "action-guide"
    ).scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}


// ==========================================
// SELECTED TEXT
// ==========================================

function getSelectedText(
    elementId
) {

    const element =
        document.getElementById(elementId);

    if (!element ||
        !element.value) {

        return "-";
    }

    return element.options[
        element.selectedIndex
    ].text;
}


// ==========================================
// LOCATION TEXT
// ==========================================

function getSelectedLocation() {

    const state =
        getSelectedText("state");

    const district =
        getSelectedText("district");

    return `${state}, ${district}`;
}


// ==========================================
// ERROR
// ==========================================

function showError(message) {

    const error =
        document.getElementById(
            "error-message"
        );

    error.textContent =
        message;

    error.style.display =
        "block";
}


function hideError() {

    const error =
        document.getElementById(
            "error-message"
        );

    error.style.display =
        "none";
}


// ==========================================
// INITIAL LOAD
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadStates();

        loadCrops();

        loadDamageTypes();

    }
);