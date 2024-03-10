////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// HELPER FUNCTIONS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Set the color of toggle menu buttons when clicked
 * @param toggleMenu
 */
function toggleMenuColors(toggleMenu)
{
    document.querySelectorAll(toggleMenu + " .btn").forEach((button) =>
    {
        button.addEventListener("click", (event) =>
        {
            document.querySelectorAll(toggleMenu + " .btn").forEach((btn) =>
            {
                btn.classList.remove("selected");
            });
            event.currentTarget.classList.add("selected");
        });
    });
}

/**
 * Get the number of height zones
 * @returns {Promise<unknown>}
 */
function getNumHeightZones()
{
    return new Promise((resolve, reject) =>
    {
        window.api
            .invoke("get-connection-address").then((connectionAddress) =>
        {
            window.api
                .invoke("get-token") // Retrieve the token
                .then((token) =>
                {
                    const myHeaders = new Headers();
                    myHeaders.append("Accept", "application/json");
                    myHeaders.append("Authorization", `Bearer ${token}`);

                    const requestOptions = {
                        method: "POST",
                        headers: myHeaders,
                        redirect: "follow",
                    };

                    fetch(`${connectionAddress}/get_height_zones`, requestOptions)
                        .then((response) => response.json())
                        .then((result) =>
                        {
                            let heightZoneData = JSON.parse(result);
                            let numHeightZones = Object.keys(heightZoneData).length;
                            resolve(numHeightZones); // Resolve the promise with numHeightZones
                        })
                        .catch((error) =>
                        {
                            console.error(error);
                            reject(error);
                        });
                });
        });
    });
}

/**
 * Collect the wind load inputs for a given height zone
 * @param zone_num
 * @returns {{exposureFactor: string, ceIntermediate, internalPressureCategory: string, topographicFactor: *}}
 */
