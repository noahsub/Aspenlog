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
        console.log(ulsWallSelection);
        console.log(slsWallSelection);
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
        console.log(ulsWallSelection);
        console.log(slsWallSelection);
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
        console.log(ulsRoofSelection);
        console.log(slsRoofSelection);
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
        console.log(ulsRoofSelection);
        console.log(slsRoofSelection);
    }
});

window.onload = function()
{

};