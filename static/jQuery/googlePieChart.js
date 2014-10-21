

        // Load the Visualization API and the piechart package.
        google.load('visualization', '1.0', {'packages':['corechart']});

        // Set a callback to run when the Google Visualization API is loaded.
        google.setOnLoadCallback(drawChart);

        // Callback that creates and populates a data table,
        // instantiates the pie chart, passes in the data and
        // draws it.
        function drawChart() {

            $.get('/tellmeaboutit/pieChart/', function(data){


            });

            // Create the data table.
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Topping');
            data.addColumn('number', 'Slices');

            data.addRows([
                ['Mac',3],
                ['I-Pad', 1],
                ['KitKat', 1],
                ['I-Phone', 1],
                ['Sony Ericson', 2]
            ]);
            // Set chart options
            var options = {'title':'Top 5 things people are complaining about',
                'width':300,
                'height':300};
            // Instantiate and draw our chart, passing in some options.
            var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
            chart.draw(data, options);
        }