function getWindLoadInputs(zone_num)
{
    let topographicFactor = document.getElementById(
        `topographic-factor-hz-${zone_num}`,
    ).value;
    let exposureFactor = document.querySelector(
        `input[name="exposure-factor-selection-hz-${zone_num}"]:checked`,
    ).id;
    let ceIntermediate;

    // if open
    if (exposureFactor === `exposure-factor-open-option-hz-${zone_num}`)
    {
        exposureFactor = "open";
    }

    // if rough
    else if (exposureFactor === `exposure-factor-rough-option-hz-${zone_num}`)
    {
        exposureFactor = "rough";
    }
    else if (
        exposureFactor === `exposure-factor-intermediate-option-hz-${zone_num}`
    )
    {
        exposureFactor = "intermediate";
        ceIntermediate = document.getElementById(
            `ce-intermediate-hz-${zone_num}`,
        ).value;
    }

    let internalPressureCategory = document.querySelector(
        `input[name="internal-pressure-category-selection-hz-${zone_num}"]:checked`,
    ).id;

    // if enclosed
    if (
        internalPressureCategory ===
        `internal-pressure-category-enclosed-option-hz-${zone_num}`
    )
    {
        internalPressureCategory = "enclosed";
    }
    else if (
        internalPressureCategory ===
        `internal-pressure-category-partially-enclosed-option-hz-${zone_num}`
    )
    {
        internalPressureCategory = "partially_enclosed";
    }
    else if (
        internalPressureCategory ===
        `internal-pressure-category-large-openings-option-hz-${zone_num}`
    )
    {
        internalPressureCategory = "large_openings";
    }

    return {
        topographicFactor,
        exposureFactor,
        ceIntermediate,
        internalPressureCategory,
    };
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// CREATE COMPONENT
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Create the wind load component
 * @param zone_num
 * @returns {string}
 */
function createWindLoadComponent(zone_num)
{
    return `
    <hr>
    <h5 id="wind-load-component-hz-${zone_num}">Height Zone ${zone_num}</h5>
    <hr>
    <div class="row gx-5 ">
        <div class="col-md-6">
        <div class="mb-3">
            <label for="topographic-factor-hz-${zone_num}">Topographic Factor (Ct)</label>
            <p>By default the topographic factor is 1</p>
            <input type="number" id="topographic-factor-hz-${zone_num}" class="form-control" value="1"/>
        </div>
        <div class="mb-3">
            <label for="exposure-factor-selection-hz-${zone_num}">Exposure Factor (Ce)</label>
            <br>
            <div class="btn-group btn-group-toggle" id="exposure-factor-selection-hz-${zone_num}" data-toggle="buttons">
                <label class="btn btn-secondary" id="exposure-factor-open-option-button-hz-${zone_num}">
                    <input type="radio" name="exposure-factor-selection-hz-${zone_num}" id="exposure-factor-open-option-hz-${zone_num}" autocomplete="off"> Open
                </label>
                <label class="btn btn-secondary" id="exposure-factor-rough-option-button-hz-${zone_num}">
                    <input type="radio" name="exposure-factor-selection-hz-${zone_num}" id="exposure-factor-rough-option-hz-${zone_num}" autocomplete="off"> Rough
                </label>
                <label class="btn btn-secondary" id="exposure-factor-intermediate-option-button-hz-${zone_num}">
                    <input type="radio" name="exposure-factor-selection-hz-${zone_num}" id="exposure-factor-intermediate-option-hz-${zone_num}" autocomplete="off"> Intermediate
                </label>
            </div>
        </div>
        <div class="mb-3">
            <input type="number" id="ce-intermediate-hz-${zone_num}" class="form-control"/>
        </div>
        <div class="mb-3">
            <label>Gust Factor (Cg)</label>
            <p>2.5</p>
        </div>
        <div class="mb-3">
            <label for="internal-pressure-category-selection-hz-${zone_num}">Internal Pressure Category</label>
            <br>
            <div class="btn-group btn-group-toggle" id="internal-pressure-category-selection-hz-${zone_num}" data-toggle="buttons">
                <label class="btn btn-secondary" id="internal-pressure-category-enclosed-option-button-hz-${zone_num}">
                    <input type="radio" name="internal-pressure-category-selection-hz-${zone_num}" id="internal-pressure-category-enclosed-option-hz-${zone_num}" autocomplete="off"> Enclosed
                </label>
                <label class="btn btn-secondary" id="internal-pressure-category-partially-enclosed-option-button-hz-${zone_num}">
                    <input type="radio" name="internal-pressure-category-selection-hz-${zone_num}" id="internal-pressure-category-partially-enclosed-option-hz-${zone_num}" autocomplete="off"> Partially Enclosed
                </label>
                <label class="btn btn-secondary" id="internal-pressure-category-large-openings-option-button-hz-${zone_num}">
                    <input type="radio" name="internal-pressure-category-selection-hz-${zone_num}" id="internal-pressure-category-large-openings-option-hz-${zone_num}" autocomplete="off"> Large Openings
                </label>
            </div>
        </div>
        </div>
        <div class="col-md-6">
            <label for="wind-load-table-hz-${zone_num}">Calculated Wind Load for Different Zones</label>
            <table id="wind-load-table-hz-${zone_num}" class="table">
                <colgroup>
                    <col span="2">
                    <col span="2">
                </colgroup>
                <thead>
                    <tr>
                        <th rowspan="2">Zone</th>
                        <th rowspan="2">Zone Name</th>
                        <th colspan="2" style="text-align:center;">Wind Load (kPa)</th>
                    </tr>
                    <tr>
                        <th>POS</th>
                        <th>NEG</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>1</td>
                        <td>Roof_interior</td>
                        <td id="pos-1-hz-${zone_num}">NA</td>
                        <td id="neg-1-hz-${zone_num}">NA</td>
                    </tr>
                    <tr>
                        <td>2</td>
                        <td>Roof_edge</td>
                        <td id="pos-2-hz-${zone_num}">NA</td>
                        <td id="neg-2-hz-${zone_num}">NA</td>
                    </tr>
                    <tr>
                        <td>3</td>
                        <td>Roof_corner</td>
                        <td id="pos-3-hz-${zone_num}">NA</td>
                        <td id="neg-3-hz-${zone_num}">NA</td>
                    </tr>
                    <tr>
                        <td>4</td>
                        <td>Wall_centre</td>
                        <td id="pos-4-hz-${zone_num}">NA</td>
                        <td id="neg-4-hz-${zone_num}">NA</td>
                    </tr>
                    <tr>
                        <td>5</td>
                        <td>Wall_corner</td>
                        <td id="pos-5-hz-${zone_num}">NA</td>
                        <td id="neg-5-hz-${zone_num}">NA</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    `;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// GET LOADS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function doneLoadingWindLoads(zoneNum)
{
    // remove skeleton-loader class from all the wind load inputs and enable the radio buttons
    document
        .getElementById(`topographic-factor-hz-${zoneNum}`)
        .classList.remove("skeleton-loader");
    document.getElementById(
        `exposure-factor-open-option-hz-${zoneNum}`,
    ).disabled = false;
    document.getElementById(
        `exposure-factor-rough-option-hz-${zoneNum}`,
    ).disabled = false;
    document.getElementById(
        `exposure-factor-intermediate-option-hz-${zoneNum}`,
    ).disabled = false;
    document
        .getElementById(
            `exposure-factor-open-option-button-hz-${zoneNum}`,
        )
        .classList.remove("skeleton-loader");
    document
        .getElementById(
            `exposure-factor-rough-option-button-hz-${zoneNum}`,
        )
        .classList.remove("skeleton-loader");
    document
        .getElementById(
            `exposure-factor-intermediate-option-button-hz-${zoneNum}`,
        )
        .classList.remove("skeleton-loader");
    document.getElementById(
        `internal-pressure-category-enclosed-option-hz-${zoneNum}`,
    ).disabled = false;
    document.getElementById(
        `internal-pressure-category-partially-enclosed-option-hz-${zoneNum}`,
    ).disabled = false;
    document.getElementById(
        `internal-pressure-category-large-openings-option-hz-${zoneNum}`,
    ).disabled = false;
    document
        .getElementById(
            `internal-pressure-category-enclosed-option-button-hz-${zoneNum}`,
        )
        .classList.remove("skeleton-loader");
    document
        .getElementById(
            `internal-pressure-category-partially-enclosed-option-button-hz-${zoneNum}`,
        )
        .classList.remove("skeleton-loader");
    document
        .getElementById(
            `internal-pressure-category-large-openings-option-button-hz-${zoneNum}`,
        )
        .classList.remove("skeleton-loader");
    document
        .getElementById(`ce-intermediate-hz-${zoneNum}`)
        .classList.remove("skeleton-loader");

    for (let j = 1; j <= 5; j++)
    {
        document
            .getElementById(`pos-${j}-hz-${zoneNum}`)
            .classList.remove("skeleton-loader");
        document
            .getElementById(`neg-${j}-hz-${zoneNum}`)
            .classList.remove("skeleton-loader");
    }

    document.getElementById('save-button').disabled = false;
}

function startLoadingWindLoads(i)
{
    // add skeleton-loader class to all the wind load inputs
    document
        .getElementById(`topographic-factor-hz-${i}`)
        .classList.add("skeleton-loader");

    // disable associated radio buttons
    document.getElementById(
        `exposure-factor-open-option-hz-${i}`,
    ).disabled = true;
    document.getElementById(
        `exposure-factor-rough-option-hz-${i}`,
    ).disabled = true;
    document.getElementById(
        `exposure-factor-intermediate-option-hz-${i}`,
    ).disabled = true;

    // add skeleton-loader to parent secondary button
    document
        .getElementById(`exposure-factor-open-option-button-hz-${i}`)
        .classList.add("skeleton-loader");
    document
        .getElementById(`exposure-factor-rough-option-button-hz-${i}`)
        .classList.add("skeleton-loader");
    document
        .getElementById(`exposure-factor-intermediate-option-button-hz-${i}`)
        .classList.add("skeleton-loader");

    // disable radio buttons of internal pressure category
    document.getElementById(
        `internal-pressure-category-enclosed-option-hz-${i}`,
    ).disabled = true;
    document.getElementById(
        `internal-pressure-category-partially-enclosed-option-hz-${i}`,
    ).disabled = true;
    document.getElementById(
        `internal-pressure-category-large-openings-option-hz-${i}`,
    ).disabled = true;

    // add skeleton loader to secondary buttons of internal pressure category
    document
        .getElementById(
            `internal-pressure-category-enclosed-option-button-hz-${i}`,
        )
        .classList.add("skeleton-loader");
    document
        .getElementById(
            `internal-pressure-category-partially-enclosed-option-button-hz-${i}`,
        )
        .classList.add("skeleton-loader");
    document
        .getElementById(
            `internal-pressure-category-large-openings-option-button-hz-${i}`,
        )
        .classList.add("skeleton-loader");

    document
        .getElementById(`ce-intermediate-hz-${i}`)
        .classList.add("skeleton-loader");

    // add skeleton-loader to pos and neg cells
    for (let j = 1; j <= 5; j++)
    {
        document
            .getElementById(`pos-${j}-hz-${i}`)
            .classList.add("skeleton-loader");
        document
            .getElementById(`neg-${j}-hz-${i}`)
            .classList.add("skeleton-loader");
    }

    document.getElementById('save-button').disabled = true;
}

/**
 * Get the wind loads
 */
function getWindLoads()
{
    window.api
        .invoke("get-connection-address").then((connectionAddress) =>
    {
        window.api
            .invoke("get-token") // Retrieve the token
            .then((token) =>
            {
                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");
                myHeaders.append("Accept", "application/json");
                myHeaders.append("Authorization", `Bearer ${token}`);

                // count the number of height zones by the number of height zones wind load headers
                const numHeightZones = document.querySelectorAll(
                    'h5[id^="wind-load-component-hz-"]',
                ).length;

                let ctValues = [];
                let exposureFactorValues = [];
                let manualCeCeiValues = [];
                let internalPressureCategoryValues = [];

                for (let i = 1; i <= numHeightZones; i++)
                {
                    let inputs = getWindLoadInputs(i);
                    ctValues.push(inputs.topographicFactor);
                    exposureFactorValues.push(inputs.exposureFactor);
                    manualCeCeiValues.push(inputs.ceIntermediate);
                    internalPressureCategoryValues.push(inputs.internalPressureCategory);

                    startLoadingWindLoads(i);
                }

                const raw = JSON.stringify(
                    {
                        ct: ctValues,
                        exposure_factor: exposureFactorValues,
                        manual_ce_cei: manualCeCeiValues,
                        internal_pressure_category: internalPressureCategoryValues,
                    });

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    body: raw,
                    redirect: "follow",
                };

                fetch(`${connectionAddress}/set_wind_load`, requestOptions)
                    .then((response) => response.json())
                    .then((result) =>
                    {
                        const myHeaders = new Headers();
                        myHeaders.append("Accept", "application/json");
                        myHeaders.append("Authorization", `Bearer ${token}`);

                        const requestOptions = {
                            method: "POST",
                            headers: myHeaders,
                            redirect: "follow",
                        };

                        fetch(`${connectionAddress}/get_height_zones`, requestOptions)
                            .then((response) => response.json())
                            .then((result) =>
                            {
                                let heightZoneData = JSON.parse(result);

                                for (let zoneNum in heightZoneData)
                                {
                                    let innerZones = heightZoneData[zoneNum]["wind_load"]["zones"];
                                    for (let innerZoneNum in innerZones)
                                    {
                                        let innerZone = innerZones[innerZoneNum];

                                        switch (innerZone["name"])
                                        {
                                            case "roof_interior":
                                                document.getElementById(`pos-1-hz-${zoneNum}`).innerHTML =
                                                    innerZone["pressure"]["pos_uls"];
                                                document.getElementById(`neg-1-hz-${zoneNum}`).innerHTML =
                                                    innerZone["pressure"]["neg_uls"];
                                                break;
                                            case "roof_edge":
                                                document.getElementById(`pos-2-hz-${zoneNum}`).innerHTML =
                                                    innerZone["pressure"]["pos_uls"];
                                                document.getElementById(`neg-2-hz-${zoneNum}`).innerHTML =
                                                    innerZone["pressure"]["neg_uls"];
                                                break;
                                            case "roof_corner":
                                                document.getElementById(`pos-3-hz-${zoneNum}`).innerHTML =
                                                    innerZone["pressure"]["pos_uls"];
                                                document.getElementById(`neg-3-hz-${zoneNum}`).innerHTML =
                                                    innerZone["pressure"]["neg_uls"];
                                                break;
                                            case "wall_centre":
                                                document.getElementById(`pos-4-hz-${zoneNum}`).innerHTML =
                                                    innerZone["pressure"]["pos_uls"];
                                                document.getElementById(`neg-4-hz-${zoneNum}`).innerHTML =
                                                    innerZone["pressure"]["neg_uls"];
                                                break;
                                            case "wall_corner":
                                                document.getElementById(`pos-5-hz-${zoneNum}`).innerHTML =
                                                    innerZone["pressure"]["pos_uls"];
                                                document.getElementById(`neg-5-hz-${zoneNum}`).innerHTML =
                                                    innerZone["pressure"]["neg_uls"];
                                                break;
                                        }
                                    }
                                    doneLoadingWindLoads(zoneNum);
                                }
                            })
                            .catch((error) =>
                            {
                                console.error(error);
                                const numHeightZones = document.querySelectorAll(
                                    'h5[id^="wind-load-component-hz-"]',
                                ).length;
                                for (let i = 1; i <= numHeightZones; i++)
                                {
                                    doneLoadingWindLoads(i);
                                }
                            });
                    })
                    .catch((error) => console.error(error));
            });
    });


}

function startLoadingSeismicLoads()
{
    document.getElementById('amplification-factor').classList.add('skeleton-loader');
    document.getElementById('response-modification-factor').classList.add('skeleton-loader');
    document.getElementById('component-factor').classList.add('skeleton-loader');

    for (let i = 1; i < document.getElementById('seismic-load-table').rows.length - 1; i++)
    {
        document.getElementById(`sp-hz-${i}`).classList.add('skeleton-loader');
        document.getElementById(`vp-hz-${i}`).classList.add('skeleton-loader');
    }

    document.getElementById('save-button').disabled = true;
}

function doneLoadingSeismicLoads()
{
    document.getElementById('amplification-factor').classList.remove('skeleton-loader');
    document.getElementById('response-modification-factor').classList.remove('skeleton-loader');
    document.getElementById('component-factor').classList.remove('skeleton-loader');

    for (let i = 1; i < document.getElementById('seismic-load-table').rows.length - 1; i++)
    {
        document.getElementById(`sp-hz-${i}`).classList.remove('skeleton-loader');
        document.getElementById(`vp-hz-${i}`).classList.remove('skeleton-loader');
    }

    document.getElementById('save-button').disabled = false;
}

/**
 * Get the seismic loads
 */
function getSeismicLoads()
{
    window.api
        .invoke("get-connection-address").then((connectionAddress) =>
    {
        window.api
            .invoke("get-token") // Retrieve the token
            .then((token) =>
            {
                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");
                myHeaders.append("Accept", "application/json");
                myHeaders.append("Authorization", `Bearer ${token}`);

                const raw = JSON.stringify(
                    {
                        ar: parseFloat(document.getElementById("amplification-factor").value),
                        rp: parseFloat(
                            document.getElementById("response-modification-factor").value,
                        ),
                        cp: parseFloat(document.getElementById("component-factor").value),
                    });

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    body: raw,
                    redirect: "follow",
                };

                fetch(`${connectionAddress}/set_seismic_load`, requestOptions)
                    .then((response) => response.json())
                    .then((result) =>
                    {
                        const myHeaders = new Headers();
                        myHeaders.append("Accept", "application/json");
                        myHeaders.append("Authorization", `Bearer ${token}`);

                        const requestOptions = {
                            method: "POST",
                            headers: myHeaders,
                            redirect: "follow",
                        };

                        startLoadingSeismicLoads();

                        fetch(`${connectionAddress}/get_height_zones`, requestOptions)
                            .then((response) => response.json())
                            .then((result) =>
                            {
                                let heightZoneData = JSON.parse(result);

                                for (let zoneNum in heightZoneData)
                                {
                                    let seismicLoad = heightZoneData[zoneNum]["seismic_load"];
                                    document.getElementById(`sp-hz-${zoneNum}`).innerHTML =
                                        seismicLoad["sp"];
                                    document.getElementById(`vp-hz-${zoneNum}`).innerHTML =
                                        seismicLoad["vp"];
                                }

                                doneLoadingSeismicLoads();
                            })
                            .catch((error) => {
                                doneLoadingSeismicLoads();
                            });
                    })
                    .catch((error) => console.error(error));
            });
    });

}

