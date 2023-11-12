import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
from PIL import Image

def refresh_button():
    if st.button("Refresh Page"):
        st.experimental_rerun()

# from streamlit_autorefresh import st_autorefresh

# count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")


plant_image = 'farm_corn.jpg'

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()
sample_data = pd.DataFrame({"Temperature": [24, 25, 27, 28, 28, 28, 28, 29, 30 ,30 ,29, 30 ,30 ,30, 32],
                            "Humidity": [65, 70, 69, 66, 66, 66, 66, 66, 65, 64, 66, 63, 62, 66, 65]})

crop = "Corn"

df = pd.read_csv('HackPrinceton Plant Data.csv')
low_temp, high_temp = df[df['plant_name'] == crop]['temp_low'].values[0], df[df['plant_name'] == 'Corn']['temp_high'].values[0]
low_h, high_h = df[df['plant_name'] == crop]['humidity_low'].values[0], df[df['plant_name'] == crop]['humidity_high'].values[0]

count_val = lambda x: (1 if x > high_temp else 1 if x < low_temp else 0)

count_temp = list(map(count_val, sample_data['Temperature'])).count(1)

count_val = lambda x: (1 if x > high_h else 1 if x < low_h else 0)

count_h = list(map(count_val, sample_data['Humidity'])).count(1)


with header:
    st.title('Welcome to HackPrinceton!')
    refresh_button()


# Select Box
# add_selectbox = st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone")
# )

# # Using "with" notation
# with st.sidebar:
#     if add_selectbox == 'Home phone':
#         st.write('Thank you for choosing')



with dataset:

    col1, col2 = st.columns(2)
   # Columns 
    with col1: 
        st.subheader('Plant Optimal Dataset')

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


        # Dialog boxes for temperature and Humidity readings 
        if count_h > 10: st.error('Danger: Extreme humidity readings! Consider crop relocation', icon ="🚨")
        elif count_h > 5: st.warning("Warning: Volatile humidity readings\n Check {} crop".format(crop), icon="⚠️")
        else: st.success('Safe: Humidity Levels normal', icon="✅")

        if count_temp > 10: st.error('Danger: Exreme temperature readings! Consider crop', icon ="🚨")
        elif count_temp > 5: st.warning("Warning: Volatile temperature readings! Check {} crop".format(crop), icon="⚠️")
        else: st.success('Safe: Temperature Levels normal', icon="✅")

    with col2:
        # Image data
        st.subheader("Image Data", divider=[])
        def load_image():
            st.markdown(
                """
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="flex: 1; margin-right: 20px;">
                        <img src="//farm_corn.jpg" alt="Image 1" style="width: 100%;">
                        <p style="text-align: center;">Caption for Image 1</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            image = Image.open(plant_image)
            st.image(image, caption=str(crop))

        load_image()
        ## Place Holder


        if st.button('Reload'):
            with st.spinner('Loading Image...'):
                time.sleep(3)



    

    with features:
        st.header('The features I created')

    with model_training:
        st.header('Model_training')
        st.subheader('Crop Classification')
        st.text('Determine the plant species: ')

        st.subheader('Crop disease and Pest classification')
        st.text('Determine if any diseases or pests have infected the crop')
    