window.chart = new CanvasJS.Chart("chartContainer",
{
	title: {
  	text: "Predicted Outcome - Dem Chance of Winning House: " + dem_win_perc + "%",
  	fontFamily: "tahoma",
  },
  subtitles:[
    {
        text: "Last Updated: " + update,
        fontColor: "gray",
        fontFamily: "tahoma",
    }
  ],
  axisY: {
		title: "% Probablility"
	},
  axisX: {
		title: "# of Democratic Seats"
	},
	data: [
	{
		type: "column",
		dataPoints: histogram_data,
	}
	]
});

chart.render();

//get("propertyName");
//set("propertyName", value, updateChart);

//updateChart = false
chart.set("dataPointWidth",Math.ceil(chart.axisX[0].bounds.width/chart.data[0].dataPoints.length),true);

//On Resize chart width changes so as the plotArea, so dataPointWidth will vary according to width
$( window ).resize(function() {
	chart.set("dataPointWidth",Math.ceil(chart.axisX[0].bounds.width/chart.data[0].dataPoints.length),true);
});