function startLoadingSnowLoads()
{
    document.getElementById('upwind-accumulation-factor').classList.add('skeleton-loader');
    document.getElementById('downwind-accumulation-factor').classList.add('skeleton-loader');
    document.getElementById('snow-load-upwind-uls').classList.add('skeleton-loader');
    document.getElementById('snow-load-downwind-uls').classList.add('skeleton-loader');

    document.getElementById('save-button').disabled = true;
}

function doneLoadingSnowLoads()
{
    document.getElementById('upwind-accumulation-factor').classList.remove('skeleton-loader');
    document.getElementById('downwind-accumulation-factor').classList.remove('skeleton-loader');
    document.getElementById('snow-load-upwind-uls').classList.remove('skeleton-loader');
    document.getElementById('snow-load-downwind-uls').classList.remove('skeleton-loader');

    document.getElementById('save-button').disabled = false;
}

/**
 * Get the snow load
 */
function getSnowLoad()
{
    window.api
        .invoke("get-connection-address").then((connectionAddress) =>
    {
        window.api
            .invoke("get-token") // Retrieve the token
            .then((token) =>
            {
                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");
                myHeaders.append("Accept", "application/json");
                myHeaders.append("Authorization", `Bearer ${token}`);

                const numHeightZones = document.querySelectorAll(
                    'h5[id^="wind-load-component-hz-"]',
                ).length;
                let exposureFactorSelection = document
                    .getElementById(`exposure-factor-selection-hz-${numHeightZones}`)
                    .querySelector(".selected").id;

                // if open
                if (
                    exposureFactorSelection ===
                    `exposure-factor-open-option-button-hz-${numHeightZones}`
                )
                {
                    exposureFactorSelection = "open";
                }

                // if rough
                else if (
                    exposureFactorSelection ===
                    `exposure-factor-rough-option-button-hz-${numHeightZones}`
                )
                {
                    exposureFactorSelection = "rough";
                }
                else if (
                    exposureFactorSelection ===
                    `exposure-factor-intermediate-option-button-hz-${numHeightZones}`
                )
                {
                    exposureFactorSelection = "intermediate";
                }

                let roofTypeSelectionElement = document.querySelector(
                    '#roof-type-selection input[type="radio"]:checked',
                );
                let roofTypeSelection = roofTypeSelectionElement ?
                    roofTypeSelectionElement.id :
                    "";

                if (
                    roofTypeSelection === "roof-selection-unobstructed-slippery-roof-option"
                )
                {
                    roofTypeSelection = "unobstructed_slippery_roof";
                }
                else if (roofTypeSelection === "roof-selection-other-option")
                {
                    roofTypeSelection = "other";
                }

                const raw = JSON.stringify(
                    {
                        exposure_factor_selection: exposureFactorSelection,
                        roof_type: roofTypeSelection,
                    });

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    body: raw,
                    redirect: "follow",
                };


                // iterate through radio buttons in roof-type-selection
                let radioButtons = document.getElementById('roof-type-selection').querySelectorAll('input[type="radio"]');
                radioButtons.forEach((button) =>
                {
                    button.disabled = true;
                });

                // iterate through all the secondary buttons in roof-type-selection
                let secondaryButtons = document.getElementById('roof-type-selection').querySelectorAll('.btn');
                secondaryButtons.forEach((button) =>
                {
                    button.classList.add('skeleton-loader');
                    button.disabled = true;
                });

                startLoadingSnowLoads();


                fetch(`${connectionAddress}/set_snow_load`, requestOptions)
                    .then((response) => response.json())
                    .then((result) =>
                    {
                        let snowLoadData = JSON.parse(result);
                        console.log(snowLoadData);
                        let upwindData = snowLoadData["upwind"];
                        let downwindData = snowLoadData["downwind"];
                        document.getElementById("upwind-accumulation-factor").innerHTML =
                            upwindData["factor"]["ca"];
                        document.getElementById("downwind-accumulation-factor").innerHTML =
                            downwindData["factor"]["ca"];
                        document.getElementById("snow-load-upwind-uls").innerHTML =
                            upwindData["s_uls"];
                        document.getElementById("snow-load-downwind-uls").innerHTML =
                            downwindData["s_uls"];

                        // iterate through radio buttons in roof-type-selection
                        let radioButtons = document.getElementById('roof-type-selection').querySelectorAll('input[type="radio"]');
                        radioButtons.forEach((button) =>
                        {
                            button.disabled = false;
                        });

                        // iterate through all the secondary buttons in roof-type-selection
                        let secondaryButtons = document.getElementById('roof-type-selection').querySelectorAll('.btn');
                        secondaryButtons.forEach((button) =>
                        {
                            button.classList.remove('skeleton-loader');
                            button.disabled = false;
                        });

                        doneLoadingSnowLoads();
                    })
                    .catch((error) => {
                        doneLoadingSnowLoads();
                    });
            });

    });

}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// BUTTON CLICK EVENTS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * When the wind-calculate-button is clicked, the wind loads are retrieved from the backend
 */
