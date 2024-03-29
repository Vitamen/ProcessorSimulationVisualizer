var scriptLoader = {
	_loadScript: function (url, callback) {
		var head = document.getElementsByTagName('head')[0];
		var script = document.createElement('script');
		script.type = 'text/javascript';
		script.src = url;
		if (callback) {
			script.onreadystatechange = function () {
				if (this.readyState == 'loaded') callback();
			}
			script.onload = callback;
		}
		head.appendChild(script);
	},
 
	load: function (items, iteration) {
		if (!iteration) iteration = 0;
		if (items[iteration]) {
			scriptLoader._loadScript(
				items[iteration],
				function () {
					scriptLoader.load(items, iteration+1);
				}
			)
		}
	}
}