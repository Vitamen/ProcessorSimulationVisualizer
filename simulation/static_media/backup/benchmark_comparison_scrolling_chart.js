var chart;
var scrolling_parsed_names = new Array();
var scrolling_parsed_data = new Array();

var scrolling_parsed_names_2 = new Array();
var scrolling_parsed_data_2 = new Array();

var i=0;
for (var key in core_data) {
	if (i >= 10) {
		break;
	}
	var data_item = core_data.shift();
	for (var parsed_key in data_item) {
		scrolling_parsed_names[i] = parsed_key.replace("Z",".");
		scrolling_parsed_data[i++] = data_item[parsed_key];
	}
}

i=0;
for (var key in core_data_2) {
	if (i >= 10) {
		break;
	}
	var data_item_2 = core_data_2.shift();
	for (var parsed_key_2 in data_item_2) {
		scrolling_parsed_names_2[i] = parsed_key_2.replace("Z",".");
		scrolling_parsed_data_2[i++] = data_item_2[parsed_key_2];
	}
}

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'container3',
            type: 'column',
            events: {
                click: function() {
                    var series1 = this.series[0];
                    var series2 = this.series[1];
                    var categories = this.xAxis[0].categories;
                
                    var data_object = core_data.shift();
                    var data_object_2 = core_data_2.shift();
                    var scrolling_parsed_data_point;
                    var scrolling_parsed_data_point_2;
                    var scrolling_parsed_name;
                    for (var key in data_object) {
                    	scrolling_parsed_data_point = data_object[key];
                    	scrolling_parsed_name = key.replace("Z",".");
                    };
                    for (var key2 in data_object_2) {
                    	scrolling_parsed_data_point_2 = data_object_2[key2]
                    };

                    categories.push(scrolling_parsed_name);
                    series1.addPoint(scrolling_parsed_data_point, true, true);
                    series2.addPoint(scrolling_parsed_data_point_2, true, true);
                }
            },
        },
        title: {
            text: '100M_np_base benchmark chart for core_insn_fetched and core_insn_fetched_onpath'
        },
        xAxis: {
            categories:scrolling_parsed_names
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Rainfall (mm)'
            }
        },
        legend: {
            layout: 'vertical',
            backgroundColor: '#FFFFFF',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            shadow: true
        },
        tooltip: {
            formatter: function() {
                return ''+
                    this.x +': '+ this.y +' mm';
            }
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Experiment 1',
            data: scrolling_parsed_data

        }, {
            name: 'Experiment 2',
            data: scrolling_parsed_data_2
        },
        ]
    });
});