document
    .getElementById("wind-calculate-button")
    .addEventListener("click", () =>
    {
        let numHeightZones = document.querySelectorAll('h5[id^="wind-load-component-hz-"]').length;
        for (let i = 1; i <= numHeightZones; i++)
        {
            // check that the exposure factor and internal pressure category are selected and topographic factor is not empty
            let exposureFactor = document.querySelector(
                `input[name="exposure-factor-selection-hz-${i}"]:checked`,
            );

            // if intermediate exposure factor is selected, check that the ce intermediate is not empty
            if (exposureFactor && exposureFactor.id === `exposure-factor-intermediate-option-hz-${i}`)
            {
                let ceIntermediate = document.getElementById(`ce-intermediate-hz-${i}`).value;
                if (ceIntermediate === "")
                {
                    document.getElementById("wind-calculate-warning").style.color = "red";
                    document.getElementById("wind-calculate-warning").style.fontWeight = "bold";
                    document.getElementById("wind-calculate-warning").innerHTML = "Please enter the ce intermediate for the intermediate exposure factor";

                    // clear pos and neg of the wind load table
                    for (let j = 1; j <= 5; j++)
                    {
                        document.getElementById(`pos-${j}-hz-${i}`).innerHTML = "NA";
                        document.getElementById(`neg-${j}-hz-${i}`).innerHTML = "NA";
                    }
                    return;
                }
            }

            let internalPressureCategory = document.querySelector(
                `input[name="internal-pressure-category-selection-hz-${i}"]:checked`,
            );
            let topographicFactor = document.getElementById(`topographic-factor-hz-${i}`).value;

            if (!exposureFactor || !internalPressureCategory || topographicFactor === "")
            {
                document.getElementById("wind-calculate-warning").style.color = "red";
                document.getElementById("wind-calculate-warning").style.fontWeight = "bold";
                document.getElementById("wind-calculate-warning").innerHTML = "Please enter the topographic factor and select the exposure factor and internal pressure category for all the height zones";

                // clear pos and neg of the wind load table
                for (let j = 1; j <= 5; j++)
                {
                    document.getElementById(`pos-${j}-hz-${i}`).innerHTML = "NA";
                    document.getElementById(`neg-${j}-hz-${i}`).innerHTML = "NA";
                }
                return;
            }
        }

        document.getElementById("wind-calculate-warning").innerHTML = "";
        getWindLoads();
    });

