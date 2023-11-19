import streamlit as st
import socket
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from PIL import Image
from io import BytesIO
import os
import pickle

os.chdir('D:/Rutgers/ExtraProjects/HackPrinceton23/HackPrinceton23/')



#st.set_config_file(path="./.streamlit/config.toml")


# from streamlit_autorefresh import st_autorefresh

# count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

file = open('Test Images/newData.txt', 'rb')

# dump information to that file
data = pickle.load(file)

# close the file
file.close()

plant_image = 'Test Images/CurrentImage.jpg'
crop = "Corn"
disease_status = data[0]
percentage_disease = data[1]
new_t = [int(i) for i in data[2].split() if i.isdigit()].join("")
new_h = [int(i) for i in data[3].split() if i.isdigit()].join("")
new_l = [int(i) for i in data[4].split() if i.isdigit()].join("")
sunlight_index = 3
sun_light = ["Full Sun", "Part Shade", "Full Shade"]
moisture = [int(i) for i in data[5].split() if i.isdigit()].join("")
old_m = moisture[-1]
new_m = moisture[0]
new_t = int(''.join(filter(str.isdigit, data[2])))
new_h = int(''.join(filter(str.isdigit, data[3])))
new_l = int(''.join(filter(str.isdigit, data[4])))
sun_light = ["Full Sun", "Part Shade", "Full Shade"]
moisture = int(''.join(filter(str.isdigit, data[5])))

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()
sample_data = pd.DataFrame({"Temperature": [23, 25, 27, 24, 22, 28, 25, 24],
                            "Humidity": [45, 44, 50, 54, 55, 52, 48, 49]})


## Get datatable with ideal conditions 
df = pd.read_csv('../HackPrinceton Plant Data.csv')

df = pd.read_csv('HackPrinceton Plant Data.csv')
low_temp, high_temp = df[df['plant_name'] == crop]['temp_low'].values[0], df[df['plant_name'] == 'Corn']['temp_high'].values[0]
low_h, high_h = df[df['plant_name'] == crop]['humidity_low'].values[0], df[df['plant_name'] == crop]['humidity_high'].values[0]

## Count number of temperature values out of bounds
count_val = lambda x: (1 if x > high_temp else 1 if x < low_temp else 0)
count_temp = list(map(count_val, sample_data['Temperature'])).count(1)

## Count number of humidity values out of bounds 
count_val = lambda x: (1 if x > high_h else 1 if x < low_h else 0)
count_h = list(map(count_val, sample_data['Humidity'])).count(1)


###### Plotting data

def plotChart():
            subheader_text = "Plant Optimal Data"
            centered_subheader = f"<h3 style='text-align: center;'>{subheader_text}</h3>"
            st.markdown(centered_subheader, unsafe_allow_html=True)

            fig, ax1 = plt.subplots()
            # Plotting temperature

            ax1.plot(sample_data['Temperature'], marker='o', color=[0.18, 0.32, 0.70], label='Temperature')
            ax1.axhspan(low_temp, high_temp, facecolor=[0.248, 0.42, 0.692], alpha=0.3, label='Ideal Temperature')
            ax1.set_ylabel('Temperature (°C)').set_color([0.248, 0.42, 0.692])
            ax1.set_ylim(0, 100)
            plt.title('Temperature and Humidity Data')

            # Plotting humidity
            ax2 = ax1.twinx()
            ax2.set_ylim(0,100)
            ax2.plot(sample_data['Humidity'], marker='o', color=[0.148,0.42, 0.16], label='Humidity')
            ax2.axhspan(low_h, high_h, facecolor='green', alpha=0.3, label='Ideal Humidity')
            ax2.set_ylabel('Humidity (%)').set_color('green')
            # [0.828, 0.58, 0.156]
            fig.legend()
            ax1.grid(axis='y')

            # Adjust layout
            fig.tight_layout()

            # Show the plot
            st.pyplot(fig)


#Select Box in sidebar and spinner returns "please wait" when selecting "Corn_1" otherwise
add_selectbox = st.sidebar.selectbox(
    "Which Module would you like to access?",
    ("Apple_1", "Apple_2", "Tomato_1", "Tomato_3", "Corn_3", "Corn_1")
)

