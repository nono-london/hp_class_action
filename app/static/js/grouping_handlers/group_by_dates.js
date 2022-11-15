// https://stackoverflow.com/questions/69615993/how-to-group-array-of-dates-and-sum-value-by-day-1hour-6hours-8hours-week-m


function get_year_month_day_parts(date_as_date){
    month = timestamp_to_month(date_as_date);
    year = timestamp_to_year(date_as_date);
    day =  timestamp_to_day(date_as_date);
    return {year, month, day};

}

function group_by_year(arr, date_key) {
  return Object.values(
    arr.reduce((a, { [date_key]: date_as_date, claims: count }) => {
      // console.log("a");
      // console.log(a);
      // console.log("date_as_date");
      // console.log(date_as_date);
      // console.log(a);
      const year = timestamp_to_year(date_as_date) ;
      const key = `${year}`;

      if (a[key] === undefined) {
        a[key] = {[date_key]: key, count: 0,  };
      }

      a[key].count += 1;

      return a;
    }, {}),
  );
}

function group_by_month(arr, date_key) {
  return Object.values(
    arr.reduce((a, { [date_key]: date_as_date, claims: count }) => {
      const { year, month } = get_year_month_day_parts(date_as_date) ;
      const key = `${year}-${('0'+month).slice(-2)}`;

      if (a[key] === undefined) {
        a[key] = {[date_key]: key, count: 0,  };
      }

      a[key].count += 1;

      return a;
    }, {}),
  );
}

function group_by_day(arr, date_key) {

  return Object.values(
    arr.reduce((new_array, { [date_key]: date_as_date, date_key: count }) => {

      const { year, month, day } = get_year_month_day_parts(date_as_date) ;
      const key = `${year}-${('0'+month).slice(-2)}-${('0'+day).slice(-2)}`;

      if (new_array[key] === undefined) {
        new_array[key] = {[date_key]: key, count: 0,  };
      }

      new_array[key].count += 1;

      return new_array;
    }, {}),
  );
}


