var color; // TODO remove
jQuery(document).ready(
		function() {
			jQuery('#vmap').vectorMap({
				map : 'cart_en',
				enableZoom : false,
				showTooltip : true,
				selectedColor : null,
				hoverColor: null,
				backgroundColor : '#ffffff00',
				borderWidth : 0.05,
				onRegionClick : function(event, code, region) {
					window.location.href = "/district/" + code;
				}
			});
			var paths = document.getElementById('vmap').getElementsByTagName(
					'g')[0];

			var createPath = function(d, id) {
				var path = document.createElementNS(
						'http://www.w3.org/2000/svg', 'path');
				path.setAttributeNS(null, 'd', d);
				path.setAttributeNS(null, 'stroke', '#000000');
				path.setAttributeNS(null, "stroke-width", 0.1);
				path.setAttributeNS(null, "stroke-linecap", 'round');
				path.setAttributeNS(null, "stroke-linejoin", 'round');
				path.setAttributeNS(null, "fill-opacity", 0);
				path.setAttribute('id', id);
				path.style["pointer-events"] = 'none';
				return path;
			}

			for ( var k in pathdata) {
				var path = createPath(pathdata[k], "outline-" + k);
				paths.appendChild(path);
			}
			
			color = function(dem_p) {
				var g;
				if (dem_p < 0.3) {
					g = dem_p*700;
					b = g;
					r = 255;
				} else if (dem_p > 0.7) {
					g = (1-dem_p)*700;
					r = g;
					b = 255;
				} else {
					g = 210;
					if (dem_p < 0.5) {
						r = 255;
						b = 210 + (255-210)/0.2*(dem_p-0.3);
					} else {
						b = 255;
						r = 210 + (255-210)/0.2*(0.7-dem_p);
					}
				}
				return "rgb("+Math.floor(r)+","+Math.floor(g)+","+Math.floor(b)+")";
			}
			for (var i = 1; i <= 435; ++i) {
				document.getElementById("jqvmap1_"+i).setAttributeNS(null,
																	 'fill',
																	 color(cartogram_data[i]));
				document.getElementById("jqvmap1_"+i).setAttributeNS(null,
						 'original',
						 color(cartogram_data[i]));
			}
		});
