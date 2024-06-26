import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents new Healthy Diner')
streamlit.header('🥣 Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast') 
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')  
#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
# streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Apple'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show) 
 

#create a repeatable block (called a function)
def get_fruityvice_data(this_fruit_choice):
	fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit_choice)
	fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
	return	fruityvice_normalized
# New Section to display fruityvice api response

# New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
	fruit_choice = streamlit.text_input('What fruit would you like information about?')
	if not fruit_choice:
		streamlit.error("Please select a fruit to get informaiton")
	else:
		back_from_function = get_fruityvice_data(fruit_choice)
		streamlit.dataframe(back_from_function)
		
except URLError as e:
	streamlit.error()
#streamlit.header("Fruit List Contains:")
streamlit.header("View our Fruit list - Add your Favorites! ") 
def	get_fruit_load_list():
	with my_cnx.cursor() as my_cur: 
		my_cur.execute("Select * from fruit_load_list") 
		return my_cur.fetchall()


# Add a button to load the fruit
if streamlit.button('Get the fruit list'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) 
	my_data_rows = get_fruit_load_list()
	my_cnx.close()
	streamlit.dataframe(my_data_rows)

#Allow end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
	with my_cnx.cursor() as my_cur:
		#my_cur.execute("insert into fruit_load_list values ('from streamlit')")
		my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "' )")
		return "Thanks for adding " + new_fruit 
		
add_my_fruit = streamlit.text_input('What fruit would you to add?') 
if streamlit.button('Add a fruit to the list'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) 
	back_from_function = insert_row_snowflake(add_my_fruit)
	streamlit.text(back_from_function)
	 
streamlit.stop()
#import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("Fruit List Contains:")
streamlit.dataframe(my_data_rows)
add_my_fruit = streamlit.text_input('What fruit would you to add?','Jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
