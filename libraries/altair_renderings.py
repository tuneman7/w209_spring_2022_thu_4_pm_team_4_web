from libraries.import_export_data_objects import import_export_data as Import_Export_Data
from libraries.utility import Utility
import numpy as np

import altair as alt
from vega_datasets import data
import os

class AltairRenderings:


    def __init__(self):
        self.my_data_object = Import_Export_Data()

    def get_altaire_line_char_json_county_trade(self,source_country,target_country):

        my_data = self.my_data_object

        title = "Trade between " + source_country + " and " + target_country + " for the years 2014 through 2020"

        source_and_target_data = my_data.get_data_by_source_and_target_country(source_country,target_country)

        base = alt.Chart(source_and_target_data).transform_fold(['Total Trade ($M)','Exports ($M)','Imports ($M)'])

        line = base.mark_line().encode(
            x=alt.X('year:O',axis=alt.Axis(title='Year')),
            y=alt.Y('value:Q',axis=alt.Axis(title='Total Trade In Millions of USD:')),
            color="key:N"
            
        ).properties(
            width=700,
            height=350,
            title=title
            )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('year:O',axis=alt.Axis(title='')),
            y=alt.Y('value:Q',axis=alt.Axis(title='')),
            tooltip=['Total Trade ($M)','Exports ($M)','Imports ($M)']
        ).properties(width=700)

        
        return_chart = alt.layer(line,points)
        return return_chart.to_json()

    def get_altaire_bar_top5_partners(self,source_country):

        my_data = self.my_data_object

        title = "Top 5 Trading Partners by Total Trade Values ($M in USD)"

        source_data = my_data.get_top5data_by_source_country(source_country)

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['year'], name="Year", init={'year': 2020})

        base = alt.Chart(source_data)#.transform_fold(['Total Trade ($M)'])

        bars = base.mark_bar().encode(
            x=alt.X('Total Trade ($M):Q',axis=alt.Axis(title='Total Trade Value ($M in USD)')),
            y=alt.Y('Trading Partner:N',axis=alt.Axis(title='Trading Partner'), sort='-x'),
            tooltip=alt.Tooltip('Total Trade ($M)', format="$,.0f")
        )

        #text = base.mark_text(
        #    align='left',
        #    baseline='middle',
        #    dx=3
        #).encode(
        #    x=alt.X('Total Trade ($M):Q'),
        #    y=alt.Y('Trading Partner:N', sort='-x'),
        #    text=alt.Text('Total Trade ($M):Q', format=',')
        #)


        return_chart = alt.layer(bars).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).properties(
            width=700,
            height=350,
            title=title
        )
        return return_chart.to_json()

    def get_world_map(self):
        source = alt.topo_feature(data.world_110m.url, 'countries')


        my_data = self.my_data_object

        country_source = my_data.get_world_countries_by_iso_label()


        foreground = (
            alt.Chart(source)
            .mark_geoshape(fill='lightgray', stroke="black", strokeWidth=1)
            .encode(
                tooltip=[
                    alt.Tooltip("Country:N", title="Country")
                ],
            )
            .transform_lookup(
                lookup="id",
                from_=alt.LookupData(country_source, "id", ["Country"]),
            )
        )

        my_map = (
            (foreground)
            .configure_view(strokeWidth=0)
            .properties(width=900, height=400)
            .project("mercator", scale=185,center=np.array([24,12]))
        )
        #my_map = alt.concat(my_map,scale=160)
        
        utility = Utility()
        this_dir = utility.get_this_dir()
        file_name = os.path.join(this_dir,"libraries","world.json")
        my_json = utility.get_data_from_file(file_name)
        return my_json,my_map.to_json()

        




