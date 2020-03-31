**P-BEST protocol**
================================

This package contains the basic scripts used to screen COVID-19 samples via group testing, as described in the manuscript "**Efficient high throughput SARS-CoV-2 testing to detect asymptomatic carriers**", by Shental et al.

The protocol allows screening 384 samples using 48 pools, where each sample appears in six pools according to a Reed-Solomon error-correcting code. 



## Creating the pools

Pools should be prepared using a liquid handling robot. 

As an example, the "**robotRelatedFiles**" directory provides the programming code for a Arise Ezmate-601 robot.

The experimental protocol is provided in 

Simple text files describing pooling design appear in the "**ExpData**" directory.



## Analyzing experimental results

A Matlab code is provided. In the coming days we would add a standalone version.

### Usage example

The directory "**mFiles**" contains the relevant files. We provide an example code for analyzing  results from an experiment in which two positive carriers in the 384 samples. 

PCR results appear in the file "**ExpData/ExpTwoCarriersResults.xlsx**" providing the C(t) values of each pool.

Follow the lines in "**example_PBEST.m**" file, or simply run the code,  to reconstruct the carriers.

The file contains the following parts:

a) Load the experimental data and the Reed-Solomon (RS) measurement matrix, M. 

b) Load the PCR results. 

c) Detect the carriers



**Acknowledgements**:
These scripts use a specific file taken from the GPSR package (relevant file included). 
We thank the Mario Figueiredo for allowing us to include this file in our package.

Please send any comments/bug reports to: 

Noam Shental, shental@openu.ac.il

Tomer Hertz, thertz@post.bgu.ac.il 