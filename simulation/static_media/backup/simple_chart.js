 var data = [4, 8, 15, 16, 23, 42];
 
 w = 400,
 h = 200,
 margin = 20,
 
 y = d3.scale.linear().domain([0, d3.max(data)]).range([0 + margin, h - margin]),
 x = d3.scale.linear().domain([0, data.length]).range([0 + margin, w - margin])
 
 var chart = d3.select("body").append("svg")
 			.attr("class", "chart")
 			.attr("width", w)
 			.attr("height", h);
 
 chart.selectAll("rect")
 	.data(data)
 	.enter().append("rect")
 	.attr("x", function(d, i) {return x(i) - 0.5})
	.attr("y", function(d) {return h-y(d)-0.5})
	.attr("width", w/data.length - margin)
	.attr("height", function(d) {return y(d)})
	.text(function(d) { return d; });
 
 var test = 'blah';