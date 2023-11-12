import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
from PIL import Image
from io import BytesIO


#st.set_config_file(path="./.streamlit/config.toml")


# from streamlit_autorefresh import st_autorefresh

# count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")


plant_image = 'farm_corn.jpg'
crop = "Corn"
percentage_crop = 85
percentage_disease = 90
new_t = 33
new_h = 68
sun_light = ["Full Sun", "Part Shade", "Full Shade"]
moisture = 10

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()
sample_data = pd.DataFrame({"Temperature": [24, 25, 27, 28, 28, 28, 28, 29, 30 ,30 ,29, 30 ,30 ,30, 32],
                            "Humidity": [65, 70, 69, 66, 66, 66, 66, 66, 65, 64, 66, 63, 62, 66, 65]})



df = pd.read_csv('HackPrinceton Plant Data.csv')
low_temp, high_temp = df[df['plant_name'] == crop]['temp_low'].values[0], df[df['plant_name'] == 'Corn']['temp_high'].values[0]
low_h, high_h = df[df['plant_name'] == crop]['humidity_low'].values[0], df[df['plant_name'] == crop]['humidity_high'].values[0]

count_val = lambda x: (1 if x > high_temp else 1 if x < low_temp else 0)

count_temp = list(map(count_val, sample_data['Temperature'])).count(1)

count_val = lambda x: (1 if x > high_h else 1 if x < low_h else 0)

count_h = list(map(count_val, sample_data['Humidity'])).count(1)

#Select Box
add_selectbox = st.sidebar.selectbox(
    "Which Module would you like to access?",
    ("Apple_1", "Apple_2", "Tomato_1", "Tomato_3", "Corn_3", "Corn_1")
)

# Using "with" notation
with st.sidebar:
    if add_selectbox == 'Corn_1':
        with st.spinner("Please wait..."):
            time.sleep(3)
    else:
        st.write("Module Disconnected")



with header:
    # st.title("Harvest Hero")
    st.markdown(f"""# Harvest Hero""")


    if st.button('Run Data Collection', use_container_width=True):
        with st.spinner('Please wait...'):
            time.sleep(2)
        #input function to run 
            
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

        sample_data.loc[len(sample_data)] = [new_t, new_h]
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
        st.info(f"""**Crop Classification Accuracy:** {percentage_crop}%""")
        # st.markdown(f"""**Crop Classification Accuracy: {percentage_crop}**%""")
        st.info(f"""**Disease Classification Accuracy:** {percentage_disease}%""")
        ## Place Holder


        if st.button('Reload', use_container_width=True):
            with st.spinner('Loading Image...'):
                time.sleep(2)



    

    with features:
        st.markdown(f"""### <u>Soil Moisure and Sun Light data:</u>""", unsafe_allow_html=True)

        
        col1, col2 = st.columns(2)
        col1.metric("Soil Moisture", "{m}%".format(m = moisture), "1.2 °F")
        col2.metric("Sun","{light}".format(light = sun_light[0]) , "-8%")
        
    