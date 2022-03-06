from libraries.import_export_data_objects import import_export_data as Import_Export_Data
from libraries.utility import Utility
import numpy as np

import altair as alt
from vega_datasets import data
import os
import pandas as pd
import pandasql as psql
import math


class AltairRenderings:


    def __init__(self,load_data_from_url=False):
        if load_data_from_url == True:
            self.my_data_object = Import_Export_Data()
        else:
            self.my_data_object = Import_Export_Data(load_data_from_url=load_data_from_url)

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

    def get_altaire_line_chart_county_trade_for_matrix(self,source_country,target_country,width=340,height=200):

        my_data = self.my_data_object

        title = "Trade between " + source_country + " and " + target_country + " 2014 - 2020"

        source_and_target_data = my_data.get_data_by_source_and_target_country(source_country,target_country)

        base = alt.Chart(source_and_target_data).transform_fold(['Total Trade ($M)','Exports ($M)','Imports ($M)'])

        line = base.mark_line().encode(
            x=alt.X('year:O',axis=alt.Axis(title='Year')),
            y=alt.Y('value:Q',axis=alt.Axis(title='Total Trade In Millions of USD:')),
            color="key:N"
            
        ).properties(
            width=width,
            height=height,
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
        ).properties(width=width)

        
        return_chart = alt.layer(line,points)
        return return_chart

    def get_altaire_bar_top5_partners_for_matrix(self,source_country,width=320,height=130):

        my_data = self.my_data_object

        title = source_country + "'s Top 5 Trading Partners"


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
        ).properties(
            title=title,
            width=width,
            height=height
        )
        return return_chart


    def get_altaire_bar_top5_partners(self,source_country):

        my_data = self.my_data_object

        title = source_country + "'s Top 5 Trading Partners by Total Trade Values ($M in USD)"

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



    def get_import_export_balance_top_five(self,source_country,year=None,for_matrix=False,height=200,width=300):

        my_data = self.my_data_object

        title = source_country + "'s Imports, Exports, and Net Trade"
        if source_country.lower() == "world":
            source_country = "world"

        source_data = my_data.get_top_trading_and_net_value(source_country)

        if year is not None:
            sql = "select '$' || printf(\"%,d\",cast(sum(net_trade) as text)) as total_net_trade from source_data where year = '" + str(year) + "'"
            my_result= psql.sqldf(sql)
            total_net_trade=my_result["total_net_trade"][0]
            title += ", Net Trade: "+ total_net_trade +" for Year: " + str(year)
            sql = "select * from source_data where year = '" + str(year) + "'"
            source_data = psql.sqldf(sql)


        # A slider filter
        if year is None:
            year_slider = alt.binding_range(min=2014, max=2020, step=1)
            slider_selection = alt.selection_single(bind=year_slider, fields=['year'], name="Year", init={'year': 2020})

        base = alt.Chart(source_data).transform_fold(
                                                    ["Exports ($M)","Imports ($M)"],
                                                    as_ = ['column','value']
                                                    )

        bars = base.mark_bar(opacity=0.6).encode(
            y=alt.Y('value:Q',axis=alt.Axis(title='Total Trade ($M)')),
            x=alt.X('Trading Partner', sort='-y'),
            tooltip=[alt.Tooltip("Total Trade ($M)",format="$,.0f"),alt.Tooltip("net_trade",format="$,.0f", title="Net Trade"),alt.Tooltip("Exports ($M)",format="$,.0f" ),alt.Tooltip("Imports ($M)",format="$,.0f"),alt.Tooltip("Imports ($M)",format="$,.0f")],
            color='column:N'

        )

        line = bars.mark_line(color='Lime').encode(
            x=alt.X('Trading Partner'),
            y=alt.Y('net_trade:Q',axis=alt.Axis(title='')),
            tooltip=[alt.Tooltip("Total Trade ($M)",format="$,.0f"),alt.Tooltip("net_trade",format="$,.0f", title="Net Trade"),alt.Tooltip("Exports ($M)",format="$,.0f" ),alt.Tooltip("Imports ($M)",format="$,.0f"),alt.Tooltip("Imports ($M)",format="$,.0f")],
            color=alt.value("Lime"),                 
        )


        invisible_dots = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Trading Partner'),
            y=alt.Y('net_trade:Q',axis=alt.Axis(title='')),
            tooltip=[alt.Tooltip("Total Trade ($M)",format="$,.0f"),alt.Tooltip("net_trade",format="$,.0f", title="Net Trade"),alt.Tooltip("Exports ($M)",format="$,.0f" ),alt.Tooltip("Imports ($M)",format="$,.0f"),alt.Tooltip("Imports ($M)",format="$,.0f")]
        )

        visible_dots = base.mark_circle(
            color='Lime',
            opacity=1.0,
            size=60
        ).encode(
            x=alt.X('Trading Partner'),
            y=alt.Y('net_trade:Q',axis=alt.Axis(title=''))
        )

        #am here
        line_text = base.mark_text(
            color="black",
            opacity=1,
            fontSize=13,
            dy=-14
        ).encode(
            x=alt.X('Trading Partner'),
            y=alt.Y('net_trade:Q',axis=alt.Axis(title='')),
            text=alt.Text('net_trade_text')
        )

        if for_matrix==False:
            return  alt.layer(bars + invisible_dots+line+line_text+visible_dots).add_selection(
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
        else:

            return  alt.layer(bars + invisible_dots+line+line_text+visible_dots).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).resolve_scale(
                y = 'independent'
            ).properties(
                width=width,
                height=height,
                title=title
            )


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

    def get_altaire_dual_pie_chart_by_types(self,source_country,target_country, direction):

        my_data = self.my_data_object
        title = source_country + " vs. "+ target_country + " Trade Type Distribution"
        
        df = my_data.imports_exports_by_sectors(source_country, target_country, direction)
        country_data = df.rename(columns={'Product/Sector-reformatted': 'Product_Type'})
        #source_country_data = df[df['Reporting Economy']==source_country].rename(
        #    columns={'Product/Sector-reformatted': 'Product_Type'})
        #target_country_data = df[df['Reporting Economy']==target_country].rename(
        #    columns={'Product/Sector-reformatted': 'Product_Type'})

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['Year'], name="Year", init={'Year': 2020})

        # radio button for export/import option
        #direction = ["exports", "imports"]
        #direction_radio = alt.binding_radio(options=direction)

        #direction_select = alt.selection_single(fields=['Direction'], bind=direction_radio, name="Direction", init = {'Direction': 'exports'})


        base = alt.Chart(country_data).encode(
            theta=alt.Theta(field="Value", type="quantitative"),
            color=alt.Color(field="Product_Type", type="nominal", scale=alt.Scale(scheme='tableau20')),
            tooltip=alt.Tooltip('Product_Type')
        )

        source_pie_chart = base.transform_filter(
            alt.FieldEqualPredicate(field='Reporting Economy', equal=source_country)
        ).mark_arc(outerRadius=120).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).properties(title=source_country)

        #source_pie_chart_direction = source_pie_chart.add_selection(
        #    direction_select
        #).transform_filter(
        #    direction_select
        #)
        base_target = alt.Chart(country_data).encode(
            theta=alt.Theta(field="Value", type="quantitative"),
            color=alt.Color(field="Product_Type", type="nominal"),
            tooltip=alt.Tooltip('Product_Type')
        ).transform_filter(
            alt.FieldEqualPredicate(field='Reporting Economy', equal=target_country)
        )

        target_pie_chart = base.mark_arc(outerRadius=120).transform_filter(
            alt.FieldEqualPredicate(field='Reporting Economy', equal=target_country)
        ).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).properties(title=target_country)

        return_chart = alt.hconcat(source_pie_chart, target_pie_chart)

        return return_chart

    def get_top_20_countries(self):

        return self.my_data_object.get_distinct_country_list()

    def get_world_map(self):

        world_map_source = alt.topo_feature(data.world_110m.url, 'countries')
        
        my_data = self.my_data_object

        country_source = my_data.get_world_countries_by_iso_label()
        country_source.loc[84,'Country'] = 'South Korea'
        country_source = country_source.drop(4)

        top20_2020 = my_data.get_top_20_gdp_data_for_map()
        country_gdp = pd.merge(country_source, top20_2020, on='Country', how = 'outer')
        country_gdp['GDP'] = country_gdp['GDP'].fillna(0)


        foreground = (
            alt.Chart(world_map_source)
            .mark_geoshape(stroke="black", strokeWidth=1)
            .encode(
                color = alt.condition('datum.GDP > 0', 
                                    alt.Color('GDP:Q',legend=alt.Legend(title="County GDP in $MM")),
                                    alt.value('lightgrey')),
                tooltip=[alt.Tooltip("Country:N", title="Country")]
            )
            .transform_lookup(
                lookup="id",
                from_=alt.LookupData(country_gdp, "id", ["Country",'GDP']),
            )
        )

        my_map = (
            (foreground)
            .configure_view(strokeWidth=0)
            .properties(width=900, height=550)
            .project("mercator", scale=185,center=np.array([24,12]))
        )
        #my_map = alt.concat(my_map,scale=160)
        
        utility = Utility()
        this_dir = utility.get_this_dir()
        file_name = os.path.join(this_dir,"libraries","world.json")
        my_json = utility.get_data_from_file(file_name)
        return my_json,my_map


    # def my_new_map(self):
    #     source = alt.topo_feature(data.world_110m.url, 'countries')
    #     my_map=alt.Chart(source).mark_geoshape(
    #     fill='blue',
    #     stroke='grey',).encode(tooltip='id:N').project('naturalEarth1').properties(width=800, height=600).configure_view(stroke=None)

    #     return my_map

    def my_new_map(self):
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        interested_countries = ['Australia','Brazil','Canada','China','France','Germany','India','Indonesia','Iran','Italy','Japan',
                       'Mexico','Netherlands','Russia','Saudi Arabia','South Korea','Spain','Switzerland','United Kingdom','United States of America']
        gdp = list(range(100,300,10))

        country_gdp = pd.DataFrame(
            {'name': interested_countries,
            'GDP': gdp
            })

        world_gdp = pd.merge(world, country_gdp, on='name', how = 'outer')
        world_gdp['GDP'] = world_gdp['GDP'].fillna(0)

        my_map = alt.Chart(world_gdp[world_gdp.continent!='Antarctica']).mark_geoshape(
            ).project(
            ).encode(
                color='GDP',
                tooltip='name' 
            ).properties(
                width=700,
                height=500
            )

        return my_map

    def get_time_series_gdp_chart_for_matrix(self,source_country,width=300,height=200):

        my_data = self.my_data_object

        my_data_to_graph = my_data.get_gdp_data_by_country(source_country)

        title = source_country + "'s GDP"

        source_and_target_data = my_data_to_graph

        base = alt.Chart(source_and_target_data)

        line = base.mark_line().encode(
            x=alt.X('Year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('GDP:Q',axis=alt.Axis(title="GDP $B",labelExpr='"$" + datum.value / 1E9 + "B"'))#,
            #color="Country:N"
            
        ).properties(
            width=width,
            height=height,
            title=title
            )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('GDP:Q',axis=alt.Axis(title='')),
            tooltip=['Country','GDP $B']
        ).properties(width=width)

        
        return_chart = alt.layer(line,points).configure_axis(grid=False)
        return return_chart

    def get_lines_for_top5_countries(self,width=300,height=200):
        #time_s = self.get_altaire_line_chart_county_trade_for_matrix(source_country,"World",width=width,height=height)
        #get_import_export_balance_top_five(source_country,for_matrix=True,width=width,height=height)
        indo = self.get_import_export_balance_top_five("Indonesia",for_matrix=True,width=width,height=height)
        aus = self.get_import_export_balance_top_five("Australia",for_matrix=True,width=width,height=height)
        sk = self.get_import_export_balance_top_five("South Korea",for_matrix=True,width=width,height=height)
        jap = self.get_import_export_balance_top_five("Japan",for_matrix=True,width=width,height=height)

        row_1  = (sk | jap )
        row_3  = (indo | aus )
        my_chart = (row_1 & row_3).configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                )

        return my_chart


    def get_charts_for_click_from_world_map(self,source_country,width=300,height=200):
        top_5  = self.get_altaire_bar_top5_partners_for_matrix(source_country,width=width,height=height)
        trade  = self.get_import_export_balance_top_five(source_country,for_matrix=True,width=width,height=height)
        time_s = self.get_altaire_line_chart_county_trade_for_matrix(source_country,"World",width=width,height=height)
        #gdp = self.get_time_series_gdp_chart_for_matrix(source_country,width=width,height=height)
        gdp = self.get_time_series_gdp_trade_for_matrix(source_country,width=width,height=height)

        row_1 = (time_s | top_5).resolve_scale(
            color='independent')
        row_2 = (trade | gdp).resolve_scale(
            color='independent')


        my_chart = (row_1 & row_2 ).configure_axis(
        grid=False
        ).configure_view(
        strokeWidth=0
        )

        return my_chart

    def get_time_series_gdp_chart(self,source_country):

        my_data = self.my_data_object

        my_data_to_graph = my_data.get_gdp_data_by_country(source_country)

        title = "GDP " + source_country

        source_and_target_data = my_data_to_graph

        base = alt.Chart(source_and_target_data)

        line = base.mark_line().encode(
            x=alt.X('Year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('GDP:Q',axis=alt.Axis(title="GDP $B",labelExpr='"$" + datum.value / 1E9 + "B"'))#,
            #color="Country:N"
            
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
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('GDP:Q',axis=alt.Axis(title='')),
            tooltip=['Country','GDP $B']
        ).properties(width=700)

        
        return_chart = alt.layer(line,points).configure_axis(grid=False)
        return return_chart


    def get_time_series_gdp_compare_chart(self,source_country,target_country):

        my_data = self.my_data_object

        my_data_to_graph = my_data.get_gdp_data_compare(source_country,target_country)

        title = "GDP Growth " + source_country + " and " + target_country + "2014 to 2020"

        source_and_target_data = my_data_to_graph

        base = alt.Chart(source_and_target_data)

        line = base.mark_line().encode(
            x=alt.X('Year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('GDP Pct Growth:Q',axis=alt.Axis(title="GDP Growth %",labelExpr='datum.value + "%"')),
            color="Country:N"
            
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
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('GDP Pct Growth:Q',scale=alt.Scale(domain=(-10, 10)),axis=alt.Axis(title='')),
            tooltip=['Country','GDP Pct Growth %']
        ).properties(width=700)

        
        return_chart = alt.layer(line,points).configure_axis(grid=False)
        return return_chart

    def get_time_series_gdp_chart_for_matrix(self,source_country,width=300,height=150):

        my_data = self.my_data_object

        my_data_to_graph = my_data.get_gdp_data_by_country(source_country)

        title = "GDP " + source_country

        source_and_target_data = my_data_to_graph

        base = alt.Chart(source_and_target_data)

        line = base.mark_line().encode(
            x=alt.X('Year',axis=alt.Axis(title='Year')),
            y=alt.Y('GDP:Q',axis=alt.Axis(title="GDP $B",labelExpr='"$" + datum.value / 1E9 + "B"'))#,
            #color="Country:N"
            
        ).properties(
            width=width,
            height=height,
            title=title
            )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Year',axis=alt.Axis(title='')),
            y=alt.Y('GDP:Q',axis=alt.Axis(title='')),
            tooltip=['Country','GDP $B']
        ).properties(width=width)

        
        return_chart = alt.layer(line,points)
        return return_chart

    def get_time_series_gdp_trade_trend_chart(self,source_country):

        my_data = self.my_data_object

        my_data_to_graph = my_data.get_gdp_data_by_country(source_country)

        title = "GDP & Trade Growth Compare " + source_country

        source_and_target_data = my_data_to_graph

        base = alt.Chart(source_and_target_data).transform_fold(['GDP Pct Growth','Trade Total Change %'])

        line = base.mark_line().encode(
            x=alt.X('Year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('value:Q',axis=alt.Axis(title="GDP and Trade % Change",labelExpr='datum.value + "%"')),
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
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('value:Q',axis=alt.Axis(title='')),
            tooltip=['GDP Growth Pct','Trade Total Change %']
        ).properties(width=700)

        return_chart = alt.layer(line,points).configure_axis(grid=False)
        return return_chart
    
    def get_time_series_gdp_trade_for_matrix(self,source_country,width=300,height=200):

        my_data = self.my_data_object

        my_data_to_graph = my_data.get_gdp_data_by_country(source_country)

        title = "GDP & Trade Growth Compare " + source_country

        source_and_target_data = my_data_to_graph

        base = alt.Chart(source_and_target_data).transform_fold(['GDP Pct Growth','Trade Total Change %'])

        line = base.mark_line().encode(
            x=alt.X('Year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('value:Q',axis=alt.Axis(title="GDP and Trade % Change",labelExpr='datum.value + "%"')),
            color="key:N"
        ).properties(
            width=width,
            height=height,
            title=title
            )

                #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('value:Q',axis=alt.Axis(title='')),
            tooltip=['GDP Growth Pct','Trade Total Change %']
        ).properties(
            width=width)

        return_chart = alt.layer(line,points)
        return return_chart


    def get_charts_for_country_dill_down(self,source_country,target_country,width=300,height=200):
        time_s  = self.get_altaire_line_chart_county_trade_for_matrix(source_country,target_country)
        pie     = self.get_altaire_dual_pie_chart_by_types_for_matrix(source_country,target_country, "exports")
        gdp     = self.get_time_series_gdp_compare_chart_form_matrix(source_country,target_country)

        row_1 = (time_s | pie).resolve_scale(
            color='independent')
        row_2 = (gdp ).resolve_scale(
            color='independent')


        my_chart = (row_1 & row_2 ).configure_axis(
        grid=False
        ).configure_view(
        strokeWidth=0
        ).configure_view(
            stroke=None
        )

        return my_chart

    def get_altaire_dual_pie_chart_by_types_for_matrix(self,source_country,target_country, direction,width=300,height=200):

        my_data = self.my_data_object
        title = source_country + " vs. "+ target_country + " Trade Type Distribution"
        
        df = my_data.imports_exports_by_sectors(source_country, target_country, direction)
        country_data = df.rename(columns={'Product/Sector-reformatted': 'Product_Type'})
        #source_country_data = df[df['Reporting Economy']==source_country].rename(
        #    columns={'Product/Sector-reformatted': 'Product_Type'})
        #target_country_data = df[df['Reporting Economy']==target_country].rename(
        #    columns={'Product/Sector-reformatted': 'Product_Type'})

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['Year'], name="Year", init={'Year': 2020})

        # radio button for export/import option
        #direction = ["exports", "imports"]
        #direction_radio = alt.binding_radio(options=direction)

        #direction_select = alt.selection_single(fields=['Direction'], bind=direction_radio, name="Direction", init = {'Direction': 'exports'})


        base = alt.Chart(country_data).encode(
            theta=alt.Theta(field="Value", type="quantitative"),
            color=alt.Color(field="Product_Type", type="nominal", scale=alt.Scale(scheme='tableau20')),
            tooltip=alt.Tooltip('Product_Type')
        )

        source_pie_chart = base.transform_filter(
            alt.FieldEqualPredicate(field='Reporting Economy', equal=source_country)
        ).mark_arc(outerRadius=(width/4)).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).properties(title=source_country,width=(width/2),height=height)

        base_target = alt.Chart(country_data).encode(
            theta=alt.Theta(field="Value", type="quantitative"),
            color=alt.Color(field="Product_Type", type="nominal"),
            tooltip=alt.Tooltip('Product_Type')
        ).transform_filter(
            alt.FieldEqualPredicate(field='Reporting Economy', equal=target_country)
        )

        target_pie_chart = base.mark_arc(outerRadius=(width/4)).transform_filter(
            alt.FieldEqualPredicate(field='Reporting Economy', equal=target_country)
        ).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).properties(title=target_country,width=(width/2),height=height)

        return_chart = alt.hconcat(source_pie_chart, target_pie_chart)

        return return_chart



    def get_time_series_gdp_compare_chart_form_matrix(self,source_country,target_country,width=300,height=200):

        my_data = self.my_data_object

        my_data_to_graph = my_data.get_gdp_data_compare(source_country,target_country)

        title = "GDP Growth " + source_country + " and " + target_country + " 2014 to 2020"

        source_and_target_data = my_data_to_graph

        base = alt.Chart(source_and_target_data)

        line = base.mark_line().encode(
            x=alt.X('Year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('GDP Pct Growth:Q',axis=alt.Axis(title="GDP Growth %",labelExpr='datum.value + "%"')),
            color="Country:N"
            
        ).properties(
            width=width,
            height=height,
            title=title
            )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('GDP Pct Growth:Q',scale=alt.Scale(domain=(-10, 10)),axis=alt.Axis(title='')),
            tooltip=['Country','GDP Pct Growth %']
        ).properties(width=width)

        
        return_chart = alt.layer(line,points)
        return return_chart


    def get_time_series_gdp_chart_for_matrix(self,source_country,width=300,height=150):

        my_data = self.my_data_object

        my_data_to_graph = my_data.get_gdp_data_by_country(source_country)

        title = "GDP " + source_country

        source_and_target_data = my_data_to_graph

        base = alt.Chart(source_and_target_data)

        line = base.mark_line().encode(
            x=alt.X('Year',axis=alt.Axis(title='Year')),
            y=alt.Y('GDP:Q',axis=alt.Axis(title="GDP $B",labelExpr='"$" + datum.value / 1E9 + "B"'))#,
            #color="Country:N"
            
        ).properties(
            width=width,
            height=height,
            title=title
            )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Year',axis=alt.Axis(title='')),
            y=alt.Y('GDP:Q',axis=alt.Axis(title='')),
            tooltip=['Country','GDP $B']
        ).properties(width=width)

        return_chart = alt.layer(line,points)
        return return_chart

    def get_net_trade_chart(self,source_country):

        my_data = self.my_data_object
        
        title = "" + source_country + "Trade Imports, Exports, Net Trade"
        #title="Trade Imports, Exports, Net Trade"

        df_set=my_data.get_data_by_source_and_target_country(source_country,'China')
        df_set['Exports']=df_set['Exports ($M)']
        df_set['Imports']=df_set['Imports ($M)']*-1
        df_set['Net Exports']=df_set['Net Exports ($M)']
        df_set[df_set['country']==source_country]

        #from altair.vegalite.v4.schema.core import Color
        base = alt.Chart(df_set).transform_fold(['Imports','Exports'])
        base2= alt.Chart(df_set)

        bar = base.mark_bar(size=(35)).encode(
            x=alt.X('year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('value:Q',axis=alt.Axis(title="Trade",labelExpr='"$" + datum.value / 1E3 + "B"')),#,
            #strokeWidth=alt.value(3)
            color=alt.Color("key:N",scale=alt.Scale(scheme='blues'))
        ).properties(
            width=500,
            height=250,
            title=title
            )

        line = base2.mark_line(color='green').encode(
            x=alt.X('year:N'),#,axis=alt.Axis(title='Year')),
            y=alt.Y('Net Exports:Q'),#,axis=alt.Axis(title="Trade")),#,
            strokeWidth=alt.value(3)
            #color=alt.Color()
            #strokeWidth=alt.value(3)
            #color=alt.Color("key:N",scale=alt.Scale(scheme='blues'))
        ).properties(
            width=500,
            height=250
            )

        return_chart=alt.layer(bar,line).configure_axis(grid=False)
        return return_chart
    
    def get_nafta_net_trade_chart(self,source_country):
        #NOT SET-UP YET
        #CAN CHANGE TO NAFTA & EU

        my_data = self.my_data_object
        
        title = "" + source_country + "Trade Imports, Exports, Net Trade"
        #title="Trade Imports, Exports, Net Trade"

        df_set=my_data.get_data_by_source_and_target_country(source_country,'China')
        df_set['Exports']=df_set['Exports ($M)']
        df_set['Imports']=df_set['Imports ($M)']*-1
        df_set['Net Exports']=df_set['Net Exports ($M)']
        df_set[df_set['country']==source_country]

        #from altair.vegalite.v4.schema.core import Color
        base = alt.Chart(df_set).transform_fold(['Imports','Exports'])
        base2= alt.Chart(df_set)

        bar = base.mark_bar(size=(35)).encode(
            x=alt.X('year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('value:Q',axis=alt.Axis(title="Trade",labelExpr='"$" + datum.value / 1E3 + "B"')),#,
            #strokeWidth=alt.value(3)
            color=alt.Color("key:N",scale=alt.Scale(scheme='blues'))
        ).properties(
            width=500,
            height=250,
            title=title
            )

        line = base2.mark_line(color='green').encode(
            x=alt.X('year:N'),#,axis=alt.Axis(title='Year')),
            y=alt.Y('Net Exports:Q'),#,axis=alt.Axis(title="Trade")),#,
            strokeWidth=alt.value(3)
            #color=alt.Color()
            #strokeWidth=alt.value(3)
            #color=alt.Color("key:N",scale=alt.Scale(scheme='blues'))
        ).properties(
            width=500,
            height=250
            )

        return_chart=alt.layer(bar,line).configure_axis(grid=False)
        return return_chart

    def get_altaire_multi_charts_for_China(self,width=1000,height=600):

        my_data = self.my_data_object
        title = "Percentage of Total Trades Done with China"
        
        df = my_data.get_Chinadata_by_country()
        df = df.rename(columns={'TradePctGDPChange': 'Trade/GDP ratio change'})
        # GDP growth correlation
        china_gdp_df = df[df['Country'] == 'China'][['Country', 'GDP Growth Pct']].reset_index(drop = True)
        other_gdp_df = df[df['Country'] != 'China'][['Country', 'GDP Growth Pct']]
        other_gdp_df = other_gdp_df.drop_duplicates().reset_index(drop = True)
        country_list = df[df['Country'] !='China']['Country'].unique()
        num_country_per_line = math.ceil(len(country_list)/3.0)
        
        gdp_correl = {}
        for country in country_list:
            gdp_correl[country] = china_gdp_df['GDP Growth Pct'].corr(
                other_gdp_df[other_gdp_df['Country']==country]['GDP Growth Pct'].reset_index(drop = True))
        gdp_correl_df = pd.DataFrame(gdp_correl.items(), columns=['Country', 'GDPcorrel_w_China'])
        
        df = df.merge(gdp_correl_df, on = 'Country', how = 'left')
        # Slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['Year'], name="Year", init={'Year': 2020})

        # Pie charts
        base = alt.Chart(df).encode(
            theta=alt.Theta(field="total_trade", type="quantitative"),
            color=alt.Color(field="isChinaPartner", type="nominal",
                            scale = alt.Scale(domain = ['Trades with China', 'GDP Growth Pct', 
                                                        'Trades with Others', 'Trade/GDP ratio change'],
                                              range = ['#2f6684', '#ff7c43', '#acc8df', '#665191']),
                            legend = alt.Legend(title="Key")),
            
            tooltip=alt.Tooltip('total_trade', format="$,.0f")
        )

        chart1 = alt.hconcat()
        for country in country_list[0:num_country_per_line]: 
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+10), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )
            chart1 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10))
        
        chart2 = alt.hconcat()
        for country in country_list[num_country_per_line:num_country_per_line*2]:
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+10), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )
            chart2 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10))

        chart3 = alt.hconcat()
        for country in country_list[num_country_per_line*2:]:
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+10), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )

            chart3 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10))
        
        # brush selection
        brush_selection = alt.selection_single(fields=['Country'], empty='none')

        # line charts
        dependency_bars = alt.Chart(df).mark_bar(opacity = 0.9, color = '#2f6684', size = 30).encode(
            x = alt.Y('Country:N', sort='-y',
                      axis=alt.Axis(labelAngle=-30, 
                                    labelOverlap=False,
                                    labelFontSize=12,
                                    labelFontWeight = 'bold')),
            y = 'PercentOfTotal:Q'
        ).transform_calculate(
            PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
        )
        dependency_text = dependency_bars.mark_text(dy = -10).encode(
            x = alt.Y('Country:N', sort='-y', axis = None),
            y = 'PercentOfTotal:Q',
            text=alt.Text("PercentOfTotal:Q", format='.1%')
        )

        dependency_chart = alt.layer(dependency_bars, dependency_text).transform_filter(
            alt.FieldEqualPredicate(field='Year', equal=2020)
        ).transform_filter(
            alt.FieldEqualPredicate(field='isChinaPartner', equal='Trades with China')
        ).resolve_scale(
            x = 'independent'
        ).add_selection(
            brush_selection
        ).properties(
            title="Click a country to see how its economy growth is associated to its trade growth",
            width=(width*0.75),height=(height/10+50)
        )

        # Correlation fact 
        corr_text = alt.Chart(df).mark_text(size = 40).encode(
            text=alt.Text("GDPcorrel_w_China:Q", format='.1%')
        ).transform_filter(
            brush_selection
        ).transform_filter(
            alt.FieldEqualPredicate(field='Year', equal=2020)
        ).properties(
            title="GDP Growth Correlation with China",
            width=(width*0.25),height=(height/10+50)
        )

        # ruler selection
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['Year'], empty='none')

        gdp_base = alt.Chart(df).transform_fold(
            ['Trade/GDP ratio change', 'GDP Growth Pct']
        )

        gdp_line = gdp_base.mark_line().encode(
            x = alt.X('Year:O',axis=alt.Axis(labelAngle=0)),
            y = alt.Y('value:Q',axis=alt.Axis(title = 'YoY Growth %', format='.1f')),
            color = 'key:N',
            tooltip=[alt.Tooltip('Year'),
                     alt.Tooltip('Trade/GDP ratio change', format=".2f"),
                     alt.Tooltip('GDP Growth Pct', format=".2f")]
        ).transform_filter(
            brush_selection
        )

        selectors = gdp_base.mark_point().encode(
            x=alt.X('Year:O',axis=alt.Axis(labelAngle=0)),
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )

        #points = gdp_line.mark_point().encode(
        #    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        #)

        points = gdp_line.mark_point(
            opacity=0.0,
            size=3000
        ).encode(
            x=alt.X('year:O',axis=None),
            y=alt.Y('value:Q',axis=None),
            tooltip=[alt.Tooltip('year'),
                     alt.Tooltip('Trade/GDP ratio change', format=".2f"),
                     alt.Tooltip('GDP Growth Pct', format=".2f")]
        )

        # Draw text labels near the points, and highlight based on selection
        #text = gdp_line.mark_text(align='left', dx=5, dy=-5).encode(
        #    text=alt.condition(nearest, 'value:Q', alt.value(' '))
        #)
        #text = gdp_base.mark_text(align='center', dx=5, dy=-5).encode(
        #    x=alt.X('year:O',axis=None),
        #    y=alt.Y('value:Q',axis=None),
        #    text=alt.Text('value:Q', format='.1f'),
        #    color = 'key:N'
        #).transform_filter(
        #    brush_selection
        #)

        # Draw a rule at the location of the selection
        rules = gdp_base.mark_rule(color='gray').encode(
            x='Year:Q',
        ).transform_filter(
            nearest
        )

        gdp_combine = alt.layer(
            gdp_line#, text #points, selectors,rules,
        ).properties(
            title="GDP and Trade/GDP ratio YoY Growth Percentage" ,width=width,height=(height*3/5-50)
        )

        return_chart = (chart1 & chart2 & chart3 & (dependency_chart | corr_text) & gdp_combine).configure_title(
            baseline="line-top",
            dy = -5
        )
        ## https://stackoverflow.com/questions/67997825/python-altair-generate-a-table-on-selection
        ## https://altair-viz.github.io/user_guide/transform/filter.html?highlight=filter
        ## https://vega.github.io/vega/docs/schemes/
        return return_chart

    def get_asian_trading_partners(self):

        

        indo = self.get_altaire_bar_top5_partners_for_matrix("Indonesia")
        aus = self.get_altaire_bar_top5_partners_for_matrix("Australia")
        sk = self.get_altaire_bar_top5_partners_for_matrix("South Korea")
        jap = self.get_altaire_bar_top5_partners_for_matrix("Japan")

        row_1  = (sk | jap )
        row_3  = (indo | aus )
        my_chart = (row_1 & row_3).configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                )

        return my_chart

    def get_iran_trade_deal_line_charts(self,width=340,height=200):

        sk = self.get_altaire_line_chart_county_trade_for_matrix("Iran","South Korea",width=width,height=height)
        spain = self.get_altaire_line_chart_county_trade_for_matrix("Iran","Spain",width=width,height=height)
        usa = self.get_altaire_line_chart_county_trade_for_matrix("Iran","United States",width=width,height=height)
        jap = self.get_altaire_line_chart_county_trade_for_matrix("Iran","United Kingdom",width=width,height=height)


        row_1 = (sk | spain )
        row_2  = (usa | jap )
        my_chart = (row_1 & row_2).configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                )

        return my_chart

    #am here
    def get_third_page_jcpoa_charts(self,width=340,height=200):
        top_five_partners = self.get_altaire_bar_top5_partners_for_matrix("Iran",width=width,height=height)
        gdp = self.get_time_series_gdp_trade_for_matrix("Iran",width=width,height=height)
        trade  = self.get_import_export_balance_top_five("Iran",for_matrix=True,width=width,height=height)


        row_1 = (top_five_partners | trade )
        row_2  = (gdp)
        my_chart = (row_1 & row_2).configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                )

        return my_chart


