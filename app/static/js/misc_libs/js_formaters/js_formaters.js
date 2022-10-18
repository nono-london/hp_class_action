function LinkFormatter(value, row, index) {
    try {
        return "<a href='"+value+"' target='_blank'>link</a>";
    } catch (error) {
        console.log("Error while building urls:"+error);
        return "<a>No URL Found</a>";
    }

};

function dateFormat(value, row, index) {
    try {

        return new Date(value).toDateString();
    } catch (error) {
        console.log("Error while Formatting date: '"+value+"'', Error: "+error);
        return value;
    }

};

function buysellFormat(value, row, index) {
    try {
            if (value=="Buy") {
                return "<p style=color:blue><b>"+value+"</b></p>";
                
            } 
            if (value=="Sell") {
                return "<p style=color:red><b>"+value+"</b></p>";
                
            } 
            else {
                return value;
                
            }
        return new Date(value).toDateString();
    } catch (error) {
        console.log("Error while Formatting date: '"+value+"'', Error: "+error);
        return value;
    }

};


function numberFormat(value, row, index) {
    try {
        _sep=",";
        let is_value_neg;
        if (value<0){
            is_value_neg=true;
            value = value * -1;
        }
        value = value.toString();

        value = typeof value != "undefined" && value > 0 ? value : "";
        
        value = value.replace(new RegExp("^(\\d{" + (value.length%3? value.length%3:0) + "})(\\d{3})", "g"), "$1 $2").replace(/(\d{3})+?/gi, "$1 ").trim();
        if(typeof _sep != "undefined" && _sep != " ") {
            value = value.replace(/\s/g, _sep);
        }
        if (is_value_neg==true){
            value="-" + value;
        }

        return value;        
    } catch (error) {
        console.log("error with numberFormat"+String(error));
    }

};


function percentFormat(value, row, index) {
    try {
        return String((value*100).toFixed(2)).concat(" %");
    } catch (error) {
        console.log("error with percentFormat"+String(error));
        return "err.";
    }

};