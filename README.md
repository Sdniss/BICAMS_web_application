# BICAMS normalization visualization [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/sdniss/bicams_web_application/BICAMS_application.py)

## Application location
Surf 🌊 🏄🏽‍ to the [Streamlit Application](https://share.streamlit.io/sdniss/bicams_web_application/BICAMS_application.py) and try it out for yourself!

## The project - understanding the comparison of cognitive scores

This project is an extension to the paper of [Costers et al. 2017](https://doi.org/10.1016/j.msard.2017.08.018), which was published in Multple Sclerosis and Related Disorders. In short, the paper validated the Brief International Cognitive Assessment for Multiple Sclerosis (BICAMS) in a Belgian, Dutch-speaking population. It hereby provided regression-based norms for the 3 subtests of BICAMS:

- The Symbol Digit Modalities Test (SDMT)
- The California Verbal Learning Test, 2nd edition (CVLT-II)
- The Brief Visuospatial Memory Test Revised (BVMT-R)

The regression-based norms allow a raw score on any of the 3 cognitive tests stated above to be converted to a score that is corrected for three factors that were found in the paper to impact cognitive performance:

- Age
- Gender
- Educational status

In short, by correcting for these factors, the resulting z-score can be compared to cognitive scores without interference by them. 3 important phases can be distinguished:

1. Scaling of the raw scores
2. Predicting which score should normally be obtained by the subject according to their age, sex and education level.
3. Obtain z-score: subtract the predicted score (2) from the scaled score (1), and divide by the residual error of the regression model

## What will you learn?

With this project, the reader will gain insight in how certain demographical parameters (age, age^2, gender and education level) affect the score on the SDMT, BVMT-R and CVLT-II. In the streamlit web application, the readership can adjust all parameters and scores according to their preferences. Also the cut-off (z score) that declares cognitive impairment can be chosen.

## About AIMS VUB

Thank you very much for your interest in this project on behalf of the Artificial Intelligence and Modelling in clinical Sciences (AIMS) lab, part of the Vrije Universiteit Brussel (VUB). We aim to contribute maximally to optimal clinical care in neurodegenerative disorders, with a special focus on Multiple Sclerosis, by performing relevant and advanced modelling on neurophysiological and brain imaging data. Moreover, in light of the prosper of the field and general understanding of our research, we do efforts to contribute to open, reproducible and transparant science by sharing code and actively practicing science communication on our [AIMS website](https://aims.research.vub.be).
