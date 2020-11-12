import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from load_data import ConversionTable
from load_data import ReferenceData
from functions import normalization_pipeline, get_table_download_link

# Load the conversion tables
sdmt_conv_table = ConversionTable().sdmt
bvmt_conv_table = ConversionTable().bvmt
cvlt_conv_table = ConversionTable().cvlt

# Initiate some options
sex_options = ['1 - Male', '2 - Female']
edu_options = ['6 - primary school', '12 - high school', '13 - professional education', '15 - bachelor', '17 - master', '21 - doctorate']

# First print section on main page
st.image('VUB-AIMS-RGB.png', use_column_width=True)
st.title('How to compare cognitive scores in MS')
st.write("Learn here about a useful trick that allows to assess the true impact that Multiple Sclerosis has on people's cognitive performance: **transformation to z-scores**")
st.write('This work is based on the paper by [Costers et al. 2017](https://doi.org/10.1016/j.msard.2017.08.018)')
st.write('**Do you want to convert your own data to z-scores? Scroll down for more details!**')
st.markdown('***')
st.title('Part 1: Illustration of z normalization')
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
    label = 'Define sex',
    options = sex_options)
sex_int = int(sex.split(' - ')[0])

edu = st.sidebar.selectbox(
    label = 'Define educational level (years)',
    options = edu_options)
