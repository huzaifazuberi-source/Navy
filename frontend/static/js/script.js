/* ============================================================
   script.js  -  Pakistan Navy Eligibility Predictor
   Simple, beginner-friendly JavaScript.
   Handles: mobile menu, form submission, showing the report.
   ============================================================ */


/* ---- 1. Mobile menu toggle (used by the hamburger button) ---- */
function toggleMenu() {
    var links = document.getElementById("navLinks");
    if (links) {
        links.classList.toggle("open");
    }
}


/* ============================================================
   2. CANDIDATE FORM
   When the form is submitted:
   - read all values
   - send them to the backend (/predict) as JSON
   - save the result in the browser
   - go to the prediction page
   ============================================================ */
var form = document.getElementById("candidateForm");

if (form) {
    form.addEventListener("submit", function (event) {
        event.preventDefault();   // stop the normal page reload

        var errorBox = document.getElementById("formError");
        var button = document.getElementById("submitBtn");

        // Collect all the form values into one object.
        var data = {
            candidate_id:           getValue("candidate_id"),
            age:                    getValue("age"),
            gender:                 getValue("gender"),
            height_cm:              getValue("height_cm"),
            weight_kg:              getValue("weight_kg"),
            matric_percentage:      getValue("matric_percentage"),
            inter_percentage:       getValue("inter_percentage"),
            cgpa:                   getValue("cgpa"),
            physical_fitness_score: getValue("physical_fitness_score"),
            medical_status:         getValue("medical_status"),
            marital_status:         getValue("marital_status"),
            city:                   getValue("city"),
            computer_skills:        getValue("computer_skills"),
            leadership_score:       getValue("leadership_score"),
            communication_score:    getValue("communication_score"),
            branch_preference:      getValue("branch_preference")
        };

        // Show a "please wait" state on the button.
        button.innerText = "Predicting...";
        button.disabled = true;

        // Send the data to the backend.
        fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        })
        .then(function (response) { return response.json(); })
        .then(function (result) {
            if (result.error) {
                // Show the error message returned by the backend.
                errorBox.innerText = result.error;
                errorBox.style.display = "block";
                button.innerText = "Predict Eligibility";
                button.disabled = false;
                return;
            }
            // Save both the input and the result for the next page.
            sessionStorage.setItem("predictionInput", JSON.stringify(data));
            sessionStorage.setItem("predictionResult", JSON.stringify(result));
            // Go to the result page.
            window.location.href = "/prediction";
        })
        .catch(function () {
            errorBox.innerText = "Something went wrong. Please try again.";
            errorBox.style.display = "block";
            button.innerText = "Predict Eligibility";
            button.disabled = false;
        });
    });
}

/* Small helper: read the value of an input by its id. */
function getValue(id) {
    var el = document.getElementById(id);
    return el ? el.value : "";
}


/* ============================================================
   3. PREDICTION PAGE
   Read the saved result and fill in the report.
   ============================================================ */
var statusBanner = document.getElementById("statusBanner");

if (statusBanner) {
    var result = JSON.parse(sessionStorage.getItem("predictionResult") || "null");
    var input  = JSON.parse(sessionStorage.getItem("predictionInput")  || "null");

    if (!result) {
        // If there is no saved result, send the user back to the form.
        window.location.href = "/form";
    } else {
        showReport(result, input);
    }
}

function showReport(result, input) {

    /* ---- Status banner (green if eligible, red if not) ---- */
    var statusText = document.getElementById("statusText");
    statusText.innerText = result.predicted_status;
    if (result.predicted_status === "Eligible") {
        statusBanner.classList.add("status-eligible");
    } else {
        statusBanner.classList.add("status-not-eligible");
    }

    /* ---- Eligibility progress bar ---- */
    document.getElementById("eligValue").innerText = result.eligibility_percentage + "%";
    /* timeout lets the bar animate from 0 to the value */
    setTimeout(function () {
        document.getElementById("eligBar").style.width = result.eligibility_percentage + "%";
    }, 100);

    /* ---- Confidence progress bar ---- */
    document.getElementById("confValue").innerText = result.confidence_percentage + "%";
    setTimeout(function () {
        document.getElementById("confBar").style.width = result.confidence_percentage + "%";
    }, 100);

    /* ---- Recommended branches (as tags) ---- */
    var branchBox = document.getElementById("branchTags");
    result.recommended_branches.forEach(function (branch) {
        var span = document.createElement("span");
        span.className = "tag";
        span.innerText = branch;
        branchBox.appendChild(span);
    });

    /* ---- Strengths / Weaknesses / Suggestions lists ---- */
    fillList("strengthsList", result.strengths, "No major strengths detected.");
    fillList("weaknessList", result.weaknesses, "No major weaknesses detected.");
    fillList("suggestionList", result.suggestions, "No suggestions needed.");

    /* ---- Detailed candidate report table ---- */
    if (input) {
        var rows = [
            ["Candidate ID", input.candidate_id || "—"],
            ["Age", input.age],
            ["Gender", input.gender],
            ["Height (cm)", input.height_cm],
            ["Weight (kg)", input.weight_kg],
            ["Matric (%)", input.matric_percentage],
            ["Intermediate (%)", input.inter_percentage],
            ["CGPA", input.cgpa],
            ["Physical Fitness", input.physical_fitness_score],
            ["Medical Status", input.medical_status],
            ["Marital Status", input.marital_status],
            ["City", input.city],
            ["Computer Skills", input.computer_skills],
            ["Leadership Score", input.leadership_score],
            ["Communication Score", input.communication_score],
            ["Branch Preference", input.branch_preference],
            ["Predicted Status", result.predicted_status],
            ["Eligibility %", result.eligibility_percentage + "%"],
            ["Confidence %", result.confidence_percentage + "%"]
        ];

        var tbody = document.querySelector("#reportTable tbody");
        rows.forEach(function (row) {
            var tr = document.createElement("tr");
            tr.innerHTML = "<td style='font-weight:600;width:40%'>" + row[0] +
                           "</td><td>" + row[1] + "</td>";
            tbody.appendChild(tr);
        });
    }
}

/* Helper: fill a <ul> with list items, or show a default message. */
function fillList(listId, items, emptyMessage) {
    var list = document.getElementById(listId);
    if (!items || items.length === 0) {
        var li = document.createElement("li");
        li.innerText = emptyMessage;
        list.appendChild(li);
        return;
    }
    items.forEach(function (text) {
        var li = document.createElement("li");
        li.innerText = text;
        list.appendChild(li);
    });
}
