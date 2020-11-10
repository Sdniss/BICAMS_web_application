import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from load_data import ConversionTable
from load_data import ReferenceData
from functions import normalization_pipeline

# Load the conversion tables
sdmt_conv_table = ConversionTable().sdmt
bvmt_conv_table = ConversionTable().bvmt
cvlt_conv_table = ConversionTable().cvlt

# Couple certain values with strings
sex_dict = {1: 'male',
            2: 'female'}

edu_dict = {'6 - primary school': 'primary school',
            '12 - high school': 'high school',
            '13 - professional education': 'professional education',
            '15 - bachelor': 'bachelor',
            '17 - master': 'master',
            '21 - doctorate': 'doctorate'}

# First print section on main page
st.title('How to compare cognitive scores in MS')
st.write("Learn here about a useful trick that allows to assess the true impact that Multiple Sclerosis has on people's cognitive performance: **transformation to z-scores**")
st.write('This work is based on the paper by [Costers et al. 2017](https://doi.org/10.1016/j.msard.2017.08.018)')
st.markdown('***')
st.header('Background Information')
st.write('Some essential concepts to make sure you optimally benefit from this application:')
st.write('The Brief International Cognitive Assessment for Multiple Sclerosis ([**BICAMS**](https://bmcneurol.biomedcentral.com/articles/10.1186/1471-2377-12-55)) is a test battery that screens for cognitive problems in MS. It consists of the following tests:')
st.write('- Symbol Digit Modalities Test (SDMT): A test for information processing speed')
st.write('- Brief Visuospatial Memory Test (BVMT): A test for visuospatial learning and memory')
st.write('- California Verbal Learning Test (CVLT): A test for verbal learning and memory')
st.write("Why should we transform these scores to z-scores, and what are z-scores? Let's get right to it! Please play around with the values and observe the impact on the figure below.")
st.markdown('***')
st.header("Choose subject's characteristics")

name = st.text_input(
    label = 'First, choose a nice name for your subject',
    value = 'Jane Doe')
st.write(f"Adapt {name}'s characteristics on the left")

st.markdown('***')

# Sidebar section
st.sidebar.subheader(f"{name}'s characteristics")

age = st.sidebar.slider(
    min_value=18,
    max_value=100,
    label = 'Define age (years)')

sex = st.sidebar.selectbox(
    label = 'Define sex (1: Male, 2: Female)',
    options = [1,2])

edu = st.sidebar.selectbox(
    label = 'Define educational level (years)',
    options = list(edu_dict.keys()))
edu = int(edu.split(' - ')[0]) # Only get the amount of years from the options list

sdmt = st.sidebar.slider(
    min_value=0,
    max_value=100,
    label = 'Define SDMT score')

bvmt = st.sidebar.slider(
    min_value=0,
    max_value=36,
    label = 'Define BVMT score')

cvlt = st.sidebar.slider(
    min_value=0,
    max_value=100,
    label = 'Define CVLT score')

# Create table
subject_dict = {'Age': age,
                'Age^2': age**2,
                'Gender': sex_dict.get(sex),
                'Education': edu_dict.get(edu),
                'SDMT': sdmt,
                'BVMT': bvmt,
                'CVLT': cvlt}
subject_DF = pd.DataFrame(subject_dict, index = [name])