'''
 Sidebar and spinner returns "please wait" when selecting "Corn_1" otherwise
 returns "module diconnected" to add more modules, the sidebar will
 have to call the reload function with a new dataset

 later demos
'''
with st.sidebar:
    if add_selectbox == 'Corn_1':
        with st.spinner("Please wait..."):
            time.sleep(3)
    else:
        st.write("Module Disconnected")



## Header (needs an update to the HTML to make it bigger and centered)
with header:
    # st.title("Harvest Hero")
    st.markdown(f"""# Harvest Hero""")

### Data Collection button will reload the page for 
    if st.button('Run Data Collection', use_container_width=True):
        with st.spinner('Please wait...'):
            time.sleep(2)       
        
        #######################
        '''
        
                input function to pull new data and save in new_t and new_h 
        
                Make sure new_t and new_h is an array
        
        '''
        #######################
        
        
        x = len(new_t)
        sample_data = sample_data.iloc[x:,:]
        sample_data = pd.concat([sample_data, pd.DataFrame(data = np.column_stack([new_t, new_h]), columns = ['Temperature', 'Humidity'])], ignore_index= True)
        plotChart()         ## plots the chart
        st.experimental_rerun()        ## Reruns the whole window
        time.sleep(2)
            
        # Append the new data
        sample_data = sample_data.append({"Temperature": new_t, "Humidity": new_h}, ignore_index=True)

        # Drop the first row to keep the DataFrame length consistent
        sample_data = sample_data.drop(sample_data.index[0])

        # Reset the index after dropping the row
        sample_data = sample_data.reset_index(drop=True)

        plotChart()
        st.experimental_rerun()



#     place.markdown("""
# <div style="position: absolute; top: 0px; left: 250px;">
#     <h1>Harvest Hero</h1>
# </div>
# """, unsafe_allow_html=True)
    # st.title("Harvest Hero", anchor='center')


with dataset:

    col1, col2 = st.columns(2)
   # Columns 
    with col1:
        plotChart()

        # Dialog boxes for temperature and Humidity readings 
        if count_h > 10: st.error('Danger: Extreme humidity readings! Consider crop relocation', icon ="🚨")
        elif count_h > 5: st.warning("Warning: Volatile humidity readings\n Check {} crop".format(crop), icon="⚠️")
        else: st.success('Safe: Humidity Levels normal', icon="✅")

        if count_temp > 10: st.error('Danger: Exreme temperature readings! Consider crop', icon ="🚨")
        elif count_temp > 5: st.warning("Warning: Volatile temperature readings! Check {} crop".format(crop), icon="⚠️")
        else: st.success('Safe: Temperature Levels normal', icon="✅")

    with col2:
        # Image data
        # Define a subheader
        subheader_text = "Image Data"
        centered_subheader = f"<h3 style='text-align: center;'>{subheader_text}</h3>"
        st.markdown(centered_subheader, unsafe_allow_html=True)
        
        def load_image():
            image = Image.open(plant_image)
            st.image(image, caption=str(crop), width=400)

        load_image()
        # st.markdown(f"""**Crop Classification Accuracy: {percentage_crop}**%""")
        st.info(f"""**Disease Evaluation:** {disease_status}""")
        st.info(f"""**Disease Classification Confidence:** {percentage_disease}%""")
        ## Place Holder

        ## Reload the image
        if st.button('Reload', use_container_width=True):
            with st.spinner('Loading Image...'):
                time.sleep(2)

                '''
                Add the code to get the image
                '''
                plant_image = "Test Images/ ::::: Fill image name here :::::"
                load_image()
            



    

    with features:
        st.markdown(f"""### <u>Soil Moisure and Sun Light data:</u>""", unsafe_allow_html=True)

        
        col1, col2 = st.columns(2)
        moisture_increase = ((new_m / old_m) - 1) * 100
        sun_increase = sunlight_index

        col1.metric("Soil Moisture", "{m}%".format(m = moisture),
                     "{m_increase}%".format(m_increase = moisture_increase))
        col2.metric("Sun","{light}".format(light = sun_light[0]) , 
                    "{s_increase}x".format(s_increase = sun_increase))
        col1.metric("Soil Moisture", "{m}%".format(m = moisture/100), "1.2%")
        col2.metric("Sun","{light}".format(light = sun_light[0]) , "33%")
        
    
