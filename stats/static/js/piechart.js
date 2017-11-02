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
                width = +svg.attr("width"),
                height = +svg.attr("height"),
                radius = Math.min(width, height) / 3,
                g = svg.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

            var color = d3.scaleOrdinal()
                .range(["#1a9850", "#66bd63", "#a6d96a","#d9ef8b","#ffffbf","#fee08b","#fdae61","#f46d43","#d73027"]);

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
                    return d.data.size;
                });

            // add legend

            var legend = d3.select('svg#pie')
                .append("g")
                .selectAll("g")
                .data(color.domain())
                .enter()
                .append('g')
                  .attr('class', 'legend')
                  .attr('transform', function(d, i) {
                    var x = 100;
                    var y = i * 15;
                    return 'translate(' + x + ',' + y + ')';
                });

            legend.append('rect')
                .attr('width', 8)
                .attr('height', 8)
                .attr('x', 0)
                .attr('y', 50)
                .style('fill', color)
                .style('stroke', color);

            legend.append('text')
                .attr('x', 15)
                .attr('y', 58)
                .text(function(d) { return d; });
        }
    };
}());