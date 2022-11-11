// https://css-tricks.com/the-many-ways-of-getting-data-into-charts/
// uses chartjs
// <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.js" integrity="sha512-d6nObkPJgV791iTGuBoVC9Aa2iecqzJRE0Jiqvk85BhLHAPhWqkuBiQb1xz2jvuHNqHLYoN3ymPfpiB1o+Zgpw==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>



const chartBackgroundColor = [ // Specify custom colors
  'rgba(255, 99, 132, 0.2)',
  
  'rgba(54, 162, 235, 0.2)',
  'rgba(255, 206, 86, 0.2)',
  'rgba(75, 192, 192, 0.2)',
  'rgba(153, 102, 255, 0.2)',
  'rgba(255, 159, 64, 0.2)',

  'rgba(255, 130, 132, 0.2)',
];

const chartBorderColor = [ // Add custom color borders
  'rgba(255,99,132,1)',
  
  'rgba(54, 162, 235, 1)',
  'rgba(255, 206, 86, 1)',
  'rgba(75, 192, 192, 1)',
  'rgba(153, 102, 255, 1)',
  'rgba(255, 159, 64, 1)',

  'rgba(255, 130, 132, 1)',
];



// this function works for sure
function chartJsBuilder(canvas_id, chart_type, color_slice_start, color_slice_end,
  x_values, y_values, chart_title) {
  const chart_graph = new Chart(canvas_id, {
    type: chart_type,
    data: {
      labels: x_values,
      datasets: [{
        label: chart_title,
        //barPercentage: 0.5,
        //barThickness: 6,
        //maxBarThickness: 8,
        //minBarLength: 200,
        data: y_values,
        backgroundColor: chartBackgroundColor.slice(color_slice_start, color_slice_end),
        borderColor: chartBorderColor.slice(color_slice_start, color_slice_end),
        borderWidth: 1 // Specify bar border width


      }]
    },
    options: {
      responsive: true, // Instruct chart js to respond nicely.
      maintainAspectRatio: true, // Add to prevent default behavior of full-width/height 
    }
  }
  )
  // return chart so that it can be destroyed before calling this function if it already exists
  // define the chart in a var golbal variable on document
  return chart_graph;

}


function chartJsBuilderMultipleDatasets(canvas_id, chart_type, datasets, serie_names, stacked) {
    // datasets should be composed of a list of list containing x_values, and y_values
    // [ [x_values, y_values],
    //   [x_values, y_values],
    //  ]
    // getting unique x_values
    let x_values = new Set();
    datasets.forEach(function(dataset){
      //select x_values 1st list
      dataset.forEach(function(row_dict){
        x_values.add(Object.values(row_dict)[0]);
      })
    })
    // create datasets for chartjs
  let chart_datasets=[];
  for (let i=0;i<serie_names.length;i++){
    let y_values = [];
    datasets[i].forEach(function(row_dict){
      //select y_values 2nd list
      y_values.push(Object.values(row_dict)[1]);
    })
    const chart_dataset = create_chartjs_dataset(y_values,serie_names[i], i, i+1);
    chart_datasets.push(chart_dataset);
  }
  let scale_option = {}
  // scale/stack bars
  if (stacked===true){
    console.log("stacked is True with ===")
    scale_option = {
      x: {
        stacked: true,
      },
      y: {
        stacked: true
      }
    };
  }
  console.log(scale_option);


  // Bulding data in Chart
  const chart_graph = new Chart(canvas_id, {
    type: chart_type,
    data: {
      labels: Array.from(x_values),
      datasets: chart_datasets
    },

    responsive: true,
    scales: scale_option
  }
  )
  // return chart so that it can be destroyed before calling this function if it already exists
  // define the chart in a var golbal variable on document
  return chart_graph;

}



function create_chartjs_dataset(y_values, serie_name, color_slice_start, color_slice_end){
  let chart_dataset = {
    label: serie_name,
    //barPercentage: 0.5,
    //barThickness: 6,
    //maxBarThickness: 8,
    //minBarLength: 200,
    data: y_values,
    backgroundColor: chartBackgroundColor.slice(color_slice_start, color_slice_end),
    borderColor: chartBorderColor.slice(color_slice_start, color_slice_end),
    borderWidth: 1 // Specify bar border width
  }
  return chart_dataset;
}