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

function createHeightZoneComponent(zone_num)
{
    return `
    <hr>
    <h5>Height Zone ${zone_num}</h5>
    <hr>
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
    `;
}

window.onload = function()
{
    getNumHeightZones().then(numHeightZones => {
        const selectors = [];
        let allWindLoadContainer = document.getElementById('all-wind-load-container');
        for (let i = 1; i <= numHeightZones; i++)
        {
            allWindLoadContainer.innerHTML += createHeightZoneComponent(i);
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
        }
        selectors.forEach(selector => toggleMenuColors(selector));
    }).catch(error => {
        console.error(error);
    });
};