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

edu_dict = {6: 'primary school',
            12: 'high school',
            13: 'professional education',
            15: 'bachelor',
            17: 'master',
            21: 'doctorate'}

# First print section on main page
st.title('BICAMS normalization visualization')
st.write("Learn here about a useful trick that allows to assess the true impact that Multiple Sclerosis has on people's cognitive performance: transformation to z-scores")
st.markdown('***')
st.header('Choose your preferences')
st.markdown('**1. Cognitive impairment cut-off**')

# region Generators of values: Sliders and boxes
z_cutoff = st.selectbox(
    label = 'Choose at which z-score cutoff you declare impairment',
    options = [-1.5, -1, -0.5, 0])


name = st.sidebar.selectbox(
    label = 'Choose a nice name for your subject',
    options = ['Guy', 'Jeroen', 'Lars', 'Johan', 'Stijn', 'Chiara', 'Frederik', 'Delphine'])

age = st.sidebar.slider(
    min_value=18,
    max_value=100,
    label = 'Define age (years)')

sex = st.sidebar.selectbox(
    label = 'Define sex (1: Male, 2: Female)',
    options = [1,2])

edu = st.sidebar.selectbox(
    label = 'Define educational level (years)',
    options = [6, 12, 13, 15, 17, 21])

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
# endregion

# Create table
subject_dict = {'Age': age,
                'Age^2': age**2,
                'Gender': sex_dict.get(sex),
                'Education': edu_dict.get(edu),
                'SDMT': sdmt,
                'BVMT': bvmt,
                'CVLT': cvlt}
subject_DF = pd.DataFrame(subject_dict, index = [name])

# region Create z-scores distribution plot
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
# endregion

# Calculate z-scores and add to ax object
imp_dict = dict()
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

            # Update imp_dict
            if imp_bool == 0:
                        text = 'preserved'
            else:
                        text = 'impaired'
            imp_dict.update({test_str: text})

# Get text for impaired/preserved
sdmt_imp = imp_dict.get('sdmt')
bvmt_imp = imp_dict.get('bvmt')
cvlt_imp = imp_dict.get('cvlt')
            
# Second print section on main page
st.markdown("**2. Subject's characteristics**")
st.write('Adapt this on the left side of the screen')
st.markdown('***')
st.header('View your results!')
st.subheader("Your subject's characteristics:")
st.write(subject_DF)
st.write(f'{name} scored:')
st.write(f'- SDMT: {sdmt}. Information Processing Speed is {sdmt_imp}')
st.write(f'- BVMT: {bvmt}. Visual Learning and Memory is {bvmt_imp}')
st.write(f'- CVLT: {cvlt}. Verbal Learning and Memory is {cvlt_imp}')
st.subheader('Projection on z-scores disbribution')
st.pyplot(fig)
st.write('This figure shows a gaussian, a distribution that is very common in nature. For example, **length** follows a gaussian distribution.') 
st.subheader('Figure interpretation')
st.write('- Many people will have an average length, so the curve is high in the middle')
st.write('- There will be gadually less people proportional to how much taller (right) or smaller (left) they are')
st.write('- The same applies for **cognitive performance**, many people will have average cognitive performance; extreme cases are rarer')
st.write('- When people score very low, they might fall into the red zone. When this **Cognitive Impairment** will be the case depends on the cut-off (defined above)')
st.markdown('***')
st.subheader('Why is normalization important?')
st.write('The values shown in the curve are **normalized** values, z-scores. Why is it important to normalize raw cognitive scores? ' 
         'Because now, we can **compare** values; we expect an 85-year old man who only went to primary school to score lower than a 25-year old woman who went to university. ' 
         'If they both score 50 on sdmt, we have to correct for their **Age**, **Gender** and **Education** in order to be able to compare them. '
         'Now, we can study the true **impact of multiple sclerosis** on the cognitive performance of the subject.')
st.markdown('***')
st.subheader('Reference to paper:')
st.write('[Costers et al. "Does including the full CVLT-II and BVMT-R improve BICAMS? '
         'Evidence from a Belgian (Dutch) validation study." Multiple Sclerosis and Related Disorders 18 (2017):'
         ' 33-40.](https://doi.org/10.1016/j.msard.2017.08.018)')
