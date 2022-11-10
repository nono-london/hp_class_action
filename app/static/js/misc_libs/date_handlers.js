

function timestamp_to_date(timestamp_str){
    // Return the date of the timestamp
    // timestamp shoud be of the form %Y-%m-%d %etc
    date_str = String(timestamp_str).split(" ")[0];
    return new Date(date_str);
}

function timestamp_to_day(timestamp_str){
    // Return the day of the timestamp
    // timestamp shoud be of the form %Y-%m-%d %etc
    date_str = String(timestamp_str).split(" ")[0];
    day_int = parseInt(date_str.split("-")[2]);
    return day_int;
    }
function timestamp_to_month(timestamp_str){
    // Return month of the timestamp
    // timestamp shoud be of the form %Y-%m-%d %etc
    date_str = String(timestamp_str).split(" ")[0];
    month_int = parseInt(date_str.split("-")[1]);
    return month_int;
    }
function timestamp_to_year(timestamp_str){
    // Return year of the timestamp
    // timestamp shoud be of the form %Y-%m-%d %etc
    date_str = String(timestamp_str).split(" ")[0];
    year_int = parseInt(date_str.split("-")[0]);
    return year_int;
    }


//console.log(timestamp_to_day("2022-01-30"));
