// const xValues = ["purchase date", "current date"];
// const yValues = [10, 11];

// // Determine line color based on the relationship between yValues[0] and yValues[1]
// const lineColor = yValues[0] < yValues[1] ? "rgba(0,255,0,1.0)" : "rgba(255,0,0,1.0)";

// new Chart("myChart", {
//   type: "line",
//   data: {
//     labels: xValues,
//     datasets: [{
//       fill: false,
//       lineTension: 0,
//       backgroundColor: lineColor,
//       borderColor: lineColor,
//       data: yValues
//     }]
//   },
//   options: {
//     legend: {display: false},
//     scales: {
//       yAxes: [{ticks: {min: 6, max: 16}}],
//     }
//   }
// });