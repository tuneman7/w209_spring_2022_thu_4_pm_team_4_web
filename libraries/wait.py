    def get_nafta_section_1a(self,width=950,height=600):

        my_data = self.my_data_object

        title = "Percentage of Total Trades Done with NAFTA"

        df = my_data.get_nafta_by_country()
        df = df.rename(columns={'TradePctGDPChange': 'Trade/GDP ratio change'})
        # GDP growth correlation
        china_gdp_df = df[df['Country'] == 'China'][['Country', 'GDP Growth Pct']].reset_index(drop = True)
        other_gdp_df = df[df['Country'] != 'China'][['Country', 'GDP Growth Pct']]
        other_gdp_df = other_gdp_df.drop_duplicates().reset_index(drop = True)
        country_list = df[df['Country'] !='China']['Country'].unique()
        #country_list = df[df['Country'] !='China']['Country'].unique()

        country_list = [ 'Japan','South Korea', 'Brazil','India',  'Switzerland', 'Indonesia', 'United Kingdom','Australia'
                        ,'Saudi Arabia', 'Italy', 'Netherlands', 'Russia',
                        'Germany',  'France',  'Spain','Iran']

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
                            scale = alt.Scale(domain = ['Trades with NAFTA', 'GDP Growth Pct', 
                                                        'Trades with Others', 'Trade/GDP ratio change'],
                                            range = ['#156296', '#799D5E', '#B9CDDB', '#E4AB65']),
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
            ).mark_text(radius=(width/30+15), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )
            chart1 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10+40))

        chart2 = alt.hconcat()
        for country in country_list[num_country_per_line:num_country_per_line*2]:
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+15), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )
            chart2 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10+40))

        chart3 = alt.hconcat()
        for country in country_list[num_country_per_line*2:]:
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+15), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )

            chart3 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10+40))


        return_chart = (chart1 & chart2 & chart3 ).configure_title(
            baseline="line-top",
            dy = -5
        )
        # return_chart = (chart1 & chart2 & chart3 & (dependency_chart | corr_text) & gdp_combine).configure_title(
        #     baseline="line-top",
        #     dy = -5
        # )

        ## https://stackoverflow.com/questions/67997825/python-altair-generate-a-table-on-selection
        ## https://altair-viz.github.io/user_guide/transform/filter.html?highlight=filter
        ## https://vega.github.io/vega/docs/schemes/        
        return return_chart
