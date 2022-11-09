// https://stackoverflow.com/questions/36975619/how-to-call-a-rest-web-service-api-from-javascript

async function download_rest_json(api_url) {
    const response = await fetch(api_url);
    const myJson = await response.json(); //extract JSON from the http response
    // do something with myJson
    return myJson;
  }

let GSHEET_URL = "https://script.google.com/macros/s/AKfycbx42OuLPncwWnsiTwX447DVCveMA_a-8GQuaxeB_h2TymNgcPL5G4-BpXG_4XapaBMruQ/exec";

console.log(download_rest_json(GSHEET_URL));