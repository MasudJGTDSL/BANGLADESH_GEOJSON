import os, django, json, sys
from tqdm import tqdm
from django.conf import settings

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BANGLADESH_GEOJSON.settings")
django.setup()
# ==========
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from geo_locations.models import (
Divisions, Districts, Upazilas, Unions
)

from django.db.models import (
    Case,
    CharField,
    Count,
    DecimalField,
    DurationField,
    ExpressionWrapper,
    F,
    FloatField,
    IntegerField,
    OuterRef,
    Q,
    Subquery,
    Sum,
    Value,
    When,
)
from django.db.models.functions import Cast, Coalesce, Concat, Extract, Round, Trunc


def pie_chart(query_set, label_field, data_field):
    labels = []
    data = []
    queryset = query_set  # gov_status_wise_total
    for item in queryset:
        labels.append(item[label_field])  # 'gov_status'
        data.append(int(item[data_field]))  # 'tota_fdr_amount'
    return {"labels": labels, "data": data}

def chart(table, area_table, title):
    qs_table = table.objects.values("name","geojson")
    areas = area_table.objects.values("feature_id", "area_km2")
    final_data = []
    for item in qs_table:
        for area in areas:
            if item["geojson"]==area["feature_id"]:
                final_data.append({"name":item["name"], "area":area["area_km2"]})
                break
            
    clr = ['steelblue', 'firebrick', 'lightgreen']
    # df_table = pd.DataFrame(final_data, columns=["name","area"])
    # print(df_table)
    
    fig_table = go.Bar(
    x = [item["name"] for item in final_data],
    y = [item["area"] for item in final_data],
    # marker_color= clr,
    # color='area',
    # color_discrete_sequence=['#ef553b', '#636efa', '#00cc96'],
    # textposition='inside', 
    # insidetextanchor='middle',
    # orientation='h',
    text=[f"{x["area"]:,.2f} Km²" for x in final_data],
    textfont=dict(size=10, color='white'),
    textposition='auto',
    name = f'{title} Name',
    )
    title_text = f"{title} Area Information:"
    x_axis_text = f"{title} Name"
    layout = go.Layout(
    title={
            'text': title_text,
            'x': 0.5,
            'xanchor': 'center',
            'y': .85,
            'yanchor': 'top',
            'font':dict(color="#CD7054", size=20),
        },
    xaxis={
        'title': {
            'text': x_axis_text,
            # 'font':dict(color="#CD7054", size=10),
        }
    },
    yaxis={
        'title': {
            'text': 'Area (Km²)'
        }
    },
    # barmode='stack',
    # legend=dict(
    #         title="ABC", orientation="h", y=1.08, yanchor="top", x=0.5, xanchor="center"
    #     ),
        
    )

    chart_figure = go.Figure(data = fig_table, layout = layout)
    chart_table = chart_figure.to_html()
    #! Bar Chart for shareholder deposit and to pay end ================

    return chart_table

"""def dummy_chart():
    labels = ['Dummy: Phase01', 'Dummy: Phase02', 'Dummy: Phase03', 'Dummy: Phase04', 'Dummy: Phase05']
    values = [4000000,1000000,6000000,400000,800000]

    fig_pie_chart = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+value+percent')])
    fig_pie_chart.update_layout(
    title_text="Work Phase Wise Spent Amount",
    # title_font=dict(size=20),
    # legend=dict(x=1, y=0.5),
    # margin=dict(l=20, r=20, t=50, b=20),
    # paper_bgcolor='lightgray',
    # plot_bgcolor='white',
    
    title={"font_size": 20, "xanchor": "auto", "x": 0.5},
    annotations=[dict(text=f'Total: {sum(values)/10**5:,.2f} Lac', x=1.25, y=-.10,font=dict(color="#E04A1C", size=18), showarrow=False)],
    )

    fig_pie_chart=fig_pie_chart.to_html()


    # Shareholders = ['CSE', 'Mech', 'Electronics']
    Shareholders = [
        "Chocolate Platypus",
        "Peach Peacock",
        "Red Bee",
        "Gold Badger",
        "Copper Roadrunner",
        "Tan Emu",
        "Scarlet Heron",
        "Indigo Aardwolf",
        "Ivory Rabbit",
        "Gold Junglefowl",
        "Pink Ocelot",
        "Emerald Guppy",
        "Turquoise Rooster",
        "Cyan Partridge",
        "Blue Skink",
        "Lime Ape",
        "Violet Mule",
        "Lavender Swan",
        "Sapphire Kangaroo",
        "Blush Deer",
    ]
    deposited =  [
        200000,
        250000,
        500000,
        400000,
        350000,
        350000,
        300000,
        300000,
        400000,
        300000,
        250000,
        250000,
        300000,
        500000,
        500000,
        450000,
        450000,
        350000,
        350000,
        250000,
    ]
    to_deposit = [
        300000,
        250000,
        0,
        100000,
        150000,
        150000,
        200000,
        200000,
        100000,
        200000,
        250000,
        250000,
        200000,
        0,
        0,
        50000,
        50000,
        150000,
        150000,
        250000,
    ]
    # print(len(Shareholders), len(deposited), len(to_deposit))
    trace1 = go.Bar(
    x = Shareholders,
    y = deposited,
    text=[f"{x/1000:.0f} k" for x in deposited],
    textfont=dict(size=9, color='white'),
    textposition='auto',
    name = 'Amount Deposited',
    )

    trace2 = go.Bar(
    x = Shareholders,
    y = to_deposit,
    text=[f"{x/1000:.0f} k" for x in to_deposit],
    textfont=dict(size=9, color='white'),
    textposition='auto',
    name = 'Amount to Deposited'
    )

    layout = go.Layout(
    title={
            'text': "Shareholder Deposit Information",
            'x': 0.5,
            'xanchor': 'center',
            'y': .85,
            'yanchor': 'top',
            'font':dict(color="#CD7054", size=20),
        },
    xaxis={
        'title': {
            'text': 'Shareholder',
            # 'font':dict(color="#CD7054", size=10),
        }
    },
    yaxis={
        'title': {
            'text': 'Amount (Taka)'
        }
    },
    barmode='stack',
    legend=dict(
            title=None, orientation="h", y=1.08, yanchor="top", x=0.5, xanchor="center"
        ),
        
    )

    data = [trace1, trace2]
    chart_deposit_target = go.Figure(data = data, layout = layout)
    # chart_deposit_target.update_layout(
    # font_family="Courier New",
    # font_color="blue",
    # title_font_family="Times New Roman",
    # title_font_color="#CD7054",
    # title_font_size="20",
    # legend_title_font_color="green"
    # )   
    chart_deposit_target = chart_deposit_target.to_html()

    return {"fig_pie_chart":fig_pie_chart, 
                "chart_deposit_target":chart_deposit_target}"""
                
#! To run: python geo_locations/chart.py

if __name__ == "__main__":
    chart(Divisions)