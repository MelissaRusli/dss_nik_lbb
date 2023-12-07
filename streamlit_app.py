import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout = 'wide')

# --- READ DATA ---
customer_clean = pd.read_pickle('data/customer_clean.pkl')
coord = pd.read_csv('data/coordinate.csv')

# --- ROW 1 ---
st.title('Customer Demography Dashboard')
st.write("""Explore Customer Profiling at a glance with this Customer Demography Dashboard. 
         Visualize customer distribution across provinces, 
         and delve into spending habits of Customers across generational and gender insights""")

# --- ROW 2 ---
col1, col2 = st.columns(2)

## --- MAP PLOT --- 
# data: map
prov_gender = pd.crosstab(index = customer_clean['province'],
                   columns = customer_clean['gender'],
                   colnames=[None]).reset_index()

prov_gender['Total'] = prov_gender['Female'] + prov_gender['Male']

df_map = prov_gender.merge(coord, on='province')

# plot: map
plot_map = px.scatter_mapbox(data_frame=df_map, lat='latitude', lon='longitude',
                             mapbox_style='carto-positron', zoom=3,
                             size='Total',
                             hover_name='province',
                             hover_data={'Male': True,
                                         'Female': True,
                                         'latitude': False,
                                         'longitude': False})

col1.write('### Customer Count across Indonesia')
col1.plotly_chart(plot_map, use_container_width=True)


## Horizontal Bar Plot

# data: income level per profesi
prof_income_level = pd.crosstab(index = customer_clean['Profession'],
                                columns = customer_clean['income_level'],
                                colnames=[None])

prof_income_level_melt = prof_income_level.melt(ignore_index=False,
                                                var_name = 'income_level',
                                                value_name = 'num_people')

prof_income_level_melt = prof_income_level_melt.reset_index()

# plot : horizontal bar plot
plot_prof_income = px.bar(data_frame = prof_income_level_melt,
                          x = 'num_people', y = 'Profession',
                          color = 'income_level',
                          barmode = 'group',
                          labels = {'num_people' : 'Customer Count',
                                   'income_level' : 'Income Level'}
                        )


col2.write('### Customer Count For Each Profession by Income Level')
col2.plotly_chart(plot_prof_income, use_container_width=True)



# --- ROW 3 ---
st.divider()
col3, col4 = st.columns(2)

## --- INPUT SLIDER ---
input_slider = col3.slider(
    label ='Select age range',
    min_value = customer_clean['age'].min(),
    max_value = customer_clean['age'].max(),
    value = [20,55]
)

min_slider = input_slider[0]
max_slider = input_slider[1]


## --- INPUT SELECT ---
input_select = col4.selectbox(
    label = 'Select Customer Profession',
    options = customer_clean['Profession'].unique().sort_values()
)

# --- ROW 4 ---
col5, col6 = st.columns(2)

## --- MULTIVARIATE ---

# data: multivariate
customer_age = customer_clean[customer_clean['age'].between(left=min_slider, right=max_slider)]
customer_level_gender = pd.crosstab(index = customer_age['customer_level'],
                                    columns = customer_age['gender'],
                                    colnames = [None])

customer_level_gender_melt = customer_level_gender.melt(ignore_index=False, 
                                                        var_name='gender', 
                                                        value_name='num_people')
customer_level_gender_melt = customer_level_gender_melt.reset_index()

# plot: multivariate
plot_cust_level = px.bar(data_frame = customer_level_gender_melt, 
                         x = 'customer_level', y = 'num_people', 
                         color = 'gender', 
                         barmode = 'group',
                         labels = {'num_people' : 'Customer Count',
                                   'customer_level' : 'Spending Level',
                                   'gender': 'Gender'}
                        )

col5.write(f'### Gender per Customer Spending Level, Age {min_slider} to {max_slider}')
col5.plotly_chart(plot_cust_level, use_container_width=True)

## --- BARPLOT ---

# data: barplot
customer_profession = customer_clean[customer_clean['Profession'] == input_select]
df_gen = pd.crosstab(index = customer_profession['generation'], 
                     columns = 'num_people', 
                     colnames = [None])
df_gen = df_gen.reset_index()

# plot: barplot
plot_gen = px.bar(df_gen, x='generation', y='num_people', 
                   labels = {'generation' : 'Generation',
                             'num_people' : 'Customer Count'})

col6.write(f'### Customer Count per Generation with Profession as {input_select}.') # f-string
col6.plotly_chart(plot_gen, use_container_width=True)