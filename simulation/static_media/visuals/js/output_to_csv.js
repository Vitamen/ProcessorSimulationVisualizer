function output_to_csv() {
	var chart_type = $('#chart_type').attr("value");
	var csv_string = "";
	if (chart_type == "HISTOGRAM") {
		var data_array = visible_data[0].data;
		for (var i = 0; i < data_array.length; i++) {
			if (csv_string != "") {
				csv_string += ","
			}
			csv_string += data_array[i].toString();
		}
	} else if (chart_type == "SCATTERPLOT") {
		for (var i = 0; i < visible_data.length; i++) {
			if (csv_string != "") {
				csv_string += ","
			}
			csv_string += visible_data[i][1].toString();
		}
	}
	alert(csv_string);
}