var LINECHART = LINECHART || (function(){
    var _args = {}; // private

    return {
        init : function(Args) {
            _args = Args;
            // some other initialising
        },
        graph : function() {
            var xdatax = _args[0];
            var ydatay = _args[1];
            var data = [];
            var i;
            for(i=0; i<name.length; i++){
                data.push({xdata:xdatax[i], ydata:ydatay[i]})
            }

            var svg = d3.select("svg"),
                margin = {top: 20, right: 20, bottom: 30, left: 50},
                width = +svg.attr("width") - margin.left - margin.right,
                height = +svg.attr("height") - margin.top - margin.bottom,
                g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            var parseTime = d3.timeParse("%d-%b-%y");

            var x = d3.scaleTime()
                .rangeRound([0, width]);

            var y = d3.scaleLinear()
                .rangeRound([height, 0]);

            var line = d3.line()
                .x(function(d) { return x(d.xdata); })
                .y(function(d) { return y(d.ydata); });

              x.domain(d3.extent(data, function(d) { return d.xdata; }));
              y.domain(d3.extent(data, function(d) { return d.ydata; }));

              g.append("g")
                  .attr("transform", "translate(0," + height + ")")
                  .call(d3.axisBottom(x))
                .select(".domain")
                  .remove();

              g.append("g")
                  .call(d3.axisLeft(y))
                .append("text")
                  .attr("fill", "#000")
                  .attr("transform", "rotate(-90)")
                  .attr("y", 6)
                  .attr("dy", "0.71em")
                  .attr("text-anchor", "end");

              g.append("path")
                  .datum(data)
                  .attr("fill", "none")
                  .attr("stroke", "steelblue")
                  .attr("stroke-linejoin", "round")
                  .attr("stroke-linecap", "round")
                  .attr("stroke-width", 1.5)
                  .attr("d", line);
                  }
    };
}());




