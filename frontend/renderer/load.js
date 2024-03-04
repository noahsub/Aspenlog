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

function waitForElements(ids, callback)
{
    let intervalId = setInterval(function()
    {
        let elements = ids.map(id => document.getElementById(id));
        if (elements.every(element => element !== null))
        {
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
    return new Promise((resolve, reject) =>
    {
        window.api.invoke('get-token') // Retrieve the token
            .then((token) =>
            {
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
                        let numHeightZones = Object.keys(heightZoneData).length;
                        resolve(numHeightZones); // Resolve the promise with numHeightZones
                    })
                    .catch((error) =>
                    {
                        console.error(error);
                        reject(error);
                    });
            })
    });
}

function getWindLoads()
{
    window.api.invoke('get-token') // Retrieve the token
        .then((token) =>
        {
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

            const raw = JSON.stringify(
                {
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
                .then((result) =>
                {
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

function getSeismicLoads()
{
    window.api.invoke('get-token') // Retrieve the token
        .then((token) =>
        {
            const myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            myHeaders.append("Accept", "application/json");
            myHeaders.append("Authorization", `Bearer ${token}`);

            const raw = JSON.stringify(
                {
                    "ar": parseFloat(document.getElementById('amplification-factor').value),
                    "rp": parseFloat(document.getElementById('response-modification-factor').value),
                    "cp": parseFloat(document.getElementById('component-factor').value)
                });

            const requestOptions = {
                method: "POST",
                headers: myHeaders,
                body: raw,
                redirect: "follow"
            };

            fetch("http://localhost:42613/set_seismic_load", requestOptions)
                .then((response) => response.json())
                .then((result) =>
                {
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
                                let seismicLoad = heightZoneData[zoneNum]['seismic_load'];
                                document.getElementById(`sp-hz-${zoneNum}`).innerHTML = seismicLoad['sp'];
                                document.getElementById(`vp-hz-${zoneNum}`).innerHTML = seismicLoad['vp'];
                            }
                        })
                        .catch((error) => console.error(error));
                })
                .catch((error) => console.error(error));
        });
}

function getSnowLoad()
{
    window.api.invoke('get-token') // Retrieve the token
        .then((token) =>
        {
            const myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            myHeaders.append("Accept", "application/json");
            myHeaders.append("Authorization", `Bearer ${token}`);

            const numHeightZones = document.querySelectorAll('h5[id^="wind-load-component-hz-"]').length;
            let exposureFactorSelection = document.getElementById(`exposure-factor-selection-hz-${numHeightZones}`).querySelector('.selected').id;

            // if open
            if (exposureFactorSelection === `exposure-factor-open-option-button-hz-${numHeightZones}`)
            {
                exposureFactorSelection = 'open';
            }

            // if rough
            else if (exposureFactorSelection === `exposure-factor-rough-option-button-hz-${numHeightZones}`)
            {
                exposureFactorSelection = 'rough';
            }

            else if (exposureFactorSelection === `exposure-factor-intermediate-option-button-hz-${numHeightZones}`)
            {
                exposureFactorSelection = 'intermediate';
            }

            let roofTypeSelectionElement = document.querySelector('#roof-type-selection input[type="radio"]:checked');
            let roofTypeSelection = roofTypeSelectionElement ? roofTypeSelectionElement.id : '';

            if (roofTypeSelection === 'roof-selection-unobstructed-slippery-roof-option')
            {
                roofTypeSelection = 'unobstructed_slippery_roof';
            }

            else if (roofTypeSelection === 'roof-selection-other-option')
            {
                roofTypeSelection = 'other';
            }

            const raw = JSON.stringify(
                {
                    "exposure_factor_selection": exposureFactorSelection,
                    "roof_type": roofTypeSelection
                });

            const requestOptions = {
                method: "POST",
                headers: myHeaders,
                body: raw,
                redirect: "follow"
            };

            fetch("http://localhost:42613/set_snow_load", requestOptions)
                .then((response) => response.json())
                .then((result) =>
                {
                    let snowLoadData = JSON.parse(result);
                    let upwindData = snowLoadData['upwind'];
                    let downwindData = snowLoadData['downwind'];
                    document.getElementById('upwind-accumulation-factor').innerHTML = upwindData['factor']['ca'];
                    document.getElementById('downwind-accumulation-factor').innerHTML = downwindData['factor']['ca'];
                    document.getElementById('snow-load-upwind-uls').innerHTML = upwindData['s_uls'];
                    document.getElementById('snow-load-downwind-uls').innerHTML = downwindData['s_uls'];
                })
                .catch((error) => console.error(error));
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

// function createSeismicLoadComponent(zone_num){
//     return `
//     <hr>
//     <h5 id="seismic-load-component-hz-${zone_num}">Height Zone ${zone_num}</h5>
//     <hr>
//     <div class="row gx-5 ">
//         <div class="col-md-6">
//             <div class="mb-3">
//                 <label for="amplification-factor-hz-${zone_num}">Element of Component Force Amplification Factor (Ar)</label>
//                 <p>By default Ar has a value of 1</p>
//                 <input type="number" id="amplification-factor-hz-${zone_num}" class="form-control" value="1"/>
//             </div>
//             <div class="mb-3">
//                 <label for="response-modification-factor-hz-${zone_num}">Element of Component Response Modification Factor (Rp)</label>
//                 <p>By default Ar has a value of 2.5</p>
//                 <input type="number" id="response-modification-factor-hz-${zone_num}" class="form-control" value="2.5"/>
//             </div>
//             <div class="mb-3">
//                 <label for="component-factor-hz-${zone_num}">Elements of Component Factor (Cp)</label>
//                 <p>By default Ar has a value of 1</p>
//                 <input type="number" id="component-factor-hz-${zone_num}" class="form-control" value="1"/>
//             </div>
//         </div>
//         <div class="col-md-6">
//             <label for="seismic-load-hz-${zone_num}">Seismic Load</label>
//             <p id="seismic-load-hz-${zone_num}">NA</p>
//         </div>
//     </div>
//
//     `;
// }

function getWindLoadInputs(zone_num)
{
    let topographicFactor = document.getElementById(`topographic-factor-hz-${zone_num}`).value;
    let exposureFactor = document.querySelector(`input[name="exposure-factor-selection-hz-${zone_num}"]:checked`).id;
    let ceIntermediate;

    // if open
    if (exposureFactor === `exposure-factor-open-option-hz-${zone_num}`)
    {
        exposureFactor = 'open';
    }

    // if rough
    else if (exposureFactor === `exposure-factor-rough-option-hz-${zone_num}`)
    {
        exposureFactor = 'rough';
    }

    else if (exposureFactor === `exposure-factor-intermediate-option-hz-${zone_num}`)
    {
        exposureFactor = 'intermediate';
        ceIntermediate = document.getElementById(`ce-intermediate-hz-${zone_num}`).value;
    }

    let internalPressureCategory = document.querySelector(`input[name="internal-pressure-category-selection-hz-${zone_num}"]:checked`).id;

    // if enclosed
    if (internalPressureCategory === `internal-pressure-category-enclosed-option-hz-${zone_num}`)
    {
        internalPressureCategory = 'enclosed';
    }

    else if (internalPressureCategory === `internal-pressure-category-partially-enclosed-option-hz-${zone_num}`)
    {
        internalPressureCategory = 'partially_enclosed';
    }

    else if (internalPressureCategory === `internal-pressure-category-large-openings-option-hz-${zone_num}`)
    {
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

// function getSeismicLoadInputs(zone_num)
// {
//     let amplificationFactor = document.getElementById(`amplification-factor-hz-${zone_num}`).value;
//     let responseModificationFactor = document.getElementById(`response-modification-factor-hz-${zone_num}`).value;
//     let componentFactor = document.getElementById(`component-factor-hz-${zone_num}`).value;
//
//     console.log(amplificationFactor, responseModificationFactor, componentFactor);
//     return {
//         amplificationFactor,
//         responseModificationFactor,
//         componentFactor
//     };
// }

// wind-calculate-button press
document.getElementById('wind-calculate-button').addEventListener('click', () =>
{
    getWindLoads();
});

// seismic-calculate-button press
document.getElementById('seismic-calculate-button').addEventListener('click', () =>
{
    getSeismicLoads();
});

// snow-calculate-button press
document.getElementById('snow-calculate-button').addEventListener('click', () =>
{
    getSnowLoad();
});

function serialize()
{
    let objects = {
        load_page:
            {
                radio:
                    {},
                input:
                    {}
            }
    };

    // Handle radio inputs
    let radios = document.querySelectorAll('input[type=radio]');
    radios.forEach(radio =>
    {
        if (radio.checked)
        {
            objects.load_page.radio[radio.id] = radio.value;
        }
    });

    // Handle other inputs
    let inputs = document.querySelectorAll('input:not([type=radio])');
    inputs.forEach(input =>
    {
        if (input.value !== "")
        {
            objects.load_page.input[input.id] = input.value;
        }
    });

    let json = JSON.stringify(objects);
    return json;
}

function deserialize(json, section)
{
    return new Promise((resolve) =>
    {
        let objects = JSON.parse(json)[section];
        let totalElements = Object.keys(objects.radio).length + Object.keys(objects.input).length;
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
                input.value = '';
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


function loadSaveFile()
{
    window.api.invoke('get-token') // Retrieve the token
        .then((token) =>
        {
            const myHeaders = new Headers();
            myHeaders.append("Accept", "application/json");
            myHeaders.append("Authorization", `Bearer ${token}`);

            const requestOptions = {
                method: "POST",
                headers: myHeaders,
                redirect: "follow"
            };

            fetch("http://localhost:42613/get_user_current_save_file", requestOptions)
                .then((response) =>
                {
                    if (response.status === 200)
                    {
                        return response.json();
                    }
                    else
                    {
                        throw new Error('Get User Current Save File Error');
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
                        redirect: "follow"
                    };

                    fetch(`http://localhost:42613/get_user_save_file?id=${id}`, requestOptions)
                        .then((response) =>
                        {
                            if (response.status === 200)
                            {
                                return response.json();
                            }
                            else
                            {
                                throw new Error('Get User Save File Error');
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
                                redirect: "follow"
                            };

                            fetch(`http://localhost:42613/get_user_save_file?id=${id}`, requestOptions)
                                .then((response) =>
                                {
                                    if (response.status === 200)
                                    {
                                        return response.json();
                                    }
                                    else
                                    {
                                        throw new Error('Get User Save File Error');
                                    }
                                })
                                .then((result) =>
                                {
                                    deserialize(result.JsonData, 'load_page')
                                        .then(() =>
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
}

// save button click
document.getElementById('save-button').addEventListener('click', () =>
{
    // serialized = serialize();
    window.api.invoke('get-token') // Retrieve the token
        .then((token) =>
        {
            const myHeaders = new Headers();
            myHeaders.append("Accept", "application/json");
            myHeaders.append("Authorization", `Bearer ${token}`);

            const requestOptions = {
                method: "POST",
                headers: myHeaders,
                redirect: "follow"
            };

            fetch("http://localhost:42613/get_user_current_save_file", requestOptions)
                .then((response) =>
                {
                    if (response.status === 200)
                    {
                        return response.json();
                    }
                    else
                    {
                        throw new Error('Get User Current Save File Error');
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
                            "json_data": serialize(),
                            "id": id
                        });

                    const requestOptions = {
                        method: "POST",
                        headers: myHeaders,
                        body: raw,
                        redirect: "follow"
                    };

                    fetch("http://localhost:42613/set_user_save_data", requestOptions)
                        .then((response) => response.text())
                        .catch((error) => console.error(error));
                })
                .catch((error) => console.error(error));
        });
});

document.getElementById('back-button').addEventListener('click', function()
{
    window.location.href = 'input.html';
});

document.getElementById('home-button').addEventListener('click', function() {
    window.location.href = 'home.html';
});


// next button click
document.getElementById('next-button').addEventListener('click', function()
{
    // iterate through all the tables and ensure no NA values are present
    let allTables = document.querySelectorAll('table');
    let allTablesArray = Array.from(allTables);
    let allTablesText = allTablesArray.map(table => table.innerText);
    if (allTablesText.some(text => text.includes('NA')))
    {
        document.getElementById('next-warning').innerHTML = 'Please calculate all the loads before proceeding';
    }

    // iterate through all snow load inputs and ensure no NA values are present
    else if (document.getElementById('upwind-accumulation-factor').innerText === 'NA' || document.getElementById('downwind-accumulation-factor').innerText === 'NA' || document.getElementById('snow-load-upwind-uls').innerText === 'NA' || document.getElementById('snow-load-downwind-uls').innerText === 'NA')
    {
        document.getElementById('next-warning').innerHTML = 'Please calculate the snow load before proceeding';
    }

    else
    {
        window.location.href = 'results.html';
    }
});

function setUsernameDropdown()
{
    window.api.invoke('get-token') // Retrieve the token
        .then((token) =>{
            const myHeaders = new Headers();
            myHeaders.append("Accept", "application/json");
            myHeaders.append("Authorization", `Bearer ${token}`);

            const requestOptions = {
                method: "POST",
                headers: myHeaders,
                redirect: "follow"
            };

            fetch("http://localhost:42613/get_user_profile", requestOptions)
                .then((response) => response.json())
                .then((result) =>
                {
                    let data = JSON.parse(result);
                    username = data['username'];
                    document.getElementById('navbarDropdownMenuLink').textContent = username;
                })
                .catch((error) => console.error(error));
        });
}

// profile click event
document.getElementById("profile").addEventListener("click", function()
{
    window.location.href = 'profile.html';
});

// logout click event
document.getElementById("logout").addEventListener("click", function()
{
    window.api.invoke('store-token', '');
    window.location.href = 'login.html';
});

window.onload = function()
{
    loadSaveFile();
    setUsernameDropdown();

    toggleMenuColors('#roof-type-selection')

    let allWindLoadContainer = document.getElementById('all-wind-load-container');
    // let allSeismicLoadContainer = document.getElementById('seismic-load-table-container');
    let seismicLoadTable = document.getElementById('seismic-load-table');

    getNumHeightZones().then(numHeightZones =>
    {
        const selectors = [];
        for (let i = 1; i <= numHeightZones; i++)
        {
            allWindLoadContainer.innerHTML += createWindLoadComponent(i);
            selectors.push(`#exposure-factor-selection-hz-${i}`);
            selectors.push(`#internal-pressure-category-selection-hz-${i}`);
            document.getElementById(`ce-intermediate-hz-${i}`).style.display = 'none';
            // case if intermediate is selected
            waitForElement(`exposure-factor-intermediate-option-hz-${i}`, () =>
            {
                document.getElementById(`exposure-factor-intermediate-option-hz-${i}`).addEventListener('click', () =>
                {
                    document.getElementById(`ce-intermediate-hz-${i}`).style.display = 'block';
                });
            });
            // case if open is selected
            waitForElement(`exposure-factor-open-option-hz-${i}`, () =>
            {
                document.getElementById(`exposure-factor-open-option-hz-${i}`).addEventListener('click', () =>
                {
                    document.getElementById(`ce-intermediate-hz-${i}`).style.display = 'none';
                });
            });

            // case if rough is selected
            waitForElement(`exposure-factor-rough-option-hz-${i}`, () =>
            {
                document.getElementById(`exposure-factor-rough-option-hz-${i}`).addEventListener('click', () =>
                {
                    document.getElementById(`ce-intermediate-hz-${i}`).style.display = 'none';
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
            document.getElementById(`exposure-factor-selection-hz-${numHeightZones}`).addEventListener('click', () =>
            {
                document.getElementById('upwind-accumulation-factor').innerHTML = 'NA';
                document.getElementById('downwind-accumulation-factor').innerHTML = 'NA';
                document.getElementById('snow-load-upwind-uls').innerHTML = 'NA';
                document.getElementById('snow-load-downwind-uls').innerHTML = 'NA';
            });
        });

        selectors.forEach(selector => toggleMenuColors(selector));
    }).catch(error =>
    {
        console.error(error);
    });
};