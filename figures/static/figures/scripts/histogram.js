var accumData = [];
for (var i = 0; i < histogram_data.length; i++) {
	const val = (i == 0) ?
					histogram_data[i]['y'] :
					histogram_data[i]['y'] + accumData[i-1];
	accumData.push(val);
}

window.chart = new CanvasJS.Chart("chartContainer",
{
	title: {
		text: "Predicted Outcome - Dem Chance of Winning House: " + dem_win_perc + "%",
		fontFamily: "tahoma",
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
	  contentFormatter: function (e) {
		  var content = "";
		  for (var i = 0; i < e.entries.length; i++) {
			  content += `
			  <strong>${e.chart['axisX'][i]['title']}</strong>
			  : ${e.entries[i].dataPoint.x}</br>
			  <strong>${e.chart['axisY'][i]['title']}</strong>
			  : ${accumData[e.entries[i].index]}%</br>
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

	var xSnapDistance = chart.get("dataPointWidth") / 10;
	var xValue;
	var mouseDown = false;
	var selected = [];
	var timerId = null;

	// @ Pimp Trizkit
	// https://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color-or-rgb-and-blend-colors
	function shadeColor2(color, percent) {   
		var f=parseInt(color.slice(1),16),t=percent<0?0:255,p=percent<0?percent*-1:percent,R=f>>16,G=f>>8&0x00FF,B=f&0x0000FF;
		return "#"+(0x1000000+(Math.round((t-R)*p)+R)*0x10000+(Math.round((t-G)*p)+G)*0x100+(Math.round((t-B)*p)+B)).toString(16).slice(1);
	}

	function getPosition(e) {
		var parentOffset = $("#chartContainer > .canvasjs-chart-container").offset();          	
		var relX = e.pageX - parentOffset.left;
		xValue = Math.round(chart.axisX[0].convertPixelToValue(relX));
	}

	function searchDataPoint() {
		var dps = chart.data[0].dataPoints;
		for (var i = 0; i < dps.length; i++ ) {
			if((xValue >= dps[i].x - xSnapDistance && xValue <= dps[i].x + xSnapDistance)) 
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
							const color = shadeColor2(origColors[first+i], 0.2);
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
					const color = shadeColor2(origColors[first+i], 0.2);
					dps[first + i]['color'] = color;
				}
				mouseDown = false;
			}
			selected = [];
		}
	});

	// If user clicks outside of chart, reset all colors
	document.addEventListener("click", function(e) {
		if (e.target.closest("#chartContainer > .canvasjs-chart-container")) return;
		for (var i = 0; i < chart.data[0].dataPoints.length; i++) {
			chart.data[0].dataPoints[i]['color'] = origColors[i];
		}
		chart.render();
	})
}
