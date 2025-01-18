<<<<<<< HEAD
# Analyzing the Relationship between Renewable Energy Consumption,CO2 Emissions in North/South/Middle America

> *This repository has been forked from the [jvalue-made-template](https://github.com/jvalue/made-template) repository.*

<figure>
    <img src="CO2_image.png" style="width:100%">
</figure>

## Project Overview
The project seeks to examine the influence of renewable energy consumption on CO₂ emissions within the electricity sector. Amid growing global concerns about climate change, renewable energy sources such as solar, wind, and hydro are increasingly being promoted as sustainable alternatives to fossil fuels. This study aims to evaluate whether the adoption of renewable energy results in significant reductions in CO₂ emissions and to analyze the factors that shape this relationship.

# Data Sources
| | Data source 1 | Data source 2 |
| ----------- | ----- | ----------- |
| Title | European Electricity | World GDP |
| Metadata URL | [Renewable Energy](https://data.worldbank.org/indicator/EG.FEC.RNEW.ZS) | [CO2 emission Data](https://data.worldbank.org/indicator/EN.GHG.CO2.PI.MT.CE.AR5) |
| Data URL | [Renewable energy Raw Data](https://api.worldbank.org/v2/en/indicator/EG.FEC.RNEW.ZS?downloadformat=c
sv)  [CO2 emission Raw Data ](https://api.worldbank.org/v2/en/indicator/EN.GHG.CO2.PI.MT.CE.AR5?downloadformat=csv) |
| Data Type | CSV Directory | CSV |
| License | CC-BY-4.0 [License](https://ember-climate.org/creative-commons/) | CC-BY-4.0 [License](https://datacatalog.worldbank.org/public-licenses#cc-by) |

# Description 

This dataset from the World Bank tracks the share of renewable energy in total
final energy consumption, presented as a percentage. It highlights global and regional trends
in transitioning to renewable energy sources. Includes country-level data on renewable
energy consumption as a percentage of total energy use from 1960 to recent years. Co2 dataset provides per capita CO₂ emissions by Latin Americans region,
showcasing historical trends in carbon dioxide emissions across different geographical areas.
It helps in understanding regional contributions to global emissions and monitoring progress
toward climate goals. Regional data on CO₂ emissions measured in metric tons per capita over
multiple decades.|To answer the question,("Does consumption of renewable energy sources decreases the Co2 emission?") two data sources have been selected for this project: The world Bank,
which shows yearly information on Latin Americans renewable energy consumption, and Our
World in Data, which shows the Co2 emissions from Latin American countries.



## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Dataset selection
2. Building an Automated Data Pipelines
3. Automated Testing
4. Continuous Integration
5. Feature Engineering and Analysis
6. Reporting on findings
7. Presentation


## Steps to run pipeline

This pipeline will run the programmed ETL and save the required data sources for the analysis/study in `\data` directory. There should be 4 datasets ***demand.csv, emission.csv, generation.csv, and world_gdp.csv***

- [ ] Clone the project using SSH
```
  git clone git@github.com:Jovinjo/made-Ramrachai-Marma.git
```

- [ ] Go to the main directory
```
  cd made-Ramrachai-Marma
```

- [ ] Run the Pipeline bash script
```
  bash project/pipeline.sh
```

## Test environment

Test environment also provided to ensure that the ETL functions properly.

```
  bash project/tests.sh
```

A Github Action has been created at [CI](https://github.com/Ramrachai-Marma/made-Ramrachai-Marma/blob/main/.github/workflows/test.yml) .This allows to execute the test on every push to the main branch.
To get started, please follow these steps:
1. Create your own fork of this repository. Feel free to rename the repository right after creation, before you let the teaching instructors know your repository URL. **Do not rename the repository during the semester**.
2. Setup the exercise feedback by changing the exercise badge sources in the `README.md` file following the patter `![](https://byob.yarr.is/<github-user-name>/<github-repo>/score_ex<exercise-number>)`. 
For example, if your user is _myuser_ and your repo is _myrepo_, then update the badge for _exercise 1_ to `![](https://byob.yarr.is/myrepo/myuser/score_ex1)`. Proceed with the remaining badges accordingly.


## Project Work
Your data engineering project will run alongside lectures during the semester. We will ask you to regularly submit project work as milestones so you can reasonably pace your work. All project work submissions **must** be placed in the `project` folder.

### Exporting a Jupyter Notebook
Jupyter Notebooks can be exported using `nbconvert` (`pip install nbconvert`). For example, to export the example notebook to html: `jupyter nbconvert --to html examples/final-report-example.ipynb --embed-images --output final-report.html`


## Exercises
During the semester you will need to complete exercises using [Jayvee](https://github.com/jvalue/jayvee). You **must** place your submission in the `exercises` folder in your repository and name them according to their number from one to five: `exercise<number from 1-5>.jv`.

In regular intervalls, exercises will be given as homework to complete during the semester. Details and deadlines will be discussed in the lecture, also see the [course schedule](https://made.uni1.de/). At the end of the semester, you will therefore have the following files in your repository:

1. `./exercises/exercise1.jv`
2. `./exercises/exercise2.jv`
3. `./exercises/exercise3.jv`
4. `./exercises/exercise4.jv`
5. `./exercises/exercise5.jv`

### Exercise Feedback
We provide automated exercise feedback using a GitHub action (that is defined in `.github/workflows/exercise-feedback.yml`). 

To view your exercise feedback, navigate to Actions -> Exercise Feedback in your repository.

The exercise feedback is executed whenever you make a change in files in the `exercise` folder and push your local changes to the repository on GitHub. To see the feedback, open the latest GitHub Action run, open the `exercise-feedback` job and `Exercise Feedback` step. You should see command line output that contains output like this:

```sh
Found exercises/exercise1.jv, executing model...
Found output file airports.sqlite, grading...
Grading Exercise 1
	Overall points 17 of 17
	---
	By category:
		Shape: 4 of 4
		Types: 13 of 13
```

## Further Links


- Link to the Final Report: [analysis-report.pdf](https://github.com/Ramrachai-Marma/made-Ramrachai-Marma/blob/main/project/Analysis_Report__.pdf)
- Link to the Data Quality Report: [data-report.pdf](https://github.com/Ramrachai-Marma/made-Ramrachai-Marma/blob/main/project/Data%20Report.pdf)

HAVE FUN! :smile:

# Exercise Badges

![Ex1](https://img.shields.io/badge/Ex1-100.0%25-green) 
![Ex2](https://img.shields.io/badge/Ex2-100.0%25-brightgreen) 
![Ex3](https://img.shields.io/badge/Ex3-100.0%25-yellow) 
![Ex4](https://img.shields.io/badge/Ex4-100.0%25-blue) 
![Ex5](https://img.shields.io/badge/Ex5-100.0%25-REd)

=======


 
>>>>>>> 0c94c3f6c2af37d576cdcfc76d29967aca0b1448
