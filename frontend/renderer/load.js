function waitForElement(id, callback) {
    let intervalId = setInterval(function() {
        let element = document.getElementById(id);
        if (element) {
            clearInterval(intervalId);
            callback(element);
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

function getNumHeightZones() {
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

                fetch("http://localhost:42613/user_data", requestOptions)
                    .then((response) => response.json())
                    .then((result) => {
                        let userData = JSON.parse(result);
                        let numHeightZones = Object.keys(userData.building.height_zones).length;
                        resolve(numHeightZones); // Resolve the promise with numHeightZones
                    })
                    .catch((error) => {
                        console.error(error);
                        reject(error); // Reject the promise if there's an error
                    });
            });
    });
}

function createWindLoadComponent(zone_num)
{
    return `
    <hr>
    <h5>Height Zone ${zone_num}</h5>
    <hr>
    <div class="row gx-5 ">
        <div class="col-md-6">
        <div class="mb-3">
            <label for="topographic-factor">Topographic Factor (Ct)</label>
            <p>By default the topographic factor is 1</p>
            <input type="number" id="topographic-factor" class="form-control" value="1"/>
        </div>
        <div class="mb-3">
            <label for="exposure-factor-selection-hz-${zone_num}">Exposure Factor (Ce)</label>
            <br>
            <div class="btn-group btn-group-toggle" id="exposure-factor-selection-hz-${zone_num}" data-toggle="buttons">
                <label class="btn btn-secondary">
                    <input type="radio" name="exposure-factor-selection-hz-${zone_num}" id="exposure-factor-open-option-hz-${zone_num}" autocomplete="off"> Open
                </label>
                <label class="btn btn-secondary">
                    <input type="radio" name="exposure-factor-selection-hz-${zone_num}" id="exposure-factor-rough-option-hz-${zone_num}" autocomplete="off"> Rough
                </label>
                <label class="btn btn-secondary">
                    <input type="radio" name="exposure-factor-selection-hz-${zone_num}" id="exposure-factor-intermediate-option-hz-${zone_num}" autocomplete="off"> Intermediate
                </label>
            </div>
        </div>
        <div class="mb-3">
            <input type="number" id="cg-intermediate-hz-${zone_num}" class="form-control"/>
        </div>
        <div class="mb-3">
            <label>Gust Factor (Cg)</label>
            <p>2.5</p>
        </div>
        <div class="mb-3">
            <label for="internal-pressure-category-selection-hz-${zone_num}">Exposure Factor (Ce)</label>
            <br>
            <div class="btn-group btn-group-toggle" id="internal-pressure-category-selection-hz-${zone_num}" data-toggle="buttons">
                <label class="btn btn-secondary">
                    <input type="radio" name="einternal-pressure-category-selection-hz-${zone_num}" id="internal-pressure-category-enclosed-option-hz-${zone_num}" autocomplete="off"> Enclosed
                </label>
                <label class="btn btn-secondary">
                    <input type="radio" name="internal-pressure-category-selection-hz-${zone_num}" id="internal-pressure-category-partially-enclosed-option-hz-${zone_num}" autocomplete="off"> Partially Enclosed
                </label>
                <label class="btn btn-secondary">
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

function createSiesmicLoadComponent(zone_num){
    return `
    <hr>
    <h5>Height Zone ${zone_num}</h5>
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
            document.getElementById(`cg-intermediate-hz-${i}`).style.display = 'none';
            // case if intermediate is selected
            waitForElement(`exposure-factor-intermediate-option-hz-${i}`, () => {
                document.getElementById(`exposure-factor-intermediate-option-hz-${i}`).addEventListener('click', () => {
                    document.getElementById(`cg-intermediate-hz-${i}`).style.display = 'block';
                });
            });
            // case if open is selected
            waitForElement(`exposure-factor-open-option-hz-${i}`, () => {
                document.getElementById(`exposure-factor-open-option-hz-${i}`).addEventListener('click', () => {
                    document.getElementById(`cg-intermediate-hz-${i}`).style.display = 'none';
                });
            });

            // case if rough is selected
            waitForElement(`exposure-factor-rough-option-hz-${i}`, () => {
                document.getElementById(`exposure-factor-rough-option-hz-${i}`).addEventListener('click', () => {
                    document.getElementById(`cg-intermediate-hz-${i}`).style.display = 'none';
                });
            });

            allSeismicLoadContainer.innerHTML += createSiesmicLoadComponent(i);
        }
        selectors.forEach(selector => toggleMenuColors(selector));
    }).catch(error => {
        console.error(error);
    });


};