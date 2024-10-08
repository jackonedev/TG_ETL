import plotly.graph_objects as go
import plotly.subplots as ms


def create_candlestick(df):
    return go.Candlestick(
        x=df.index,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        hoverinfo="x",
    )


def create_scatter(df, column, name, color, hover=False):
    if hover:
        return go.Scatter(
            x=df.index,
            y=df[column],
            name=name,
            line=dict(color=color, width=1),
            hovertemplate="%{y}",
            hoverlabel=dict(font_size=10),
        )
    else:
        return go.Scatter(
            x=df.index,
            y=df[column],
            name=name,
            line=dict(color=color, width=1),
            hoverinfo="x",
        )


def create_bar(df, column, name, color, hover=False):
    if hover:
        return go.Bar(
            x=df.index,
            y=df[column],
            name=name,
            marker_color=color,
            hovertemplate="%{y}",
            hoverlabel=dict(font_size=10),
        )
    else:
        return go.Bar(
            x=df.index,
            y=df[column],
            name=name,
            marker_color=color,
            hoverinfo="x",
        )


def create_SQZMOM_bar(df, normalize=False):

    if normalize:
        df["SQZMOM_value"] = (df["SQZMOM_value"] - df["SQZMOM_value"].min()) / (
            df["SQZMOM_value"].max() - df["SQZMOM_value"].min()
        ) * 100 - 50

    colors = []
    for i in range(len(df)):
        if (
            df["SQZMOM_value"].iloc[i] > 0
            and df["SQZMOM_value"].iloc[i] > df["SQZMOM_value"].iloc[i - 1]
        ):
            colors.append("darkgreen")  # Sección 1: Verde oscuro
        elif (
            df["SQZMOM_value"].iloc[i] > 0
            and df["SQZMOM_value"].iloc[i] < df["SQZMOM_value"].iloc[i - 1]
        ):
            colors.append("indianred")  # Sección 2: Rojo claro
        elif (
            df["SQZMOM_value"].iloc[i] < 0
            and df["SQZMOM_value"].iloc[i] < df["SQZMOM_value"].iloc[i - 1]
        ):
            colors.append("darkred")  # Sección 3: Rojo oscuro
        elif (
            df["SQZMOM_value"].iloc[i] < 0
            and df["SQZMOM_value"].iloc[i] > df["SQZMOM_value"].iloc[i - 1]
        ):
            colors.append("green")  # Sección 4: Verde claro
        else:
            colors.append("gray")
    return go.Bar(
        x=df.index,
        y=df["SQZMOM_value"],
        name="SQZMOM",
        marker_color=colors,
        hoverinfo="x",
    )


def create_price_figure(
    data,
    graph_objects,
    width=1500,
    height=600,
    margin=dict(l=50, r=50, b=50, t=50, pad=4),
    bgcolor="LightSteelBlue",
    title=None,
):
    fig = go.Figure(data=graph_objects)
    fig.layout.xaxis.type = "category"
    fig.layout.xaxis.rangeslider.visible = False
    dist_tick = data.shape[1] // 3
    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=data.index[dist_tick // 2 :: dist_tick],
            ticktext=[
                indice.strftime("%d/%m--%H:%M")
                for indice in data.index[: -dist_tick // 2 : dist_tick]
            ],
        ),
        autosize=False,
        width=width,
        height=height,
        margin=margin,
        paper_bgcolor=bgcolor,
        title=title,
        showlegend=False,  # TODO: considerar meter dentro del layout
    )
    return fig


def create_bar_figure(
    data,
    graph_objects,
    width=1500,
    height=300,
    margin=dict(l=50, r=50, b=1, t=10, pad=4),
    bgcolor="LightSteelBlue",
    title=None,
):
    fig = go.Figure(data=graph_objects)
    fig.layout.xaxis.type = "category"
    fig.layout.xaxis.rangeslider.visible = False
    dist_tick = data.shape[1] // 3
    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=data.index[dist_tick // 2 :: dist_tick],
            ticktext=[
                indice.strftime("%d/%m--%H:%M")
                for indice in data.index[: -dist_tick // 2 : dist_tick]
            ],
        ),
        autosize=False,
        width=width,
        height=height,
        margin=margin,
        paper_bgcolor=bgcolor,
        title=title,
        showlegend=False,
    )
    return fig


def make_2r_subplots(figs: list, title: str):
    "Two rows subplots"
    assert len(figs) == 2, "Two figures are required, figs must be a list of 2 elements"
    kwargs = dict(
        rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02, row_heights=[0.8, 0.2]
    )
    subplot_fig = ms.make_subplots(**kwargs)
    for i, fig in enumerate(figs):
        for trace in fig.data:
            subplot_fig.add_trace(trace, row=i + 1, col=1)
    subplot_fig.update_layout(
        height=900,
        template="seaborn",
        paper_bgcolor="LightSteelBlue",
        title=title,
        hovermode="x",
    )
    # fig.layout.xaxis.type = 'category'
    subplot_fig.layout.xaxis.rangeslider.visible = False
    return subplot_fig


def make_3r_subplots(figs: list, title: str):
    "Three rows subplots"
    assert (
        len(figs) == 3
    ), "Three figures are required, figs must be a list of 3 elements"
    kwargs = dict(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.6, 0.2, 0.2],
    )
    subplot_fig = ms.make_subplots(**kwargs)
    for i, fig in enumerate(figs):
        for trace in fig.data:
            subplot_fig.add_trace(trace, row=i + 1, col=1)
    subplot_fig.update_layout(
        height=1000,
        template="seaborn",
        paper_bgcolor="LightSteelBlue",
        title=title,
        hovermode="x",
    )
    # fig.layout.xaxis.type = 'category'
    subplot_fig.layout.xaxis.rangeslider.visible = False
    return subplot_fig


def download_html(fig, filename):
    with open(filename, "w") as f:
        f.write(fig.to_html())
    print(f"File saved as {filename}")


def add_signals(serie, color) -> list:
    """
    add vertical lines - for DI crosses

    Returns:
        - list of Scatter objects
    """
    y_values = [-10, 10]
    fig_traces = []
    for i in range(len(serie)):
        if serie.iloc[i] == 1:
            x = serie.index[i]
            fig_traces.append(
                go.Scatter(
                    x=[x, x],
                    y=y_values,
                    mode="lines",
                    line=dict(color=color, width=1, dash="dash"),
                    showlegend=False,
                    name=serie.name,
                )
            )
    return fig_traces