# Create z-scores distribution plot
z_cutoff = -1.5
fig, ax = plt.subplots()
sns.kdeplot(ReferenceData().data, ax = ax, color= 'k', alpha =0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_xlabel('Z Score')
ax.set_xlim([-4,4])
kde_x, kde_y = ax.lines[0].get_data()
ax.fill_between(kde_x, kde_y, where= kde_x > -4, color='#b1eba9')  # First fill everything green
ax.fill_between(kde_x, kde_y, where=kde_x <= z_cutoff,color='#EF9A9A')  # Then fill red only where necessary

# Calculate z-scores and add to ax object
imp_dict = dict()
z_dict = dict()
for test, test_str, conv_table, colour,label_pos in zip([sdmt, bvmt, cvlt],
                                                        ['sdmt', 'bvmt', 'cvlt'],
                                                        [sdmt_conv_table, bvmt_conv_table, cvlt_conv_table],
                                                        ['blue', 'black','purple'],
                                                        [1,2,3]):

            z_score, imp_bool = normalization_pipeline(data_vector = [age, age**2, sex, edu],
                                               raw_score= test,
                                               test = test_str,
                                               conversion_table= conv_table,
                                               z_cutoff= z_cutoff)

            # Plot vertical line on x-position being z-score. Add vertical text alongside it.
            ax.axvline(x=z_score, color = colour)
            text_position = ax.get_ylim()[1]-(ax.get_ylim()[1]/10)*label_pos
            ax.text(x=z_score+0.05, y= text_position, s=test_str, rotation =90, color = colour)

            # Update imp_dict and z_dict
            if imp_bool == 0:
                        text = 'preserved'
            else:
                        text = 'impaired'
            imp_dict.update({test_str: text})
            z_dict.update({test_str: z_score})

# Get z-score and text for impaired/preserved
sdmt_z = round(z_dict.get('sdmt'), 2)
bvmt_z = round(z_dict.get('bvmt'), 2)
cvlt_z = round(z_dict.get('cvlt'), 2)
sdmt_imp = imp_dict.get('sdmt')
bvmt_imp = imp_dict.get('bvmt')
cvlt_imp = imp_dict.get('cvlt')
            
# Second print section on main page
st.header('View your results!')
st.subheader("Your subject's characteristics:")
st.write(subject_DF)
st.write(f'{name} scored:')
st.write(f'- SDMT: {sdmt}. Information Processing Speed is {sdmt_imp} (z-score = {sdmt_z})')
st.write(f'- BVMT: {bvmt}. Visual Learning and Memory is {bvmt_imp} (z-score = {bvmt_z})')
st.write(f'- CVLT: {cvlt}. Verbal Learning and Memory is {cvlt_imp} (z-score = {cvlt_z})')
st.subheader('Projection on z-scores disbribution')
st.pyplot(fig)
st.write('*the sensitivity of this normalization method (correcting with regression-based norms from a healthy reference population) is higher '
        'than traditional normalization methods. Thus, it is recommended to use a lower cut-off of -1 or -0.5, opposed to the [traditional value of -1.5](https://n.neurology.org/content/90/6/278), '
        'to classify a subject as cognitively impaired*')
st.write('This figure shows a gaussian, a distribution that is very common in nature. For example, **length** follows a gaussian distribution.') 
st.subheader('Figure interpretation')
st.write('- Many people will have an average length, so the curve is high in the middle')
st.write('- There will be gadually less people proportional to how much taller (right) or smaller (left) they are')
st.write('- The same applies for **cognitive performance**: many people will have average cognitive performance, extreme cases are rarer')
st.write('- When people score very low, they might fall into the red zone, **Cognitive Impairment**, that is defined here as having a z-score lower than 1.5')
st.markdown('***')
st.subheader('Why is normalization important?')
st.write('The values shown in the curve are **normalized** values, z-scores. They are computed by comparing the *raw score* to what we would *expect* this person '
         'to have based on the **Age**, **Gender** and **Education**. But why is it important to normalize raw cognitive scores? ' 
         'Because now, we can **compare** values; we expect an 85-year old man who only went to primary school to score lower than a 25-year old woman who went to university. ' 
         'If they both score 50 on sdmt, the woman will have a lower z-score, since we *expect* her score to be high based on her **Age**, **Gender** and **Education**. '
         'Now, we can study the true impact of Multiple Sclerosis on the cognitive performance of the subject.')
st.markdown('***')
st.subheader('Reference to paper:')
st.write('[Costers et al. "Does including the full CVLT-II and BVMT-R improve BICAMS? '
         'Evidence from a Belgian (Dutch) validation study." Multiple Sclerosis and Related Disorders 18 (2017):'
         ' 33-40.](https://doi.org/10.1016/j.msard.2017.08.018)')