/**
 * When the seismic-calculate-button is clicked, the seismic loads are retrieved from the backend
 */
document
    .getElementById("seismic-calculate-button")
    .addEventListener("click", () =>
    {
        // check that the amplification factor, response modification factor and component factor are not empty
        let amplificationFactor = document.getElementById("amplification-factor").value;
        let responseModificationFactor = document.getElementById("response-modification-factor").value;
        let componentFactor = document.getElementById("component-factor").value;

        if (amplificationFactor === "" || responseModificationFactor === "" || componentFactor === "")
        {
            document.getElementById("seismic-calculate-warning").style.color = "red";
            document.getElementById("seismic-calculate-warning").style.fontWeight = "bold";
            document.getElementById("seismic-calculate-warning").innerHTML = "Please enter the amplification factor, response modification factor and component factor";

            // clear sp and vp of the seismic load table
            for (let i = 1; i < document.getElementById('seismic-load-table').rows.length - 1; i++)
            {
                document.getElementById(`sp-hz-${i}`).innerHTML = "NA";
                document.getElementById(`vp-hz-${i}`).innerHTML = "NA";
            }
            return;
        }

        document.getElementById("seismic-calculate-warning").innerHTML = "";
        getSeismicLoads();
    });

/**
 * When the snow-calculate-button is clicked, the snow loads are retrieved from the backend
 */
