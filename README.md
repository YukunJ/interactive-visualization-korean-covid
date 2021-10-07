# Project Writeup
#### Yukun Jiang 
##### yukunj@cs.cmu.edu

Current Deployment link: https://share.streamlit.io/yukunj/interactive-visualization-korean-covid/main/korean_covid.py

### Project Overview

Mankind has been fighting against Covid-19 Virus for almost two years. Major attention has been put on the Europe, North America and East China. However, there are many countries that are less reported and noticed, and yet stuck in the spiral of the virus. In this project, we will focus on **South Korean** and analyze how it copes with the Covid-19 virus and how severe is the situation there using different kinds of exploratory analysises and interactive visualizations. 

In specific, through our analysises and visualizations, we aim to enable readers to answer, or at least spark thoughts upon, the following questions:

> 1. how widely are infections spread in the South Korean?
> 2. Is the virus situation there getting better or worse?

The answers to these two questions are critical in understanding the South Korean's **medical preparedness** and **governmental virus-related decisions and enforcements**.

### Design Rationale

To be able to answer the following two questions, we actually decide to cut our analysis into 2 dimensions:

+ **Spatially**: from the geographical distribution, is there any particular infection pattern?
+ **Temporally**: using time series analysis, what is the trend of infection? Is there snowball effect?

we used `Streamlit` as the web deployment framework. There are actually quite a number of alternatives suitable for aforementioned questions, for example scatter plot and histogram were once very appealing to our design. However, after browsing through the gallery, we decided to use

> **Mapping** for spatial analysis since it gives the best geographical distribution display and relative displacement between different cities and infection numbers.

> **Animated Time Series Plotting** for temporal analysis as it provides a "walkthrough" of a period of time in the past to see how the infection trend evolves as time goes.

### Development Process

This is a solo project. 
First of all, we adopted the [dataset](https://www.kaggle.com/kimjihoo/coronavirusdataset) from Kaggle. It comprises of around 4000 infection cases in South Korean from Jan 2020 to June 2020. We believe it's of good quality as it has been published *in proceedings of NeurIPS 2020*, arguably one of the most influential conferences on the topic of Data Science.

+ A great proportion of time was spent on exploratory data analysis and data cleaning. The code is always provided in the folder, named "Preprocessing.ipynb". Many data rows have missing values, either because the staff could not collect them, or due to privacy concerns. 

+ For the spatial visualization, to use a mapping, we have to manually search and get the longitude and latitude of each province and city, which is quite time-consuming overall. 

+ For the temporal visualization, we need to be able to manipulate the datetime object and do increment/decrement accordingly, and calculate the presum vectors of target statistics. 

+ For the Streamlit web application development, since it's the first time we use this framework, it took a while to get ourselves familiar with it and walked through a few demos to know the common APIs.

In total, we probably spent 11 hours in total on this assignment, 4 hours on exploratory data analysis and cleaning, 6 hours of learning the Streamlit and developing the web application and 1 hour for GitHub deployment.
