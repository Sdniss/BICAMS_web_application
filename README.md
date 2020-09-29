 

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

In short, by correcting for these factors, the resulting z-score can be compared to cognitive scores without interference by them. 3 important phases can be distinguished:

1. Scaling of the raw scores
2. Predicting which score should normally be obtained by the subject according to their age, sex and education level.
3. Obtain z-score: subtract the predicted score (2) from the scaled score (1), and divide by the residual error of the regression model

## Deliverables

With this project, the reader will gain insight in how certain demographical parameters (age, age^2, gender and education level) affect the score on the SDMT, BVMT-R and CVLT-II. In the streamlit web application, the readership can adjust all parameters and scores according to their preferences. Also the cut-off (z score) that declares cognitive impairment can be chosen.

## How to run it + dependencies
General: Make sure that you have any version of python 3 installed on your computer.

### 1. Clone the repository to your local computer

Please open a terminal window in a folder that will subsequently contain the GitHub repo after running following command: `git clone https://github.com/Sdniss/BICAMS_web_application`. Subsequently, type `cd BICAMS_web_application` to enter that folder in the terminal.

### 2. Environment set-up:

To be able to run the main script, we first have to set up the environment containing the correct dependencies that the code relies on. In the table below, please pick the column that accords with the operating system you are using and run the commands in the terminal. Under the `explanation` column, you can keep track of what operation is performed with the corresponding command.

| Step | Explanation                                                  | Mac                                    | Windows                             | Linux                                  |
| ---- | ------------------------------------------------------------ | -------------------------------------- | ----------------------------------- | -------------------------------------- |
| 1    | Create a virtual environment (`BICAMS_norm_venv`) within your local repository | `python3 -m venv BICAMS_norm_venv`     | `python3 -m venv BICAMS_norm_venv`  | `python3 -m venv BICAMS_norm_venv`     |
| 2    | Activate the virtual environment                             | `source BICAMS_norm_venv/bin/activate` | `BICAMS_norm_venv\Scripts\activate` | `source BICAMS_norm_venv/bin/activate` |
| 3    | Install all dependencies (`dependencies.txt`) within the virtual environment | `pip3 install -r dependencies.txt`     | `pip3 install -r dependencies.txt`  | `pip3 install -r dependencies.txt`     |

> Warning: Installing dependencies takes some time

### 3. Running the main script

Run `streamlit run BICAMS_application.py` to start the application. A localhost will appear in your browser, or you can fetch it as printed in the terminal after `Local URL:`. The app is now visible in this browser tab. Once you adapt something in the app, the script will automatically run again and update the app according to your preferences.

