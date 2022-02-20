from libraries.import_export_data_objects import import_export_data as Import_Export_Data
from libraries.utility import Utility
import numpy as np

import altair as alt
from vega_datasets import data
import os
import pandas as pd

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
        return return_chart

    def get_altaire_line_chart_county_trade_for_matrix(self,source_country,target_country):

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
        return return_chart

    def get_altaire_bar_top5_partners_for_matrix(self,source_country):

        my_data = self.my_data_object

        title = "Top 5 Trading Partners by Total Trade Values ($M in USD)"

        source_data = my_data.get_top5data_by_source_country(source_country)

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['year'], name="Year", init={'year': 2020})

        base = alt.Chart(source_data)

        bars = base.mark_bar(color = '#aec7e8').encode(
            x=alt.X('Total Trade ($M):Q',axis=alt.Axis(title='Total Trade Value ($M in USD)')),
            y=alt.Y('Trading Partner:N',axis=alt.Axis(title='Trading Partner'), sort='-x'),
            tooltip=alt.Tooltip('Total Trade ($M)', format="$,.0f")
        )

        text = base.mark_text(align='left', dx=5, dy=-5).encode(
            x=alt.X('Total Trade ($M):Q'),
            y=alt.Y('Trading Partner:N', sort='-x',axis=None),
            text=alt.Text('Total Trade ($M):Q', format='$,.0f')
        )

        return_chart = alt.layer(bars, text).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).resolve_scale(
            y = 'independent'
        ).configure_axis(
            grid=False
        ).configure_view(
            strokeWidth=0
        ).properties(
            width=700,
            height=350,
            title=title
        )
        return return_chart


    def get_altaire_bar_top5_partners(self,source_country):

        my_data = self.my_data_object

        title = "Top 5 Trading Partners by Total Trade Values ($M in USD)"

        source_data = my_data.get_top5data_by_source_country(source_country)

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['year'], name="Year", init={'year': 2020})

        base = alt.Chart(source_data)

        bars = base.mark_bar(color = '#aec7e8').encode(
            x=alt.X('Total Trade ($M):Q',axis=alt.Axis(title='Total Trade Value ($M in USD)')),
            y=alt.Y('Trading Partner:N',axis=alt.Axis(title='Trading Partner'), sort='-x'),
            tooltip=alt.Tooltip('Total Trade ($M)', format="$,.0f")
        )

        text = base.mark_text(align='left', dx=5, dy=-5).encode(
            x=alt.X('Total Trade ($M):Q'),
            y=alt.Y('Trading Partner:N', sort='-x',axis=None),
            text=alt.Text('Total Trade ($M):Q', format='$,.0f')
        )

        return_chart = alt.layer(bars, text).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).resolve_scale(
            y = 'independent'
        ).configure_axis(
            grid=False
        ).configure_view(
            strokeWidth=0
        ).properties(
            width=700,
            height=350,
            title=title
        )
        return return_chart


    def get_altaire_bar_top5_partners(self,source_country):

        my_data = self.my_data_object

        title = "Top 5 Trading Partners by Total Trade Values ($M in USD)"

        source_data = my_data.get_top5data_by_source_country(source_country)

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['year'], name="Year", init={'year': 2020})

        base = alt.Chart(source_data)

        bars = base.mark_bar(color = '#aec7e8').encode(
            x=alt.X('Total Trade ($M):Q',axis=alt.Axis(title='Total Trade Value ($M in USD)')),
            y=alt.Y('Trading Partner:N',axis=alt.Axis(title='Trading Partner'), sort='-x'),
            tooltip=alt.Tooltip('Total Trade ($M)', format="$,.0f")
        )

        text = base.mark_text(align='left', dx=5, dy=-5).encode(
            x=alt.X('Total Trade ($M):Q'),
            y=alt.Y('Trading Partner:N', sort='-x',axis=None),
            text=alt.Text('Total Trade ($M):Q', format='$,.0f')
        )

        return_chart = alt.layer(bars, text).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).resolve_scale(
            y = 'independent'
        ).configure_axis(
            grid=False
        ).configure_view(
            strokeWidth=0
        ).properties(
            width=700,
            height=350,
            title=title
        )
        return return_chart

    def get_import_export_balance_top_five(self,source_country):

        my_data = self.my_data_object

        title = "Top 5 Trading Partners by Total Trade Values ($M in USD)"

        source_data = my_data.get_top_trading_and_net_value(source_country)

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['year'], name="Year", init={'year': 2020})

        base = alt.Chart(source_data).transform_fold(
                                                    ["Exports ($M)","Imports ($M)"],
                                                    as_ = ['column','value']
                                                    )

        bars = base.mark_bar().encode(
            x=alt.X('Trading Partner'),
            y=alt.Y('value:Q',axis=alt.Axis(title='Total Trade ($M)')),
            tooltip=[alt.Tooltip("Total Trade ($M)",format="$,.0f"),alt.Tooltip("net_trade",format="$,.0f", title="Net Trade"),alt.Tooltip("Exports ($M)",format="$,.0f" ),alt.Tooltip("Imports ($M)",format="$,.0f"),alt.Tooltip("Imports ($M)",format="$,.0f")],
            color='column:N'

        )

        line = bars.mark_line(color='green').encode(
            x=alt.X('Trading Partner'),
            y=alt.Y('net_trade:Q',axis=alt.Axis(title='Total Trade In Millions of USD:')),
            tooltip=[alt.Tooltip("Total Trade ($M)",format="$,.0f"),alt.Tooltip("net_trade",format="$,.0f", title="Net Trade"),alt.Tooltip("Exports ($M)",format="$,.0f" ),alt.Tooltip("Imports ($M)",format="$,.0f"),alt.Tooltip("Imports ($M)",format="$,.0f")],
            color=alt.value("Green")
            
        )


        invisible_dots = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Trading Partner'),
            y=alt.Y('net_trade:Q',axis=alt.Axis(title='Total Trade In Millions of USD:')),
            tooltip=[alt.Tooltip("Total Trade ($M)",format="$,.0f"),alt.Tooltip("net_trade",format="$,.0f", title="Net Trade"),alt.Tooltip("Exports ($M)",format="$,.0f" ),alt.Tooltip("Imports ($M)",format="$,.0f"),alt.Tooltip("Imports ($M)",format="$,.0f")]
        )


        return_chart = alt.layer(bars + invisible_dots+line).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).resolve_scale(
            y = 'independent'
        ).configure_axis(
            grid=False
        ).configure_view(
            strokeWidth=0
        ).properties(
            width=700,
            height=350,
            title=title
        )
        return return_chart



    def get_altaire_dual_axis_bar_top5(self,source_country):

        my_data = self.my_data_object

        title = "Top 5 Trading Product Types by Values ($M in USD)"

        exports_data = my_data.get_top5data_by_imports_exports(source_country, 'exports')
        exports_data['Value'] = exports_data['Value'] * -1.0
        exports_data = exports_data.rename(columns={'Value': 'Export_Value', 'Product/Sector-reformatted': 'Export_Product'})
        imports_data = my_data.get_top5data_by_imports_exports(source_country, 'imports')
        imports_data = imports_data.rename(columns={'Value': 'Import_Value', 'Product/Sector-reformatted': 'Import_Product'})
        df = pd.merge(exports_data, imports_data, 
                      how = 'inner', on = ['rnk', 'Year'], 
                     left_index = False, right_index = False)
        domain_x = max(max(abs(df['Export_Value'])), max(df['Import_Value']))
        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['Year'], name="Year", init={'Year': 2020})

        base = alt.Chart(df).encode(x='Export_Value:Q')

        export_bars = base.mark_bar(color = '#aec7e8').encode(
            x=alt.X('Export_Value:Q',axis=alt.Axis(title='Trade Value ($M in USD)'), scale=alt.Scale(domain=[-domain_x,domain_x])),
            y=alt.Y('Export_Product:N',axis=alt.Axis(title='Export Product'), sort='x'),
            tooltip=alt.Tooltip('Export_Value', format="$,.0f")
        )
        import_bars = base.mark_bar(color = '#e7969c').encode( 
            x=alt.X('Import_Value:Q',axis=alt.Axis(title='Trade Value ($M in USD)'), scale=alt.Scale(domain=[-domain_x,domain_x])),
            y=alt.Y('Import_Product:N',axis=alt.Axis(title='Import Product'), sort='-x'),
            tooltip=alt.Tooltip('Import_Value', format="$,.0f")
        )

        text_import = base.mark_text(align='left', dx=5, dy=-5).encode(
            x=alt.X('Import_Value:Q'),
            y=alt.Y('Import_Product:N', sort='-x', axis=None),
            text=alt.Text('Import_Value:Q', format='$,.0f')
        )
        text_export = base.mark_text(align='right', dx=-5, dy=-5).encode(
            x=alt.X('Export_Value:Q'),
            y=alt.Y('Export_Product:N', sort='x', axis=None),
            text=alt.Text('Export_Value:Q', format='$,.0f')
        )

        return_chart = alt.layer(export_bars, import_bars, text_export, text_import).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).resolve_scale(
            y = 'independent'
        ).configure_axis(
            grid=False
        ).configure_view(
            strokeWidth=0
        ).properties(
            width=700,
            height=350,
            title=title
        )
        return return_chart

    def get_top_20_countries(self):

        return self.my_data_object.get_distinct_country_list()

    def get_world_map(self):

        world_map_source = alt.topo_feature(data.world_110m.url, 'countries')


        my_data = self.my_data_object

        country_source = my_data.get_world_countries_by_iso_label()


        foreground = (
            alt.Chart(world_map_source)
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
        return my_json,my_map


    def my_new_map(self):
        source = alt.topo_feature(data.world_110m.url, 'countries')
        my_map=alt.Chart(source).mark_geoshape(
        fill='blue',
        stroke='grey',).encode(tooltip='id:N').project('naturalEarth1').properties(width=800, height=600).configure_view(stroke=None)

        return my_map

        




