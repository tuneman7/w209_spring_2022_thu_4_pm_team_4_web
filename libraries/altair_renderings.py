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

    def get_world_map(self):
        source = alt.topo_feature(data.world_110m.url, 'countries')


        my_data = self.my_data_object

        country_source = my_data.get_world_countries_by_iso_label()


        foreground = (
            alt.Chart(source)
            .mark_geoshape(stroke="black", strokeWidth=1)
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

        