document
    .getElementById("snow-calculate-button")
    .addEventListener("click", () =>
    {
        // check that roof type and exposure factor are selected
        let numHeightZones = document.querySelectorAll('h5[id^="wind-load-component-hz-"]').length;
        let roofTypeSelection = document.querySelector('#roof-type-selection input[type="radio"]:checked', );
        let exposureFactorSelection = document.getElementById(`exposure-factor-selection-hz-${numHeightZones}`).querySelector(".selected");
        if (!exposureFactorSelection || !roofTypeSelection)
        {
            document.getElementById("snow-calculate-warning").style.color = "red";
            document.getElementById("snow-calculate-warning").style.fontWeight = "bold";
            document.getElementById("snow-calculate-warning").innerHTML = "Please select the roof type and ensure exposure factor of last height zone is selected";

            document.getElementById("upwind-accumulation-factor").innerHTML = "NA";
            document.getElementById("downwind-accumulation-factor").innerHTML = "NA";
            document.getElementById("snow-load-upwind-uls").innerHTML = "NA";
            document.getElementById("snow-load-downwind-uls").innerHTML = "NA";
            return;
        }

        document.getElementById("snow-calculate-warning").innerHTML = "";
        getSnowLoad();
    });

/**
 * When the save button is clicked, the current state of the page is serialized and sent to the backend
 */
document.getElementById("save-button").addEventListener("click", () =>
{
    window.api
        .invoke("get-connection-address").then((connectionAddress) =>
    {
        window.api
            .invoke("get-token") // Retrieve the token
            .then((token) =>
            {
                const myHeaders = new Headers();
                myHeaders.append("Accept", "application/json");
                myHeaders.append("Authorization", `Bearer ${token}`);

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    redirect: "follow",
                };

                fetch(`${connectionAddress}/get_user_current_save_file`, requestOptions)
                    .then((response) =>
                    {
                        if (response.status === 200)
                        {
                            return response.json();
                        }
                        else
                        {
                            throw new Error("Get User Current Save File Error");
                        }
                    })
                    .then((result) =>
                    {
                        let id = parseInt(result);
                        const myHeaders = new Headers();
                        myHeaders.append("Content-Type", "application/json");
                        myHeaders.append("Accept", "application/json");
                        myHeaders.append("Authorization", `Bearer ${token}`);

                        const raw = JSON.stringify(
                            {
                                json_data: serialize(),
                                id: id,
                            });

                        const requestOptions = {
                            method: "POST",
                            headers: myHeaders,
                            body: raw,
                            redirect: "follow",
                        };

                        fetch(`${connectionAddress}/set_user_save_data`, requestOptions)
                            .then((response) => response.text())
                            .catch((error) => console.error(error));
                    })
                    .catch((error) => console.error(error));
            });
    });

});

/**
 * When the back button is pressed, the user is redirected to the input page
 */
document.getElementById("back-button").addEventListener("click", function()
{
    window.location.href = "input.html";
});

/**
 * When the home button is pressed, the user is redirected to the home page
 */
document.getElementById("home-button").addEventListener("click", function()
{
    window.location.href = "home.html";
});

/**
 * When the next button is pressed, the user is redirected to the results page
 */
document.getElementById("next-button").addEventListener("click", function()
{
    // iterate through all the tables and ensure no NA values are present
    let allTables = document.querySelectorAll("table");
    let allTablesArray = Array.from(allTables);
    let allTablesText = allTablesArray.map((table) => table.innerText);
    if (allTablesText.some((text) => text.includes("NA")))
    {
        document.getElementById("next-warning").innerHTML =
            "Please calculate all the loads before proceeding";
    }

    // iterate through all snow load inputs and ensure no NA values are present
    else if (
        document.getElementById("upwind-accumulation-factor").innerText === "NA" ||
        document.getElementById("downwind-accumulation-factor").innerText ===
        "NA" ||
        document.getElementById("snow-load-upwind-uls").innerText === "NA" ||
        document.getElementById("snow-load-downwind-uls").innerText === "NA"
    )
    {
        document.getElementById("next-warning").innerHTML =
            "Please calculate the snow load before proceeding";
    }
    else
    {
        window.location.href = "results.html";
    }
});

/**
 * When the profile button is clicked, the user is redirected to the profile page
 */
document.getElementById("profile").addEventListener("click", function()
{
    window.location.href = "profile.html";
});

/**
 * When the logout button is clicked, the user is logged out and redirected to the login page
 */
document.getElementById("logout").addEventListener("click", function()
{
    window.api.invoke("store-token", "");
    window.location.href = "login.html";
});

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SERIALIZATION
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Wait for an element to load
 * @param id
 * @param callback
 */
function waitForElement(id, callback)
{
    let intervalId = setInterval(function()
    {
        let element = document.getElementById(id);
        if (element)
        {
            clearInterval(intervalId);
            callback(element);
        }
    }, 100); // Check every 100ms
}

/**
 * Serialize the input page
 * @returns A JSON string representing the input page
 */
function serialize()
{
    let objects = {
        load_page:
            {
                radio:
                    {},
                input:
                    {},
            },
    };

    // Handle radio inputs
    let radios = document.querySelectorAll("input[type=radio]");
    radios.forEach((radio) =>
    {
        if (radio.checked)
        {
            objects.load_page.radio[radio.id] = radio.value;
        }
    });

    // Handle other inputs
    let inputs = document.querySelectorAll("input:not([type=radio])");
    inputs.forEach((input) =>
    {
        if (input.value !== "")
        {
            objects.load_page.input[input.id] = input.value;
        }
    });

    let json = JSON.stringify(objects);
    return json;
}

