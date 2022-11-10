// https://css-tricks.com/the-many-ways-of-getting-data-into-charts/

const chartBackgroundColor = [ // Specify custom colors
  'rgba(255, 99, 132, 0.2)',
  'rgba(54, 162, 235, 0.2)',
  'rgba(255, 206, 86, 0.2)',
  'rgba(75, 192, 192, 0.2)',
  'rgba(153, 102, 255, 0.2)',
  'rgba(255, 159, 64, 0.2)'
];

const chartBorderColor = [ // Add custom color borders
  'rgba(255,99,132,1)',
  'rgba(54, 162, 235, 1)',
  'rgba(255, 206, 86, 1)',
  'rgba(75, 192, 192, 1)',
  'rgba(153, 102, 255, 1)',
  'rgba(255, 159, 64, 1)'
];


function jsChartBuilder(labels, values, chartTitle, chartCanvasId, chartType) {
  // var ctx = document.getElementById("myChart").getContext('2d');
  var myChart = new Chart(chartCanvasId, {
    type: chartType,
    data: {
      labels: labels, // Our labels
      datasets: [{
        label: chartTitle, // Name the series
        data: values, // Our values
        backgroundColor: [ // Specify custom colors
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(255, 159, 64, 0.2)'
        ],
        borderColor: [ // Add custom color borders
          'rgba(255,99,132,1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)'
        ],
        borderWidth: 1 // Specify bar border width
      }]
    },
    options: {
      responsive: true, // Instruct chart js to respond nicely.
      maintainAspectRatio: false, // Add to prevent default behavior of full-width/height 
    }
  });
  return myChart;
};


// this function works for sure
// uses chartjs
//     <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.js" integrity="sha512-d6nObkPJgV791iTGuBoVC9Aa2iecqzJRE0Jiqvk85BhLHAPhWqkuBiQb1xz2jvuHNqHLYoN3ymPfpiB1o+Zgpw==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>

function createChart(canvas_id, chart_type, color_slice_start, color_slice_end,
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
        backgroundColor: [ // Specify custom colors
          'rgba(255, 99, 132, 0.2)',
          'rgba(255, 130, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(255, 159, 64, 0.2)'
        ].slice(color_slice_start, color_slice_end),
        borderColor: [ // Add custom color borders
          'rgba(255,99,132,1)',
          'rgba(255, 130, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)'
        ].slice(color_slice_start, color_slice_end),
        borderWidth: 1 // Specify bar border width


      }]
    },

  }
  )

}
