function output_to_csv() {
	var chart_type = $('#chart_type').attr("value");
	var csv_string = "";
	if (chart_type == "HISTOGRAM") {
		for (var i = 0; i < visible_data.length; i++) {
			if (csv_string!="") {
				csv_string += "\n"
			}
			var data_array = visible_data[i].data;
			console.log(data_array);
			for (var j = 0; i < data_array.length; j++) {
				if (csv_string.charAt(csv_string.length-1) != "\n") {
					csv_string += ","
				}
				csv_string += data_array[j].toString();
			}
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