/**
 * Deserialize the input page
 * @param json
 * @param section
 * @returns {Promise<unknown>}
 */
function deserialize(json, section)
{
    return new Promise((resolve) =>
    {
        let objects = JSON.parse(json)[section];
        let totalElements =
            Object.keys(objects.radio).length + Object.keys(objects.input).length;
        let processedElements = 0;

        // go through all the radio
        for (let id in objects.radio)
        {
            waitForElement(id, function(radio)
            {
                if (radio.value === objects.radio[id])
                {
                    radio.click();
                }
                processedElements++;
                if (processedElements === totalElements)
                {
                    resolve();
                }
            });
        }

        // go through all the input
        for (let id in objects.input)
        {
            waitForElement(id, function(input)
            {
                input.value = "";
                input.focus();
                let value = objects.input[id];
                for (let i = 0; i < value.length; i++)
                {
                    input.value = value;
                }
                processedElements++;
                if (processedElements === totalElements)
                {
                    resolve();
                }
            });
        }
    });
}

/**
 * Load the save file
 */
function loadSaveFile()
{
    window.api
        .invoke("get-connection-address").then((connectionAddress) =>
    {
        window.api
            .invoke("get-token") // Retrieve the token
            .then((token) =>
            {
                const myHeaders = new Headers();
                myHeaders.append("Accept", "application/json");
                myHeaders.append("Authorization", `Bearer ${token}`);

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    redirect: "follow",
                };

                fetch(`${connectionAddress}/get_user_current_save_file`, requestOptions)
                    .then((response) =>
                    {
                        if (response.status === 200)
                        {
                            return response.json();
                        }
                        else
                        {
                            throw new Error("Get User Current Save File Error");
                        }
                    })
                    .then((result) =>
                    {
                        let id = parseInt(result);
                        const myHeaders = new Headers();
                        myHeaders.append("Accept", "application/json");
                        myHeaders.append("Authorization", `Bearer ${token}`);

                        const requestOptions = {
                            method: "POST",
                            headers: myHeaders,
                            redirect: "follow",
                        };

                        fetch(
                            `${connectionAddress}/get_user_save_file?id=${id}`,
                            requestOptions,
                        )
                            .then((response) =>
                            {
                                if (response.status === 200)
                                {
                                    return response.json();
                                }
                                else
                                {
                                    throw new Error("Get User Save File Error");
                                }
                            })
                            .then((data) =>
                            {
                                const myHeaders = new Headers();
                                myHeaders.append("Accept", "application/json");
                                myHeaders.append("Authorization", `Bearer ${token}`);

                                const requestOptions = {
                                    method: "POST",
                                    headers: myHeaders,
                                    redirect: "follow",
                                };

                                fetch(
                                    `${connectionAddress}/get_user_save_file?id=${id}`,
                                    requestOptions,
                                )
                                    .then((response) =>
                                    {
                                        if (response.status === 200)
                                        {
                                            return response.json();
                                        }
                                        else
                                        {
                                            throw new Error("Get User Save File Error");
                                        }
                                    })
                                    .then((result) =>
                                    {
                                        deserialize(result.JsonData, "load_page").then(() =>
                                        {
                                            window.scrollTo(0, 0);
                                        });
                                    })
                                    .catch((error) => console.error(error));
                            })
                            .catch((error) => console.error(error));
                    })
                    .catch((error) => console.error(error));
            });
    });

}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// DROPDOWN MENU
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Set the username in the dropdown menu
 */
function setUsernameDropdown()
{
    window.api
        .invoke("get-connection-address").then((connectionAddress) =>
    {
        window.api
            .invoke("get-token") // Retrieve the token
            .then((token) =>
            {
                const myHeaders = new Headers();
                myHeaders.append("Accept", "application/json");
                myHeaders.append("Authorization", `Bearer ${token}`);

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    redirect: "follow",
                };

                fetch(`${connectionAddress}/get_user_profile`, requestOptions)
                    .then((response) => response.json())
                    .then((result) =>
                    {
                        let data = JSON.parse(result);
                        username = data["username"];
                        document.getElementById("navbarDropdownMenuLink").textContent =
                            username;
                    })
                    .catch((error) => window.location.href = "login.html");
            });
    });

}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// WINDOW ONLOAD EVENT
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Set up the page on load
 */
