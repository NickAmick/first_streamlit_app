import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title('My Parents New Healthy Diner')
  
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

streamlit.header('Fruityvice Fruit Advice!')
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered', fruit_choice)
fruityvice_response = requests.get(f'https://www.fruityvice.com/api/fruit/{fruit_choice}')

fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("use warehouse compute_wh")

my_data_rows = my_cur.execute("select * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST").fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

fruit_choice_2 = streamlit.text_input('What fruit would you like to add?')
if fruit_choice_2:
  my_cur.execute(f"INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES {fruit_choice_2}")
  streamlit.write('Thanks for adding:', fruit_choice_2)

  
