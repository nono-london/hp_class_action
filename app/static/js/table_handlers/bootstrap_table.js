

function table_populator(table_dataset, table_to_populate, dataSetHasBeenJONed=false) {
    //table_to_populate.bootstrapTable('destroy');
    // console.log('inner table populator');
    // console.log(table_dataset);
    table_dataset.forEach(element => {
        console.log(element);
        
    });

    // table_to_populate.bootstrapTable({
    //     data: table_dataset
    //   });





        if (table_dataset !=null) {
            if (dataSetHasBeenJONed==true){
                console.log("boostrap-table function DO NOt need to be parsed");
                table_to_populate.bootstrapTable({data:table_dataset});    
            }
            else{
                console.log("boostrap-table data need to be parsed");
                table_dataset = JSON.parse(table_dataset);
                table_to_populate.bootstrapTable({data: table_dataset});    
            }
            
        } else {
            console.log('No data found for table:'+table_to_populate);
            //table_to_populate.bootstrapTable({data:null});
            table_to_populate.bootstrapTable();
        }
        


    

};