window.onload = function()
{
    loadSaveFile();
    setUsernameDropdown();

    toggleMenuColors("#roof-type-selection");

    let allWindLoadContainer = document.getElementById("all-wind-load-container");
    // let allSeismicLoadContainer = document.getElementById('seismic-load-table-container');
    let seismicLoadTable = document.getElementById("seismic-load-table");

    getNumHeightZones()
        .then((numHeightZones) =>
        {
            const selectors = [];
            for (let i = 1; i <= numHeightZones; i++)
            {
                allWindLoadContainer.innerHTML += createWindLoadComponent(i);

                waitForElement(`topographic-factor-hz-${i}`, () =>
                {
                    // add event listener for topographic-factor-hz-i if the value is changed
                    document.getElementById(`topographic-factor-hz-${i}`).addEventListener("input", () =>
                    {
                        // set the pos and neg of the associated wind load table to NA
                        for (let j = 1; j <= 5; j++)
                        {
                            document.getElementById(`pos-${j}-hz-${i}`).innerHTML = "NA";
                            document.getElementById(`neg-${j}-hz-${i}`).innerHTML = "NA";
                        }
                    });
                });

                selectors.push(`#exposure-factor-selection-hz-${i}`);
                selectors.push(`#internal-pressure-category-selection-hz-${i}`);
                document.getElementById(`ce-intermediate-hz-${i}`).style.display =
                    "none";
                // case if intermediate is selected
                waitForElement(`exposure-factor-intermediate-option-hz-${i}`, () =>
                {
                    document
                        .getElementById(`exposure-factor-intermediate-option-hz-${i}`)
                        .addEventListener("click", () =>
                        {
                            document.getElementById(`ce-intermediate-hz-${i}`).style.display = "block";
                            // set the pos and neg of the associated wind load table to NA
                            for (let j = 1; j <= 5; j++)
                            {
                                document.getElementById(`pos-${j}-hz-${i}`).innerHTML = "NA";
                                document.getElementById(`neg-${j}-hz-${i}`).innerHTML = "NA";
                            }
                        });

                    waitForElement(`ce-intermediate-hz-${i}`, () =>
                    {
                        document
                            .getElementById(`ce-intermediate-hz-${i}`)
                            .addEventListener("input", () =>
                            {
                                // set the pos and neg of the associated wind load table to NA
                                for (let j = 1; j <= 5; j++)
                                {
                                    document.getElementById(`pos-${j}-hz-${i}`).innerHTML = "NA";
                                    document.getElementById(`neg-${j}-hz-${i}`).innerHTML = "NA";
                                }
                            });
                    });
                });
                // case if open is selected
                waitForElement(`exposure-factor-open-option-hz-${i}`, () =>
                {
                    document
                        .getElementById(`exposure-factor-open-option-hz-${i}`)
                        .addEventListener("click", () =>
                        {
                            document.getElementById(`ce-intermediate-hz-${i}`).style.display = "none";
                            // set the pos and neg of the associated wind load table to NA
                            for (let j = 1; j <= 5; j++)
                            {
                                document.getElementById(`pos-${j}-hz-${i}`).innerHTML = "NA";
                                document.getElementById(`neg-${j}-hz-${i}`).innerHTML = "NA";
                            }
                        });
                });

                // case if rough is selected
                waitForElement(`exposure-factor-rough-option-hz-${i}`, () =>
                {
                    document
                        .getElementById(`exposure-factor-rough-option-hz-${i}`)
                        .addEventListener("click", () =>
                        {
                            document.getElementById(`ce-intermediate-hz-${i}`).style.display = "none";
                            // set the pos and neg of the associated wind load table to NA
                            for (let j = 1; j <= 5; j++)
                            {
                                document.getElementById(`pos-${j}-hz-${i}`).innerHTML = "NA";
                                document.getElementById(`neg-${j}-hz-${i}`).innerHTML = "NA";
                            }
                        });
                });

                waitForElement(`internal-pressure-category-selection-hz-${i}`, () =>
                {
                    document
                        .getElementById(`internal-pressure-category-selection-hz-${i}`)
                        .addEventListener("click", () =>
                        {
                            // set the pos and neg of the associated wind load table to NA
                            for (let j = 1; j <= 5; j++)
                            {
                                document.getElementById(`pos-${j}-hz-${i}`).innerHTML = "NA";
                                document.getElementById(`neg-${j}-hz-${i}`).innerHTML = "NA";
                            }
                        });
                });

                // add row to the seismic load table
                seismicLoadTable.innerHTML += `
            <tr>
                <td>Height Zone ${i}</td>
                <td id="sp-hz-${i}">NA</td>
                <td id="vp-hz-${i}">NA</td>
             </tr>`;
            }

            // add event handler for biggest height zone if the exposure factor selection is changed
            waitForElement(`exposure-factor-selection-hz-${numHeightZones}`, () =>
            {
                document
                    .getElementById(`exposure-factor-selection-hz-${numHeightZones}`)
                    .addEventListener("click", () =>
                    {
                        document.getElementById("upwind-accumulation-factor").innerHTML =
                            "NA";
                        document.getElementById("downwind-accumulation-factor").innerHTML =
                            "NA";
                        document.getElementById("snow-load-upwind-uls").innerHTML = "NA";
                        document.getElementById("snow-load-downwind-uls").innerHTML = "NA";
                    });
            });

            selectors.forEach((selector) => toggleMenuColors(selector));


        })
        .catch((error) =>
        {
            console.error(error);
        });

    waitForElement('amplification-factor', (element) =>
    {
        // set all sp and vp to NA if the amplification factor is changed
        element.addEventListener('input', () =>
        {
            for (let i = 1; i < document.getElementById('seismic-load-table').rows.length - 1; i++)
            {
                document.getElementById(`sp-hz-${i}`).innerHTML = 'NA';
                document.getElementById(`vp-hz-${i}`).innerHTML = 'NA';
            }
        });
    });

    waitForElement('response-modification-factor', (element) =>
    {
        // set all sp and vp to NA if the response modification factor is changed
        element.addEventListener('input', () =>
        {
            for (let i = 1; i < document.getElementById('seismic-load-table').rows.length - 1; i++)
            {
                document.getElementById(`sp-hz-${i}`).innerHTML = 'NA';
                document.getElementById(`vp-hz-${i}`).innerHTML = 'NA';
            }
        });
    });

    waitForElement('component-factor', (element) =>
    {
        // set all sp and vp to NA if the component factor is changed
        element.addEventListener('input', () =>
        {
            for (let i = 1; i < document.getElementById('seismic-load-table').rows.length - 1; i++)
            {
                document.getElementById(`sp-hz-${i}`).innerHTML = 'NA';
                document.getElementById(`vp-hz-${i}`).innerHTML = 'NA';
            }
        });
    });

    waitForElement('roof-type-selection', (element) =>
    {
        // set all snow load values to NA if the roof type is changed
        element.addEventListener('click', () =>
        {
            document.getElementById('upwind-accumulation-factor').innerHTML = 'NA';
            document.getElementById('downwind-accumulation-factor').innerHTML = 'NA';
            document.getElementById('snow-load-upwind-uls').innerHTML = 'NA';
            document.getElementById('snow-load-downwind-uls').innerHTML = 'NA';
        });
    });
};