// https://stackoverflow.com/questions/69615993/how-to-group-array-of-dates-and-sum-value-by-day-1hour-6hours-8hours-week-m

function group_by_year(dataset_to_group, date_key) {
    return Object.values(
      arr.reduce((a, { x: date_string, y: value }) => {
        const { year } = get_date_parts(date_string);
        (a[year] ??= { color: 'Blue?', value: 0, label: year }).value += value;
  
        return a;
      }, {}),
    );
  }