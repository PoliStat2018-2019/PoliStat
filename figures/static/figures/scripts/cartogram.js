jQuery(document).ready(
		function() {
			jQuery('#vmap').vectorMap({
				map : 'cart_en',
				enableZoom : false,
				showTooltip : true,
				selectedColor : null,
				hoverColor : '#639',
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
		});