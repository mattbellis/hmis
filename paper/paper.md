---
title: 'hmis: A Python tool to visualize and analyze HMIS data'
tags:
  - python
  - hmis
  - homelessness
  - homeless
  - continuum of care
  - open source
  - data visualization
  - data science
authors:
 - name: Sara Mahar
   orcid: 0000-0003-0920-3042
   affiliation: 1
 - name: Matthew Bellis
   orcid: 0000-0002-6353-6043
   affiliation: 1
affiliations:
 - name: Siena College 
date: 
bibliography: paper.bib
---


# Summary

Many organizations that work to combat homelessness receive funds from the US Department of Housing and Urban Development (HUD). 
These organizations might be overnight shelters or transitional housing or somewhere in between the Continuum of Care (CoC) provided by these groups. 
Since 2004, HUD has mandated that groups that receive these funds collect data on the homeless individuals that make use of these services. 
As such, there is a wealth of data that has been collected all over the country from a variety of organizations. 
Organizations have some freedom in how they collect and store these data, often making use of 3rd-party software solutions, 
but the data format is the same everywhere. 

This variety of data storage tools means that is is difficult for a data scientist at any of these organizations to dig into this data using standard, open-source computing tools like python or R. 
These groups can download the data in a standardized "HMIS data dump", which results in 12 separate .csv files, but this still does not make any initial analysis any easier, a priori. These files have information about individuals's name (hashed as a personal ID number), date of birth, prior living, disabilities, jail time, etc.

This module contains a suite of python functions to allow for analysis and visualization of the data collected by the various partners across the CoC. Visualization includes time-series plots, and mapping of the locations of the programs individuals have entered. Analysis can be done with these visualizations and with the ability to withdraw individuals who share a common character. For example, the analyst can withdraw all of the individuals who have visited more than 25 programs and then visualize them. 

We have developed these tools to work with the standard HMIS data dump in the RHY (Runaway and Homeless Youth) data format, that produces 12 .csv files in which personal identifying information is de-identified through a hashing algorithm. 
Because of this standardization, any other tools that leverage this software package can be used by similar networks across the country.

The definitions of the information in the HMIS data can be found [on HUD's website](https://www.hudexchange.info/programs/hmis/). This unit tests make use of definitions as of 2017. 

This software project started thanks to the help and assistance from members of [CARES NY](http://caresny.org/),
a group committed to ending homelessness and who applies for grants from HUD and administers them with
partners across the CoC. We would like to particularly acknowledge CARES members, Maureen Burns, 
Terry O'Brien, and Allyson Thiessen, who explained to us the need for tools like this and the data
formats themselves.
We also acknowledge members of the Siena College community, Ruth Kassel and Paul Thurston, for the initial connects with CARES, and their strong and continued support of this project.

# References
