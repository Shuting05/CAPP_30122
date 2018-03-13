# Group Mit@U 

CAPP 30122: Computer Science with Applications-2

The University of Chicago | Winter 2018

## About this repository:
This repository contains the final course project for CAPP 30122. 

## About all sub-directories:
* <code>nlp_final</code>: contains all scripts necessary to do natural language processing

* <code>crawler</code>: contains all scripts necessary to scrape attraction informations.

* <code>mytrip</code>: contains all scripts necessary for interface created by Django.

* <code>Presentation_slides</code>: contains the presentation slides.


## Required Packages:

* Selenium (v3.11.0)
* Django (v2.0.3)
* ChromeDriver (v2.36)
* gensim (installation guideline:  https://radimrehurek.com/gensim/install.html)
* nltk: (installation guideline: http://www.nltk.org/install.html)
* googlemaps 

## How to install all required packages on **Ubuntu**:
1. Fire up a terminal, and go to the directory you want to store our program.

2. In the directory of your choice, run this command to clone the git 
 epository: <br /> 
<code>git clone https://github.com/Shuting05/CAPP_30122.git</code>

3. After cloning the git repo, you will find a new local sub-directory 
called **Project**.

4. In the home directory of **Project**, type in 
<code>sh Installation.sh</code>. 
    + After typing in this bash command, you might be asked to input the 
      password of your machine.
    + After inputting your password, Linux would start to install all required
      packages so as to ensure our program could run successfully and 
      smoothly in your machine.
    + The nltk pakeage has to be downloaded in python, so after firing up the 
      ipython3, run the following command:
      * import nltk
      * nltk.download()      
    + **Friendly Reminder**: you only need to install once, and it might 
      take about 30s to 1min to finish all required installations. 
   

## How to launch AldaCourse on **Ubuntu**:
1. Go to the home directory of **Project** in your machine and type in 
<code>sh launch_interface.sh</code>.
    + If you are a first-time user and just finished installing all packages 
following the tutorial above, you can actually just stay in the same terminal 
window and input the command <code>sh launch_interface.sh</code>.
    + **Notice**: after typing in <code>sh launch_interface.sh</code>, you will find 
the current terminal you are using could no longer input other bash command. 

2. **Open a new terminal in the same directory**, and type in 
<code>sh initialize.sh</code>. It would automatically launch your default web 
browser and you will see our amazing interface, powered by Django.

## How to use our program:
### I. 
* Once you have successfully see our interface, the first thing you 
want to do, of course, is to input the **origin** and **destination**
(anywhere in California) that you want your trip to start and end with. 

* After putting in **origin** and **destination**, click on the "GO!" button 
below. It will direct you to the second page which gives several categories of 
attractions that are along the route and you might pass by during your trip. 

* On the right panel, we provide a list of recommended attractions that ordered 
by popularity and ratings from google. Notice that by clicking each attractions, 
you will be directed to a tripadvisor webpage of that attractions. 

* You can choose whatever attractions that you find interested following the instruction
on the webpage. After clicking "submit" button, you can see an optimal route is 
displayed on the map, and the detailed travel plan is presented in the bottom. 

* You can find out our raw NLP results by clicking the links at the buttom of the 
page. You will be directed to three csv files:
  + Attractions and the key phrases found in reviews of attractions
  + Categories of phrases with their attractions
  + Attractions with their classifications and key phrases

## Contributors
**Ruxin Chen** : Contributed to crawling data, requesting data from Googlemap API, web desgin and NLP.  
[RuxinChen](https://github.com/RuxinChen)

**Shuting Chen** : Contributed to Django implementation.  
[Shuting05](https://github.com/Shuting05)

**Mengchen Shi** : Contributed to crawling data and NLP.  
[mcs2017](https://github.com/mcs2017)


We would like to express our sincere gratitude to **Prof. Anne Rogers**, 
**Mr.Nick Seltzer**, and **Mr.Kartik Singhal** for your teaching, guidance, and support throughout 
the quarter.

