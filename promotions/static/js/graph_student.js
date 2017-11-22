function generateGraph(username, data) {
    var data_parsed = jQuery.parseJSON(data);
    console.log(data_parsed.data);

    var xtest = data_parsed.xaxis,
        yz = [[], []],
        xmonthz = ["Septembre", "Octobre", "Novembre", "Décembre"];

    data_parsed.data.forEach(function (item) {
        yz[0].push(item["acquired"]);
        yz[1].push(item["not-acquired"]);
    });

    var y01z = d3.stack().keys(d3.range(2))(d3.transpose(yz));

    var svg = d3.select("svg#"+username.replace(".","\\."));

    var margin = {top: 40, right: 10, bottom: 20, left: 10},
        width = +svg.attr("width") - margin.left - margin.right,
        height = +svg.attr("height") - margin.top - margin.bottom,
        g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        g.on("click", function(){
            d3.request("viewStat/"+username + "/").get(function(data) {
                console.log(data)
            })
        });

    // Determine the position of the bar in the graph (relative to the width of the graph)

    var x = d3.scaleBand()
        .domain(xtest)
        .rangeRound([0, width])
        .padding(0);


    var xmonth = d3.scaleBand()
        .domain(xmonthz)
        .rangeRound([0, width])
        .padding(0);

    var y = d3.scaleLinear()
        .domain([0, 12])
        .range([height, 0]);

    // Color for the graph. The first color is for the acquired skill (green) and the second for the non-acquired (orange)
    var color = ["#33cc00", "#ff8c1a"];

    var series = g.selectAll(".series")
        .data(y01z)
        .enter().append("g")
        .attr("fill", function (d, i) {
            return color[i];
        });

    var rect = series.selectAll("rect")
        .data(function (d) {
            return d;
        })
        .enter().append("rect")
        .attr("x", function (d, i) {
            return x(xtest[i]);
        })
        .attr("y", function (d) {
            return y(d[1]);
        })
        .attr("width", x.bandwidth())
        .attr("height", function (d) {
            return y(d[0]) - y(d[1]);
        });
    /* Do not need this for the global view with all student
    g.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x)
            .tickSize(0)
            .tickPadding(0));

    g.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xmonth)
            .tickSize(0)
            .tickPadding(10));
    */
}

$(".graph-student").each(function() {
    var username = $(this.getAttribute("id")).selector;
    var lesson = $(this.getAttribute("lesson")).selector;
    var uaa = $(this.getAttribute("uaa")).selector;

    d3.request(encodeURI("/professor/lesson/" + lesson + "/getStat/"+username + "/" + uaa + "/"))
        .get(function(data) {
            if (data === null) {
                console.log("no data");
            } else {
                var dic = data.response;
                generateGraph(username, dic);
            }
    });

});