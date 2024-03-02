function waitForElement(id, callback) {
    let intervalId = setInterval(function() {
        let element = document.getElementById(id);
        if (element) {
            clearInterval(intervalId);
            callback(element);
        }
    }, 100); // Check every 100ms
}

function waitForElements(ids, callback) {
    let intervalId = setInterval(function() {
        let elements = ids.map(id => document.getElementById(id));
        if (elements.every(element => element !== null)) {
            clearInterval(intervalId);
            callback(elements);
        }
    }, 100); // Check every 100ms
}

function toggleMenuColors(toggleMenu)
{
    document.querySelectorAll(toggleMenu + ' .btn').forEach((button) =>
    {
        button.addEventListener('click', (event) =>
        {
            document.querySelectorAll(toggleMenu + ' .btn').forEach((btn) =>
            {
                btn.classList.remove('selected');
            });
            event.currentTarget.classList.add('selected');
        });
    });
}

function getNumHeightZones()
{
    return new Promise((resolve, reject) => {
        window.api.invoke('get-token') // Retrieve the token
            .then((token) => {
                const myHeaders = new Headers();
                myHeaders.append("Accept", "application/json");
                myHeaders.append("Authorization", `Bearer ${token}`);

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    redirect: "follow"
                };

                fetch("http://localhost:42613/get_height_zones", requestOptions)
                    .then((response) => response.json())
                    .then((result) => {
                        let heightZoneData = JSON.parse(result);
                        let numHeightZones = Object.keys(heightZoneData).length;
                        resolve(numHeightZones); // Resolve the promise with numHeightZones
                    })
                    .catch((error) => {
                        console.error(error);
                        reject(error);
                    });
            })
    });
}

