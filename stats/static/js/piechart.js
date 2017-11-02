var PIECHART = PIECHART || (function () {
    var _args = {}; // private

    return {
        init: function (Args) {
            _args = Args;
            // some other initialising
        },
        graph: function () {
            var name = _args[0];
            var size = _args[1];
            var data = [];
            var i;
            for (i = 0; i < name.length; i++) {
                data.push({text: name[i], size: size[i]})
            }

            var svg = d3.select("svg#pie"),
                margin = {top: 100, right: 30, bottom: 30, left: 30},
                width = +svg.attr("width") - margin.left - margin.right,
                height = +svg.attr("height") - margin.top - margin.bottom,
                radius = Math.min(width, height) / 2,
                nml = -margin.left,
                nmt = -margin.top,
                g = svg.append("g").attr("transform", "translate(" + (width+margin.left) / 2 + "," + (height+margin.top) / 2 + ")")

            svg.append("text")
                .attr("x", margin.left + (width / 2))
                .attr("y", (margin.top / 2))
                .attr("text-anchor", "middle")
                .style("font-size", "16px")
                .style("text-decoration", "underline")
                .text("My Wonderful Title");


            var color = d3.scaleOrdinal(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

            var pie = d3.pie()
                .sort(null)
                .value(function (d) {
                    return d.size;
                });

            var path = d3.arc()
                .outerRadius(radius - 10)
                .innerRadius(0);

            var label = d3.arc()
                .outerRadius(radius - 40)
                .innerRadius(radius - 40);

            var arc = g.selectAll(".arc")
                .data(pie(data))
                .enter().append("g")
                .attr("class", "arc");

            arc.append("path")
                .attr("d", path)
                .attr("fill", function (d) {
                    return color(d.data.text);
                });

            arc.append("text")
                .attr("transform", function (d) {
                    return "translate(" + label.centroid(d) + ")";
                })
                .attr("dy", "0.35em")
                .text(function (d) {
                    return d.data.text;
                });
        }
    };
}());