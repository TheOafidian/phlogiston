import math
import plotly.graph_objects as go

DISTANCE_CORR = 1200


def get_edges(graph):

    edge_x = []
    edge_y = []

    for edge in graph.edges():
        x0, y0 = graph.nodes[edge[0]]["pos"]
        x1, y1 = graph.nodes[edge[1]]["pos"]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    return edge_x, edge_y


def get_nodes(graph):
    node_x = []
    node_y = []
    for node in graph.nodes():
        x, y = graph.nodes[node]["pos"]
        node_x.append(x)
        node_y.append(y)
    return node_x, node_y


def get_mid_nodes(graph, dcor):

    mnode_x, mnode_y, mnode_txt = [], [], []
    edge_x, edge_y = [], []
    for idx0, idx1 in graph.edges():
        x0, y0 = graph.nodes[idx0]["pos"]
        x1, y1 = graph.nodes[idx1]["pos"]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

        mnode_x.extend([(x0 + x1) / 2])  # assuming values positive/get midpoint
        mnode_y.extend([(y0 + y1) / 2])  # assumes positive vals/get midpoint
        distance = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        mnode_txt.extend([f"{round(dcor*DISTANCE_CORR*distance**2)} hours"])  # hovertext

    return mnode_x, mnode_y, mnode_txt


def plot_graph(g, sphere_names, map_name="", distance_corr=1):

    edges_x, edges_y = get_edges(g)
    nodes_x, nodes_y = get_nodes(g)
    mnodes_x, mnodes_y, mnode_text = get_mid_nodes(g, distance_corr)

    edge_trace = go.Scatter(
        x=edges_x,
        y=edges_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    mnode_trace = go.Scatter(
        x=mnodes_x,
        y=mnodes_y,
        mode="markers",
        showlegend=False,
        hovertemplate="%{hovertext}<extra></extra>",
        hovertext=mnode_text,
        marker=go.scatter.Marker(opacity=0),
    )

    node_trace = go.Scatter(
        x=nodes_x,
        y=nodes_y,
        mode="markers",
        hoverinfo="text",
        marker=dict(
            showscale=True,
            colorscale="Picnic",
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title="Connected routes",
                xanchor="left",
                titleside="right",
            ),
            line_width=2,
        ),
    )

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(g.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append("# of connections: " + str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_text = ["P" + str(t) for t in range(len(node_text))]
    node_text = [sphere_names[t] if t in sphere_names else t for t in node_text]
    node_trace.text = node_text

    # highlight_trace = go.Scatter(
    #     x=[0.78, 0.78, 0.9, 0.89, 0.85],
    #     y=[0.15, 0.32, 0.32, 0.2, 0.08],
    #     fill="toself",
    #     hoverinfo="none",
    # )

    fig = go.Figure(
        data=[edge_trace, node_trace, mnode_trace],
        layout=go.Layout(
            title="Starchart<br>The Known Universe",
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            # annotations=[
            #     dict(
            #         text="Only known locations are displayed on this map, the cartographer is not responsible for any missed planes.",
            #         showarrow=False,
            #         xref="paper",
            #         yref="paper",
            #         x=0.005,
            #         y=-0.002,
            #     )
            # ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )

    fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font_family="Courier New",
        font_color="white",
        # title_font_family="Times New Roman",
        # title_font_color="red",
    )

    return fig
