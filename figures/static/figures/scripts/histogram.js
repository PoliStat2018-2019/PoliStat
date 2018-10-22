var accumData = [];
var sum = 0;
for (var i = histogram_data.length - 1; i >= 0; i--) {
	sum += histogram_data[i]['y'];
	accumData.push(sum);
}
accumData.reverse();
const dataOffset = dem_win_perc - accumData[38];
accumData = accumData.map(function(x) {return x + dataOffset;});

window.chart = new CanvasJS.Chart("chartContainer",
{
	title: {
		text: "Predicted Outcome - Dem Chance of Winning House: " + dem_win_perc + "%",
		fontFamily: "Oswald",
	},
  subtitles: [
    {
        text: "Last Updated: " + update,
        fontColor: "gray",
        fontFamily: "tahoma",
    }
  ],
  axisY: {
		title: "% Probablility",
		minimum: 0
  },
  axisX: {
		title: "# of Democratic Seats"
  },
  data: [
	{
		type: "column",
		name: "# of Dem. Seats",
		dataPoints: histogram_data,
	}
  ],
  toolTip: {
	  enabled: true,
	  shared: true,
	  contentFormatter: function (e) {
		  var content = "";
		  for (var i = 0; i < e.entries.length; i++) {
			content += `
			<strong>% Probability of at least</strong>
			${e.entries[i].dataPoint.x}<br />
			<strong>Democrat Seats</strong>
			: ${accumData[e.entries[i].index].toFixed(2)}%</br>
			`;
		  }
		  return content;
	  }
  }
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

window.onload = function() {

	const origColors = chart.data[0].dataPoints.map((val, _ind, _arr) => {
		return val['color'];
	})
	const origContentFormatter = chart.toolTip.contentFormatter;

	var xSnapDistance = chart.get("dataPointWidth") / 10;
	var xValue;
	var mouseDown = false;
	var selected = [];
	var timerId = null;

	var popup = document.createElement("div");

	// @ Pimp Trizkit
	// https://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color-or-rgb-and-blend-colors
	function shadeColor2(color, percent) {   
		var f=parseInt(color.slice(1),16),t=percent<0?0:255,p=percent<0?percent*-1:percent,R=f>>16,G=f>>8&0x00FF,B=f&0x0000FF;
		return "#"+(0x1000000+(Math.round((t-R)*p)+R)*0x10000+(Math.round((t-G)*p)+G)*0x100+(Math.round((t-B)*p)+B)).toString(16).slice(1);
	}

	function resetChartColors() {
		for (var i = 0; i < chart.data[0].dataPoints.length; i++) {
			chart.data[0].dataPoints[i]['color'] = origColors[i];
		}
	}

	function getPosition(e) {
		var parentOffset = $("#chartContainer > .canvasjs-chart-container").offset();          	
		var relX = e.pageX - parentOffset.left;
		xValue = Math.round(chart.axisX[0].convertPixelToValue(relX));
	}

	function searchDataPoint() {
		var dps = chart.data[0].dataPoints;
		for (var i = 0; i < dps.length; i++ ) {
			if (xValue == dps[i].x) 
			{
				if(mouseDown) {
					selected.push(i);
					break;
				} else {
					changeCursor = true;
					break; 
				}
			} else {
				// selected = [];
				changeCursor = false;
			}
		}
	}

	jQuery("#chartContainer > .canvasjs-chart-container").on({
		mousedown: function(e) {
			// reset
			resetChartColors();
			popup.style.display= "none";

			mouseDown = true;
			getPosition(e);  
			searchDataPoint();
		},
		mousemove: function(e) {
			getPosition(e);
			searchDataPoint();
			if(mouseDown) {
				clearTimeout(timerId);
				timerId = setTimeout(function(){
					if(selected != []) {
						var dps = chart.data[0].dataPoints;
						var first = selected[0];
						var last = selected.slice(-1)[0];
						[first, last] = last < first ? [last, first] : [first, last];
						for (var i = 0; i < last - first; i++) {
							const color = shadeColor2(origColors[first+i], -0.5);
							dps[first + i]['color'] = color;
						}
						chart.render();
					}   
				}, 0);
			}
			else {
				searchDataPoint();
				if(changeCursor) {
					chart.data[0].set("cursor", "grabbed");
				} else {
					chart.data[0].set("cursor", "grab");
				}
			}
		},
		mouseup: function(e) {
			if(selected != []) {
				var dps = chart.data[0].dataPoints;
				var first = selected[0];
				var last = selected.slice(-1)[0];
				[first, last] = last < first ? [last, first] : [first, last];
				for (var i = 0; i < last - first; i++) {
					const color = shadeColor2(origColors[first+i], -0.5);
					dps[first + i]['color'] = color;
				}

				var chartContainer = document.querySelector("#chartContainer > .canvasjs-chart-container");
				popup.innerHTML = `
				<strong>Selected Range:</strong><br />
				${dps[first]['x']}-${dps[last]['x']}<br />
				<strong>Probability</strong>
				: ${(accumData[first]-accumData[last]).toFixed(2)}%</br>`;
				popup.classList.add("chart-popup");

				// Popup styles
				chartContainer.appendChild(popup);
				style = {
					position: "absolute",
					top: "150px",
					right: "0",
					display: "block",
					zIndex: 100,
					border: "2px solid black",
					padding: "15px",
					width: "185px",
					backgroundColor: "white"
				}
				Object.assign(popup.style, style);

				mouseDown = false;
			}
			selected = [];
		}
	});

	// If user clicks outside of chart, reset all colors
	document.addEventListener("click", function(e) {
		if (e.target.closest("#chartContainer > .canvasjs-chart-container")) return;
		resetChartColors();
		popup.style.display = "none";
		chart.render();
	})
}
