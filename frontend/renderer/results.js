let ulsWallSelection;
let slsWallSelection;
let ulsRoofSelection;
let slsRoofSelection;

document.getElementById('uls-wall-selection').addEventListener('change', function(e)
{
    let selectedOption = e.target.id;
    switch (selectedOption)
    {
        case "uls-wall-selection-dead-only-1-4D-option":
            ulsWallSelection = 'uls_1.4D';
            break;
        case "uls-wall-selection-full-wind-1-25D-1-4Wy-option":
            ulsWallSelection = 'uls_1.25D_1.4Wy';
            break;
        case "uls-wall-selection-seismic-1-0D-1-0Ey-option":
            ulsWallSelection = 'uls_1.0D_1.0Ey';
            break;
        case "uls-wall-selection-seismic-1-0D-1-0Ex-option":
            ulsWallSelection = 'uls_1.0D_1.0Ex';
            break;
    }

    if (ulsWallSelection !== undefined && slsWallSelection !== undefined)
    {
        getWallLoadCombinations();
    }
});

document.getElementById('sls-wall-selection').addEventListener('change', function(e)
{
    let selectedOption = e.target.id;
    switch (selectedOption)
    {
        case "sls-wall-selection-1-0D-1-0Wy-option":
            slsWallSelection = 'sls_1.0D_1.0Wy';
            break;
    }

    if (ulsWallSelection !== undefined && slsWallSelection !== undefined)
    {
        getWallLoadCombinations();
    }
});

document.getElementById('uls-roof-selection').addEventListener('change', function(e)
{
    let selectedOption = e.target.id;
    switch (selectedOption)
    {
        case "uls-roof-selection-dead-only-1-4D-option":
            ulsRoofSelection = 'uls_1.4D';
            break;
        case "uls-roof-selection-full-wind-1-25D-1-4Wy-option":
            ulsRoofSelection = 'uls_1.25D_1.4Wy';
            break;
        case "uls-roof-selection-seismic-1-0D-1-0Ey-option":
            ulsRoofSelection = 'uls_1.0D_1.0Ey';
            break;
        case "uls-roof-selection-seismic-1-0D-1-0Ex-option":
            ulsRoofSelection = 'uls_1.0D_1.0Ex';
            break;
        case "uls-roof-selection-full-snow-with-wind-1-25D-1-5S-option":
            ulsRoofSelection = 'uls_1.25D_1.5S';
            break;
    }

    if (ulsRoofSelection !== undefined && slsRoofSelection !== undefined)
    {
        getRoofLoadCombinations()
    }
});

document.getElementById('sls-roof-selection').addEventListener('change', function(e)
{
    let selectedOption = e.target.id;
    switch (selectedOption)
    {
        case "sls-roof-selection-dead-and-wind-y-normal-to-face-1-0D-1-0Wy-option":
            slsRoofSelection = 'sls_1.0D_1.0Wy';
            break;
        case "sls-roof-selection-full-snow-with-wind-y-1-0D-1-0S-option":
            slsRoofSelection = 'sls_1.0D_1.0S';
            break;
        case "sls-roof-selection-dead-and-live-1-0D-1-0L-option":
            slsRoofSelection = 'sls_1.0D_1.0L_WY';
            break;
    }

    if (ulsRoofSelection !== undefined && slsRoofSelection !== undefined)
    {
        getRoofLoadCombinations()
    }
});

function getWallLoadCombinations()
{
    window.api.invoke('get-token') // Retrieve the token
        .then((token) =>{
            const myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            myHeaders.append("Accept", "application/json");
            myHeaders.append("Authorization", `Bearer ${token}`);

            const raw = JSON.stringify({
                "uls_wall_type": ulsWallSelection,
                "sls_wall_type": slsWallSelection
            });

            const requestOptions = {
                method: "POST",
                headers: myHeaders,
                body: raw,
                redirect: "follow"
            };

            fetch("http://localhost:42613/get_wall_load_combinations", requestOptions)
                .then((response) => response.text())
                .then((result) => {
                    let data = JSON.parse(result);
                    console.log(data);
                    let table = document.getElementById('wall-combination-table');
                    table.innerHTML = "";
                    let tableString = "";
                    tableString += '<thead>'
                    tableString += '<tr>'
                    let headers = Object.keys(data[0]);
                    tableString += `<th>Height Zone</th>`;
                    headers.forEach((header) => {
                        tableString += `<th>${header}</th>`;
                    });
                    tableString += '<tr>'
                    tableString += '</thead>'
                    tableString += '<tbody>'
                    for (let i = 0; i < data.length; i++)
                    {
                        tableString += '<tr>'
                        let values = Object.values(data[i]);
                        let newValues = [i + 1].concat(values);
                        newValues.forEach((value) => {
                            tableString += `<td>${value}</td>`;
                        });
                        tableString += '</tr>'
                    }
                    tableString += '</tbody>'
                    table.innerHTML = tableString;
                })
                .catch((error) => console.error(error));
        });

}

function getRoofLoadCombinations()
{
    window.api.invoke('get-token') // Retrieve the token
        .then((token) =>{
            const myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            myHeaders.append("Accept", "application/json");
            myHeaders.append("Authorization", `Bearer ${token}`);

            const raw = JSON.stringify({
                "uls_roof_type": ulsRoofSelection,
                "sls_roof_type": slsRoofSelection
            });

            const requestOptions = {
                method: "POST",
                headers: myHeaders,
                body: raw,
                redirect: "follow"
            };

            fetch("http://localhost:42613/get_roof_load_combinations", requestOptions)
                .then((response) => response.text())
                .then((result) => {
                    let data = JSON.parse(result);
                    console.log(data);
                    let table = document.getElementById('roof-combination-table');
                    table.innerHTML = "";
                    let tableString = "";
                    tableString += '<thead>'
                    tableString += '<tr>'
                    let headers = Object.keys(data[0]);
                    tableString += `<th>Height Zone</th>`;
                    headers.forEach((header) => {
                        tableString += `<th>${header}</th>`;
                    });
                    tableString += '<tr>'
                    tableString += '</thead>'
                    tableString += '<tbody>'
                    for (let i = 0; i < data.length; i++)
                    {
                        tableString += '<tr>'
                        let values = Object.values(data[i]);
                        let newValues = [i + 1].concat(values);
                        newValues.forEach((value) => {
                            tableString += `<td>${value}</td>`;
                        });
                        tableString += '</tr>'
                    }
                    tableString += '</tbody>'
                    table.innerHTML = tableString;
                })
                .catch((error) => console.error(error));
        });
}

window.onload = function()
{

};