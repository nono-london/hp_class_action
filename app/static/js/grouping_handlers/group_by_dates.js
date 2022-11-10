// https://stackoverflow.com/questions/69615993/how-to-group-array-of-dates-and-sum-value-by-day-1hour-6hours-8hours-week-m


function get_year_month_parts(date_as_date){
    month = timestamp_to_month(date_as_date);
    year = timestamp_to_year(date_as_date);
    
    return {year, month};

}

function group_by_month(arr, date_key) {
    return Object.values(
      arr.reduce((a, { date_key: date_as_date, date_key: value }) => {
        const { year, month } = get_year_month_parts(date_as_date) ;
        const key = `${year}/${month}`;
        // using logical nullish assignment
        //(a[key] ??= { color: 'Blue?', value: 0, label: key }).value += value;
  
        // or written out long hand
        if (a[key] === undefined) {
          a[key] = { color: 'Blue?', value: 0, date_key: key };
        }
  
        a[key].value += 1;
  
        return a;
      }, {}),
    );
}
const group_by_m_dataset = group_by_month(json_dataset['data'], 'post_id');
console.log(group_by_m_dataset);