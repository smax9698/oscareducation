function generateGraph(username, data) {


    var data_parsed = jQuery.parseJSON(data);

    var xz = data_parsed.xaxis,
        yz = [[], []];

    data_parsed.data.forEach(function (item) {
        yz[0].push(item["acquired"]);
        yz[1].push(item["not-acquired"]);
    });

    var y01z = d3.stack().keys(d3.range(2))(d3.transpose(yz));


    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .style('border', '1px solid #fff')
        .style('box-shadow', '1px 1px 4px rgba(0,0,0,0.5)')
        .style('border-radius', 'none')
        .offset([-12, 0])
        .html(function (d, i, item) {
            console.log(yz[0][i]);
            console.log(yz[1][i]);
            console.log(xz[i]);
            var test_name = xz[i] + ", organisé le";
            var acq_skill = "Nombre de compétence acquise : " + yz[0][i];
            var not_acq_skill = "Nombre de compétence non acquise : " + yz[1][i];
            return test_name + "<br>" + acq_skill + "<br>" + not_acq_skill
        });


    var svg = d3.select("svg#"+username.replace(".","\\."));

    var margin = {top: 40, right: 10, bottom: 30, left: 30},
        width = +svg.attr("width") - margin.left - margin.right,
        height = +svg.attr("height") - margin.top - margin.bottom,
        g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    g.call(tip);

    // Determine the position of the bar in the graph (relative to the width of the graph)
    var x = d3.scaleBand()
        .domain(xz)
        .rangeRound([0, width])
        .padding(0);

    var y = d3.scaleLinear()
        .domain([0, 12])
        .range([height, 0]);

    // Color for the graph. The first color is for the acquired skill (green) and the second for the non-acquired (orange)
    var color = [["acquired","#00a73f"],["not acquired", "#ff8c1a"]];

    var series = g.selectAll(".series")
        .data(y01z)
        .enter().append("g")
        .attr("fill", function (d, i) {
            return color[i][1];
        });

    var rect = series.selectAll("rect")
        .data(function (d) {
            return d;
        })
        .enter().append("rect")
        .attr("x", function (d, i) {
            return x(xz[i]);
        })
        .attr("y", function (d) {
            return y(d[1]);
        })
        .attr("width", x.bandwidth())
        .attr("height", function (d) {
            return y(d[0]) - y(d[1]);
        })
        .on("mouseover", tip.show)
        .on("mouseout", tip.hide);


    /*  Axis and legend */
    g.append("g")
    .attr("class", "axis axis--x")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x)
        .tickSize(0)
        .tickPadding(6));

    g.append("g")
        .attr("class", "axis axis--y")
        .attr("transform", "translate(0,0)")
        .call(d3.axisLeft(y)
            .tickSize(0)
            .tickPadding(0));

    g.append("text")
	    .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.bottom) +")")
	    .style("text-anchor", "middle")
	    .text("Tests");

    g.append("text")
        .attr("transform", "rotate(-90) translate(" + -(height/2)+ ","+ -(margin.left/2)+")")
        .style("text-anchor", "middle")
        .text("Nombre ompétences testée");

    // Title

   g.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .text("Nombre total de compétences acquises et non acquises sur l'UAA");


    var ord = d3.scaleOrdinal()
        .domain(["acquise", "non-acquise"])
        .range([color[0][1], color[1][1]]);

    g.append("g")
      .attr("class", "legendColor")
      .attr("transform", "translate("+ (width - width/3)+ ",20)");

    var colorLegend = d3.legendColor()
        .labelFormat(d3.format("c"))
        .scale(ord);

    g.select(".legendColor")
      .call(colorLegend);

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