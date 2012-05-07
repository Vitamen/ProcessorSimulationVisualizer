/* on startup */
$("#benchmark-link").click(function() {
	populateBenchmarks();
});


/* populate the metrics list with valid metric types */
function benchmarkResponse(responseText, statusText, xhr, $form)  {
	$('#benchmark_form').empty();
	responseText = responseText.replace(/\'/g,"\"").replace(/u/g,"")
	var myjsonObject = JSON.parse(responseText);
	var benchmarks = myjsonObject.benchmarks;
	console.log(benchmarks);
	for (var i=0; i < benchmarks.length; i+=5) {
		var tableRowElement = $("<tr>");
		$('#benchmark_form').append(tableRowElement);
		var pos = 0;
		while (pos < 5 && i+pos < benchmarks.length) {
			var tableCellElement = $("<td>");
			
			var inputElement = $("<input>").attr("class", "benchmark_checkbox").attr("type", "checkbox")
											.attr("value",benchmarks[i+pos]).attr("name", "benchmarks");
			inputElement.append("<br>").append(benchmarks[i+pos]);
			tableRowElement.append(tableCellElement);
			tableCellElement.append(inputElement);
			pos++;
		}
	}
}

function populateBenchmarks() {
    var options = { 
        url: '/getBenchmarksFromExperiments',
        success: benchmarkResponse
    }; 
	$("#argForm").ajaxSubmit(options);
}