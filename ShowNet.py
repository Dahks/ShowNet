import uuid
import json

import igraph as ig
from IPython.display import display, HTML

def draw_graph(
	graph: ig.Graph,
	layout: str = 'sugiyama'
):
    """
    @param graph: An Igraph Graph.

    @returns: nothing but plots the graph using IPython's display() function
    """

    # Get Graph attributes required for drawing
    pointPositions = ', '.join([f"{t[0]}, {t[1]}" for t in graph.layout(layout)])
    links = ', '.join([f"{e[0]}, {e[1]}" for e in graph.get_edgelist()])

    # Define config outside the HTML
    # TODO make configurable with input parameters
    config = json.dumps({
        "spaceSize": 4096,
        "backgroundColor": '#2d313a',
        "pointDefaultColor": '#F069B4',
        "scalePointsOnZoom": True,
        "simulationFriction": 0.0, # Make stuff move
        "simulationGravity": 0,
        "simulationRepulsion": 0.5,
        "curvedLinks": True,
        "fitViewDelay": 500,
        "fitViewPadding": 0.3,
        "rescalePositions": True,
        "enableDrag": True,
        "attribution": 'Cosmograph'
    })

    # Like key, required to reference div in this specific cell's output (might otherwise reference other cell's output)
    unique_id = "graph_" + str(uuid.uuid4()).replace("-", "")

    cosmo_html = """
    <div id="{unique_id}" style="height: 500px; width: 100%; background: #2d313a;"></div>

    <script type="module">
      // Use CDN for imports
      import {{ Graph }} from 'https://esm.sh/@cosmos.gl/graph';

      const container = document.getElementById('{unique_id}');
      const config = {config_json};
      const graph = new Graph(container, config);

      // Points: [x, y, x, y...]
      const pointPositions = new Float32Array([{pointPositions}]);
      graph.setPointPositions(pointPositions);

      // Links: [source, target, source, target...]
      const links = new Float32Array([{links}]);
      graph.setLinks(links);

      graph.render();
    </script>
    """.format(
      unique_id=unique_id,
      config_json=config,
      pointPositions=pointPositions,
      links=links
    )

    display(HTML(cosmo_html))