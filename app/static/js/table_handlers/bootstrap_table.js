

function table_populator(data_for_table, table_to_populate, dataSetHasBeenJONed=false) {
    //table_to_populate.bootstrapTable('destroy');
    // console.log('inner table populator');
    // console.log(data_for_table);


        if (data_for_table !=null) {
            if (dataSetHasBeenJONed==true){
                console.log("boostrap-table function DO NOt need to be parsed");
                table_to_populate.bootstrapTable({data:data_for_table});    
            }
            else{
                console.log("boostrap-table data need to be parsed");
                data_for_table = JSON.parse(data_for_table);
                table_to_populate.bootstrapTable({data: data_for_table});    
            }
            
        } else {
            console.log('No data found for table:'+table_to_populate);
            //table_to_populate.bootstrapTable({data:null});
            table_to_populate.bootstrapTable();
        }
        


    

};