edu_int = int(edu.split(' - ')[0]) # Only get the amount of years from the education string

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
                'Gender': sex.split(' - ')[1], # Get gender from the string
                'Education': edu.split(' - ')[1], # Get the degree from the education string
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

            z_score, imp_bool = normalization_pipeline(data_vector = [age, age**2, sex_int, edu_int],
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
            
# Results section
st.header('View your results!')
st.subheader("Your subject's characteristics:")
st.write(subject_DF)
st.write(f'{name} scored:')
st.write(f'- SDMT: {sdmt}. Information Processing Speed is {sdmt_imp} (z-score = {sdmt_z})')
st.write(f'- BVMT: {bvmt}. Visual Learning and Memory is {bvmt_imp} (z-score = {bvmt_z})')
st.write(f'- CVLT: {cvlt}. Verbal Learning and Memory is {cvlt_imp} (z-score = {cvlt_z})')
st.subheader('Projection on z-scores disbribution')
st.pyplot(fig)
show_disclaimer = st.button(label = 'Show disclaimer about impairment cut-off of z = -1.5')
if show_disclaimer:
            st.write('*The sensitivity of this normalization method (correcting with regression-based norms from a healthy reference population) is higher '
                     'than traditional normalization methods. Thus, it is recommended to use a lower cut-off of -1 or -0.5, opposed to the [traditional value of -1.5](https://n.neurology.org/content/90/6/278), '
                     'to classify a subject as cognitively impaired.*')
st.write('This figure shows a gaussian, a distribution that is very common in nature. For example, **length** follows a gaussian distribution.') 
st.subheader('Figure interpretation')
st.write('- Many people will have an average length, so the curve is high in the middle')
st.write('- There will be gadually less people proportional to how much taller (right) or smaller (left) they are')
st.write('- The same applies for **cognitive performance**: many people will have average cognitive performance, extreme cases are rarer')
st.write('- When people score very low, they might fall into the red zone, **Cognitive Impairment**, that is defined here as having a z-score lower than 1.5')
st.markdown('***')

# Explanation of normalization
st.subheader('Why is normalization important?')
st.write('The values shown in the curve are **normalized** values, z-scores. They are computed by comparing the *raw score* to what we would *expect* this person '
         'to have based on the **Age**, **Gender** and **Education**. But why is it important to normalize raw cognitive scores? ' 
         'Because now, we can **compare** values; we expect an 85-year old man who only went to primary school to score lower than a 25-year old woman who went to university. ' 
         'If they both score 50 on sdmt, the woman will have a lower z-score, since we *expect* her score to be high based on her **Age**, **Gender** and **Education**. '
         'Now, we can study the true impact of Multiple Sclerosis on the cognitive performance of the subject.')

# File upload and conversion section
st.markdown('***')
st.title('Part 2: Convert your own data!')
st.markdown('***')
st.header('Step 1: Prepare your data')
st.write('This is what your data should look like:')
st.write(pd.read_excel("data/mock_data.xlsx").head())
st.write('- *age* column: years (integer)')
st.write('- *sex* column: 1 = Male, 2 = Female (integer)')
st.write('- *education* column: years of education (integer). Choose from [6, 12, 13, 15, 17, 21]. '
         'Check the option list in the sidebar ("Define education level") for the corresponding degrees.')
st.write('- *sdmt/bvmt/cvlt*: raw score on the test (integer)')
st.write('**Note 1**: please use exactly these column names in this order')
st.write('**Note 2**: only the 3 first columns are an absolute requirement. '
         'For the cognitive scores, please prepare your dataframe to only contain columns for which you have data. '
         'Hence, this can be a subset of the latter 3 columns, but should at least include one of them')

st.header('Step 2: Define the z-score on which you want to declare cognitive impairment')
z_cutoff = st.selectbox(label = 'Choose the z cutoff score',
                        options = [-1.5, -1, -0.5, 0])

st.header('Step 3: Upload your excel file')
input_object = st.file_uploader("Browse for a file or drag and drop here:", type=("xlsx"))
if input_object:
    input_data = pd.read_excel(input_object)

    # region Perform checks if the data was correctly entered
    error_dict = {'columns': 'Please be sure to use the correct column names and that they are lower case',
                  'age': 'Please use age values between 0 and 125 years, and only use integer values',
                  'sex': 'Please assure the following encoding: Male = 1, Female = 2',
                  'education': 'Please use education levels that are encoded as 6, 12, 13, 15, 17 or 21 years',
                  'sdmt': 'Please use sdmt values between 0 and 110',
                  'bvmt': 'Please use bvmt values between 0 and 36',
                  'cvlt': 'Please use cvlt values between 0 and 80'}

    allowed_range_dict = {'columns': {'age', 'sex', 'education', 'sdmt', 'bvmt', 'cvlt'},
                          'age': set(range(0, 126)),
                          'sex': {1, 2},
                          'education': {6, 12, 13, 15, 17, 21},
                          'sdmt': set(range(0, 111)),
                          'bvmt': set(range(0, 37)),
                          'cvlt': set(range(0, 81))}

    for key in ['columns'] + list(input_data.columns):
        # Extract the data vector for a specific key
        if key == 'columns':
            input_vector = set(input_data.columns)
        else:
            input_vector = set(input_data[key])
        # Check whether the vector is within the allowed range
        if not input_vector.issubset(allowed_range_dict.get(key)):
            raise ValueError(error_dict.get(key))

    # endregion

else:
    input_data = pd.DataFrame()

# Table Conversion
if input_data.empty == False:

    # Print preview of the data
    st.write('Your input data (first 5 rows):')
    st.write(input_data)

    # Add age^2 column for the calculation
    age_2 = input_data['age'] ** 2
    input_data.insert(loc=1, column='age^2', value=age_2)  # insert age^2 column in second position (thus loc = 1)

    # Load the data (either mock data or your data)
    demographics = input_data[['age', 'age^2', 'sex', 'education']]
    cognitive_raw = input_data.drop(['age', 'age^2', 'sex', 'education'], axis=1)

    # Load the conversion tables
    conversion_table_dict = {'sdmt': ConversionTable().sdmt,
                             'bvmt': ConversionTable().bvmt,
                             'cvlt': ConversionTable().cvlt}

    # region Calculate all z-scores and binary scores (impaired / preserved) for all tests and all subjects
    # General initiations
    transform_matrix = []

    for subject in range(input_data.shape[0]):

        # Initiations per subject
        z_row = []
        imp_row = []

        for test in cognitive_raw.columns:

            # Extract raw data from dataframe
            raw_scores = cognitive_raw[test]

            # Get correct conversion table
            conv_table = conversion_table_dict.get(test)

            # Calculate z-score and whether it is impaired or not for the test and subject
            z_score, imp_bool = normalization_pipeline(data_vector = demographics.iloc[subject],
                                                       raw_score= raw_scores.iloc[subject],
                                                       test = test,
                                                       conversion_table= conv_table,
                                                       z_cutoff= z_cutoff)

            # Append lists
            z_row.append(z_score)
            imp_row.append(imp_bool)

        # Append to general matrix
        transform_matrix.append(z_row + imp_row)

    # endregion

    # region Put in matrix
    # Define new columnnames for dataframe
    z_score_columns = [element + '_z' for element in cognitive_raw.columns]
    imp_columns = [element + '_imp' for element in cognitive_raw.columns]
    new_columns = z_score_columns + imp_columns

    # Convert matrix to pandas dataframe
    transform_matrix = pd.DataFrame(data=transform_matrix,
                                    columns=new_columns)
    # endregion

    # Concatenate original data with the z-scores and impairment boolean columns
    transformed_data = pd.concat([input_data, transform_matrix], axis = 1)

st.header('Step 4: Download your file, enriched with new information!')
if input_data.empty == False:
    st.write('A little sneak peak:')
    st.write(transformed_data.head())
    st.write('Fetch your excel file below!')
    st.markdown(get_table_download_link(transformed_data), unsafe_allow_html=True)
    st.write('**Note**')
    st.write('- In the "imp" columns, 0 denotes preserved, 1 denotes impaired')
    st.write('- age^2 was added which is the age column squared. This is necessary to calculate the z-scores.') 
else:
    st.write('Nothing to show now, upload your file in step 3!')
st.markdown('***')

# Paper reference
st.subheader('Reference to paper:')
st.write('[Costers et al. "Does including the full CVLT-II and BVMT-R improve BICAMS? '
         'Evidence from a Belgian (Dutch) validation study." Multiple Sclerosis and Related Disorders 18 (2017):'
         ' 33-40.](https://doi.org/10.1016/j.msard.2017.08.018)')
st.markdown('***')

# Contact details of author
st.subheader('About the author')
st.image('Stijn_Violin.jpg', width=150)
st.write('Hello there!:wave: My name is Stijn Denissen, and I am a PhD student of the '
         '[AIMS lab @ VUB](https://aims.research.vub.be/), studying the interplay between '
         'artificial Intelligence and neuroscience, applied to Multiple Sclerosis. I am highly enthousiastic '
         'about making science accessible to anyone interested.')
st.write('This project aims to provide insight in studying cognitive performance in MS, '
         'one of the research interests of the [AIMS lab](https://aims.research.vub.be/). '
         'Furthermore, it offers a quick tool to standardize cognitive scores, as an additional effort '
         'to the [paper](https://doi.org/10.1016/j.msard.2017.08.018) of Lars Costers, '
         'a fellow PhD student at the AIMS lab.')
st.write('I am happy to get in touch! Just send a mail to <stijn.denissen@vub.be> :wink:')
st.markdown('[twitter](https://twitter.com/denissenstijn) - [LinkedIn](https://www.linkedin.com/in/stijndenissen/) - [github](https://github.com/Sdniss)')
