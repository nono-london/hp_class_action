

function simpleAverage(arr, item_key, window, round_decimal){
    let total = 0;
    for (let i=0; i<window; i++){
        total+=arr[i][item_key];
    }
    result = Math.round(total / window, round_decimal)
    return result;
}