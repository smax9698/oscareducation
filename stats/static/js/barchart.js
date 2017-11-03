var BARCHART = BARCHART || (function () {
    var _args = {}; // private

    return {
        init: function (Args) {
            _args = Args;
            // some other initialising
        },
        graph: function () {
            var xdata = _args[0];
            var ydata = _args[1];
            var xtitle = _args[2];
            var ytitle = _args[3];
            var title = _args[4];
            var data = [];
            var i;
            for (i = 0; i < xdata.length; i++) {
                data.push({letter: xdata[i], frequency: ydata[i]})
            }

            var formatCount = d3.format(",.0f");

            var svg = d3.select("svg#bar"),
                margin = {top: 50, right: 30, bottom: 30, left: 50},
                width = +svg.attr("width") - margin.left - margin.right,
                height = +svg.attr("height") - margin.top - margin.bottom,
                g = svg.append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

            svg.append("text")
                .attr("x", margin.left + (width / 2))
                .attr("y", (margin.top / 2))
                .attr("text-anchor", "middle")
                .style("font-size", "16px")
                .style("text-decoration", "underline")
                .text(title);

            var x = d3.scaleBand().rangeRound([0, width]).padding(0.1),
                y = d3.scaleLinear().rangeRound([height, 0]);

            var g = svg.append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


              x.domain(data.map(function(d) { return d.letter; }));
              y.domain([0, d3.max(data, function(d) { return d.frequency; })]);

              g.append("g")
                  .attr("class", "axis axis--x")
                  .attr("transform", "translate(0," + height + ")")
                  .call(d3.axisBottom(x))
                  .append("text")
                  .attr("fill", "#000")
                  .attr("x", width/2)
                  .attr("dx", "0.71em")
                  .attr("y", 30)
                  .text(xtitle);

              g.append("g")
                  .attr("class", "axis axis--y")
                  .call(d3.axisLeft(y))
                  .append("text")
                  .attr("fill", "#000")
                  .attr("transform", "rotate(-90)")
                  .attr("y", -40)
                  .attr("x", -height/2)
                  .attr("dy", "0.71em")
                  .text(ytitle);

              var bar = g.selectAll(".bar")
                        .data(data)
                        .enter().append("rect")
                          .attr("class", "bar")
                          .attr("x", function(d) { return x(d.letter); })
                          .attr("y", function(d) { return y(d.frequency); })
                          .attr("width", x.bandwidth())
                          .attr("height", function(d) { return height - y(d.frequency); });

              bar.append("text")
                .text(function(d){return d;})

/*
            var formatCount = d3.format(",.0f");

            var svg = d3.select("svg#bar"),
                margin = {top: 50, right: 30, bottom: 30, left: 50},
                width = +svg.attr("width") - margin.left - margin.right,
                height = +svg.attr("height") - margin.top - margin.bottom,
                g = svg.append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")


            svg.append("text")
                .attr("x", margin.left + (width / 2))
                .attr("y", (margin.top / 2))
                .attr("text-anchor", "middle")
                .style("font-size", "16px")
                .style("text-decoration", "underline")
                .text("My Wonderful Title");

            var x = d3.scaleLinear()
                .rangeRound([0, width]);

            var bins = d3.histogram()
                .domain(x.domain())
                .thresholds(x.ticks(20))
                (data);

            var y = d3.scaleLinear()
                .domain([0, d3.max(bins, function (d) {
                    return d.length;
                })])
                .range([height, 0]);

            var bar = g.selectAll(".bar")
                .data(bins)
                .enter().append("g")
                .attr("class", "bar")
                .attr("transform", function (d) {
                    return "translate(" + (x(d.x0)-10) + "," + y(d.length) + ")";
                });

            bar.append("rect")
                .attr("x", 1)
                .attr("width", x(bins[0].x1) - x(bins[0].x0) - 1)
                .attr("height", function (d) {
                    return height - y(d.length);
                });

            bar.append("text")
                .attr("dy", ".75em")
                .attr("y", 6)
                .attr("x", (x(bins[0].x1) - x(bins[0].x0)) / 2)
                .attr("text-anchor", "middle")
                .text(function (d) {
                    return formatCount(d.length);
                });

            g.append("g")
                .attr("class", "axis axis--x")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x))
                .append("text")
                .attr("fill", "#000")
                .attr("x", width/2)
                .attr("dx", "0.71em")
                .attr("y", 30)
                .text("X-axis");

            g.append("g")
                .call(d3.axisLeft(y))
                .append("text")
                .attr("fill", "#000")
                .attr("transform", "rotate(-90)")
                .attr("y", -40)
                .attr("x", -height/2)
                .attr("dy", "0.71em")
                .text("Y-axis");*/


        }
    };
}());