function getWindLoads()
{
    window.api.invoke('get-token') // Retrieve the token
        .then((token) => {
            const myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            myHeaders.append("Accept", "application/json");
            myHeaders.append("Authorization", `Bearer ${token}`);

            // count the number of height zones by the number of height zones wind load headers
            const numHeightZones = document.querySelectorAll('h5[id^="wind-load-component-hz-"]').length;
            
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

                // add skeleton-loader class to all the wind load inputs
                document.getElementById(`topographic-factor-hz-${i}`).classList.add('skeleton-loader');

                // disable associated radio buttons
                document.getElementById(`exposure-factor-open-option-hz-${i}`).disabled = true;
                document.getElementById(`exposure-factor-rough-option-hz-${i}`).disabled = true;
                document.getElementById(`exposure-factor-intermediate-option-hz-${i}`).disabled = true;

                // add skeleton-loader to parent secondary button
                document.getElementById(`exposure-factor-open-option-button-hz-${i}`).classList.add('skeleton-loader');
                document.getElementById(`exposure-factor-rough-option-button-hz-${i}`).classList.add('skeleton-loader');
                document.getElementById(`exposure-factor-intermediate-option-button-hz-${i}`).classList.add('skeleton-loader');

                // disable radio buttons of internal pressure category
                document.getElementById(`internal-pressure-category-enclosed-option-hz-${i}`).disabled = true;
                document.getElementById(`internal-pressure-category-partially-enclosed-option-hz-${i}`).disabled = true;
                document.getElementById(`internal-pressure-category-large-openings-option-hz-${i}`).disabled = true;

                // add skeleton loader to secondary buttons of internal pressure category
                document.getElementById(`internal-pressure-category-enclosed-option-button-hz-${i}`).classList.add('skeleton-loader');
                document.getElementById(`internal-pressure-category-partially-enclosed-option-button-hz-${i}`).classList.add('skeleton-loader');
                document.getElementById(`internal-pressure-category-large-openings-option-button-hz-${i}`).classList.add('skeleton-loader');

                document.getElementById(`ce-intermediate-hz-${i}`).classList.add('skeleton-loader');

                // add skeleton-loader to pos and neg cells
                for (let j = 1; j <= 5; j++)
                {
                    document.getElementById(`pos-${j}-hz-${i}`).classList.add('skeleton-loader');
                    document.getElementById(`neg-${j}-hz-${i}`).classList.add('skeleton-loader');
                }
            }

            const raw = JSON.stringify({
                "ct": ctValues,
                "exposure_factor": exposureFactorValues,
                "manual_ce_cei": manualCeCeiValues,
                "internal_pressure_category": internalPressureCategoryValues
            });

            const requestOptions = {
                method: "POST",
                headers: myHeaders,
                body: raw,
                redirect: "follow"
            };

            fetch("http://localhost:42613/set_wind_load", requestOptions)
                .then((response) => response.json())
                .then((result) => {
                    const myHeaders = new Headers();
                    myHeaders.append("Accept", "application/json");
                    myHeaders.append("Authorization", `Bearer ${token}`);

                    const requestOptions = {
                        method: "POST",
                        headers: myHeaders,
                        redirect: "follow"
                    };

                    fetch("http://localhost:42613/get_height_zones", requestOptions)
                        .then((response) => response.json())
                        .then((result) =>
                        {
                            let heightZoneData = JSON.parse(result);
                            console.log(heightZoneData);

                            for (let zoneNum in heightZoneData)
                            {
                                let innerZones = heightZoneData[zoneNum]['wind_load']['zones']
                                for (let innerZoneNum in innerZones)
                                {
                                    let innerZone = innerZones[innerZoneNum];

                                    switch (innerZone['name'])
                                    {
                                        case 'roof_interior':
                                            document.getElementById(`pos-1-hz-${zoneNum}`).innerHTML = innerZone['pressure']['pos_uls'];
                                            document.getElementById(`neg-1-hz-${zoneNum}`).innerHTML = innerZone['pressure']['neg_uls'];
                                            break;
                                        case 'roof_edge':
                                            document.getElementById(`pos-2-hz-${zoneNum}`).innerHTML = innerZone['pressure']['pos_uls'];
                                            document.getElementById(`neg-2-hz-${zoneNum}`).innerHTML = innerZone['pressure']['neg_uls'];
                                            break;
                                        case 'roof_corner':
                                            document.getElementById(`pos-3-hz-${zoneNum}`).innerHTML = innerZone['pressure']['pos_uls'];
                                            document.getElementById(`neg-3-hz-${zoneNum}`).innerHTML = innerZone['pressure']['neg_uls'];
                                            break;
                                        case 'wall_centre':
                                            document.getElementById(`pos-4-hz-${zoneNum}`).innerHTML = innerZone['pressure']['pos_uls'];
                                            document.getElementById(`neg-4-hz-${zoneNum}`).innerHTML = innerZone['pressure']['neg_uls'];
                                            break;
                                        case 'wall_corner':
                                            document.getElementById(`pos-5-hz-${zoneNum}`).innerHTML = innerZone['pressure']['pos_uls'];
                                            document.getElementById(`neg-5-hz-${zoneNum}`).innerHTML = innerZone['pressure']['neg_uls'];
                                            break;
                                    }
                                }

                                // remove skeleton-loader class from all the wind load inputs and enable the radio buttons
                                document.getElementById(`topographic-factor-hz-${zoneNum}`).classList.remove('skeleton-loader');
                                document.getElementById(`exposure-factor-open-option-hz-${zoneNum}`).disabled = false;
                                document.getElementById(`exposure-factor-rough-option-hz-${zoneNum}`).disabled = false;
                                document.getElementById(`exposure-factor-intermediate-option-hz-${zoneNum}`).disabled = false;
                                document.getElementById(`exposure-factor-open-option-button-hz-${zoneNum}`).classList.remove('skeleton-loader');
                                document.getElementById(`exposure-factor-rough-option-button-hz-${zoneNum}`).classList.remove('skeleton-loader');
                                document.getElementById(`exposure-factor-intermediate-option-button-hz-${zoneNum}`).classList.remove('skeleton-loader');
                                document.getElementById(`internal-pressure-category-enclosed-option-hz-${zoneNum}`).disabled = false;
                                document.getElementById(`internal-pressure-category-partially-enclosed-option-hz-${zoneNum}`).disabled = false;
                                document.getElementById(`internal-pressure-category-large-openings-option-hz-${zoneNum}`).disabled = false;
                                document.getElementById(`internal-pressure-category-enclosed-option-button-hz-${zoneNum}`).classList.remove('skeleton-loader');
                                document.getElementById(`internal-pressure-category-partially-enclosed-option-button-hz-${zoneNum}`).classList.remove('skeleton-loader');
                                document.getElementById(`internal-pressure-category-large-openings-option-button-hz-${zoneNum}`).classList.remove('skeleton-loader');
                                document.getElementById(`ce-intermediate-hz-${zoneNum}`).classList.remove('skeleton-loader');
                                for (let j = 1; j <= 5; j++)
                                {
                                    document.getElementById(`pos-${j}-hz-${zoneNum}`).classList.remove('skeleton-loader');
                                    document.getElementById(`neg-${j}-hz-${zoneNum}`).classList.remove('skeleton-loader');
                                }
                            }
                        })
                        .catch((error) => console.error(error));
                })
                .catch((error) => console.error(error));
        });
}

function getSiesmicLoads()
{
    window.api.invoke('get-token') // Retrieve the token
        .then((token) => {

        });
}

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

