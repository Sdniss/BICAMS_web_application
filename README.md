 

# BICAMS normalization visualization

## Introduction - AIMS VUB

First of all, thank you very much for your interest in using our project on behalf of the Artificial Intelligence and Modelling in clinical Sciences (AIMS) lab, part of the Vrije Universiteit Brussel (VUB). We aim to contribute maximally to optimal clinical care in neurodegenerative disorders, with a special focus on Multiple Sclerosis, by performing relevant and advanced modelling on neurophysiological and brain imaging data. Moreover, in light of the prosper of the field and general understanding of our research, we do efforts to contribute to open, reproducible and transparant science by sharing code and actively practicing science communication on our [AIMS website]().

## Introduction - The project

This project is an extension to the paper of [Costers et al. 2017](https://doi.org/10.1016/j.msard.2017.08.018), which was published in Multple Sclerosis and Related Disorders. In short, the paper validated the Brief International Cognitive Assessment for Multiple Sclerosis (BICAMS) in a Belgian, Dutch-speaking population. It hereby provided regression-based norms for the 3 subtests of BICAMS:

- The Symbol Digit Modalities Test (SDMT)
- The California Verbal Learning Test, 2nd edition (CVLT-II)
- The Brief Visuospatial Memory Test Revised (BVMT-R)

The regression-based norms allow a raw score on any of the 3 cognitive tests stated above to be converted to a score that is corrected for three factors that were found in the paper to impact cognitive performance:

- Age
- Gender
- Educational status

In short, by correcting for these 3 factors, the resulting z-score can be compared to cognitive scores without interference by them. In the following section, we explain the code that performs exactly this transformation.

## Deliverables

With this project, the reader will gain insight in how certain demographical parameters (age, age^2, gender and education level) affect the score on the SDMT, BVMT-R and CVLT-II. In the streamlit web application, the readership can adjust all parameters and scores according to their preferences. Also the cut-off (z score) that declares cognitive impairment can be chosen.

## Repo explanation

The project adopts the following file structure:

1. BICAMS_application.py: the main script that runs the application using streamlit. It depends on the following elements:

   1. Data (`load_data.py`). Location of the data and description in the "data" and "data_descriptions" folder respectively.

      - class `ConversionTable`: a look-up table that is used for the conversion from raw to scaled scores

        Attributes:

        - `sdmt`: sdmt conversion table
        - `bvmt`: bvmt conversion table
        - `cvlt`: cvlt conversion table
        - `description`: description of the structure of a conversion table

      - class `ReferenceData`: A 100.000 element vector creating the normal distribution of the reference population.

        Attributes:

        - `data`: numpy array of length 100.000
        - `description`: description of the data

   2. Functions (`functions.py`)

      - `normalization_pipeline` is the mother function that combines all other functions to do the normalization
      - `get_expected_score` generates an expected cognitive score
      - `raw_to_scaled` converts raw value to scaled value
      - `to_z_score` turns the expected and scaled score to a z-score
      - `impaired_or_not` declares whether the z-score is impaired or not

## How to run it + dependencies

Run the `BICAMS_application.py` file using streamlit, which you have to install first using e.g. `pip3 install streamlit`

Furthermore, following libraries need to be installed within the environment you are working in.

- Pandas
- Numpy
- Seaborn
- Matplotlib