function createSeismicLoadComponent(zone_num){
    return `
    <hr>
    <h5 id="seismic-load-component-hz-${zone_num}">Height Zone ${zone_num}</h5>
    <hr>
    <div class="row gx-5 ">
        <div class="col-md-6">
            <div class="mb-3">
                <label for="amplification-factor-hz-${zone_num}">Element of Component Force Amplification Factor (Ar)</label>
                <p>By default Ar has a value of 1</p>
                <input type="number" id="amplification-factor-hz-${zone_num}" class="form-control" value="1"/>
            </div>
            <div class="mb-3">
                <label for="response-modification-factor-hz-${zone_num}">Element of Component Response Modification Factor (Rp)</label>
                <p>By default Ar has a value of 2.5</p>
                <input type="number" id="response-modification-factor-hz-${zone_num}" class="form-control" value="2.5"/>
            </div>
            <div class="mb-3">
                <label for="component-factor-hz-${zone_num}">Elements of Component Factor (Cp)</label>
                <p>By default Ar has a value of 1</p>
                <input type="number" id="component-factor-hz-${zone_num}" class="form-control" value="1"/>
            </div>
        </div>
        <div class="col-md-6">
            <label for="seismic-load-hz-${zone_num}">Seismic Load</label>
            <p id="seismic-load-hz-${zone_num}">NA</p>
        </div>
    </div>
    
    `;
}

function getWindLoadInputs(zone_num)
{
    let topographicFactor = document.getElementById(`topographic-factor-hz-${zone_num}`).value;
    let exposureFactor = document.querySelector(`input[name="exposure-factor-selection-hz-${zone_num}"]:checked`).id;
    let ceIntermediate;

    // if open
    if (exposureFactor === `exposure-factor-open-option-hz-${zone_num}`){
        exposureFactor = 'open';
    }

    // if rough
    else if (exposureFactor === `exposure-factor-rough-option-hz-${zone_num}`){
        exposureFactor = 'rough';
    }

    else if (exposureFactor === `exposure-factor-intermediate-option-hz-${zone_num}`){
        exposureFactor = 'intermediate';
        ceIntermediate = document.getElementById(`ce-intermediate-hz-${zone_num}`).value;
    }

    let internalPressureCategory = document.querySelector(`input[name="internal-pressure-category-selection-hz-${zone_num}"]:checked`).id;

    // if enclosed
    if (internalPressureCategory === `internal-pressure-category-enclosed-option-hz-${zone_num}`){
        internalPressureCategory = 'enclosed';
    }

    else if (internalPressureCategory === `internal-pressure-category-partially-enclosed-option-hz-${zone_num}`){
        internalPressureCategory = 'partially_enclosed';
    }

    else if (internalPressureCategory === `internal-pressure-category-large-openings-option-hz-${zone_num}`){
        internalPressureCategory = 'large_openings';
    }

    console.log(topographicFactor, exposureFactor, ceIntermediate, internalPressureCategory);

    return {
        topographicFactor,
        exposureFactor,
        ceIntermediate,
        internalPressureCategory
    };
}

function getSeismicLoadInputs(zone_num)
{
    let amplificationFactor = document.getElementById(`amplification-factor-hz-${zone_num}`).value;
    let responseModificationFactor = document.getElementById(`response-modification-factor-hz-${zone_num}`).value;
    let componentFactor = document.getElementById(`component-factor-hz-${zone_num}`).value;

    console.log(amplificationFactor, responseModificationFactor, componentFactor);
    return {
        amplificationFactor,
        responseModificationFactor,
        componentFactor
    };
}

// wind-calculate-button press
document.getElementById('wind-calculate-button').addEventListener('click', () =>
{
    getWindLoads();
});

// seismic-calculate-button press
document.getElementById('seismic-calculate-button').addEventListener('click', () =>
{
    getSeismicLoadInputs(1);
});

window.onload = function()
{
    let allWindLoadContainer = document.getElementById('all-wind-load-container');
    let allSeismicLoadContainer = document.getElementById('all-seismic-load-container');

    getNumHeightZones().then(numHeightZones => {
        const selectors = [];
        for (let i = 1; i <= numHeightZones; i++)
        {
            allWindLoadContainer.innerHTML += createWindLoadComponent(i);
            selectors.push(`#exposure-factor-selection-hz-${i}`);
            selectors.push(`#internal-pressure-category-selection-hz-${i}`);
            document.getElementById(`ce-intermediate-hz-${i}`).style.display = 'none';
            // case if intermediate is selected
            waitForElement(`exposure-factor-intermediate-option-hz-${i}`, () => {
                document.getElementById(`exposure-factor-intermediate-option-hz-${i}`).addEventListener('click', () => {
                    document.getElementById(`ce-intermediate-hz-${i}`).style.display = 'block';
                });
            });
            // case if open is selected
            waitForElement(`exposure-factor-open-option-hz-${i}`, () => {
                document.getElementById(`exposure-factor-open-option-hz-${i}`).addEventListener('click', () => {
                    document.getElementById(`ce-intermediate-hz-${i}`).style.display = 'none';
                });
            });

            // case if rough is selected
            waitForElement(`exposure-factor-rough-option-hz-${i}`, () => {
                document.getElementById(`exposure-factor-rough-option-hz-${i}`).addEventListener('click', () => {
                    document.getElementById(`ce-intermediate-hz-${i}`).style.display = 'none';
                });
            });

            allSeismicLoadContainer.innerHTML += createSeismicLoadComponent(i);
        }
        selectors.forEach(selector => toggleMenuColors(selector));
    }).catch(error => {
        console.error(error);
    });
};