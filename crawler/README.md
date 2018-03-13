## Data Description

* <code>reviews_dta</code>: contains all reviews we scraped from tripadvisor for 189 
attractions that have the total number of reviews > 1000. 

* <code>Attractions.json</code>: the geometrical information we requested from Google
Map API for 10055 attractions.

* <code>final_data1</code>: the dataset we import in Django which contains geometrical 
info for 8000+ attractions and reviews for 189 attractions. 

* <code>att_csv</code>: contains the attractions that we scraped their reviews and their
url in tripadvisor. 

* <code>category.csv</code>: contains the category (first column) we mannually summarized
from all the phrases we obtained after training our NLP models. For each row, from the 
second column to the end are the phrases we defined to belong to the category in the first
column. 

* <code>classify.csv</code>: contains the classification of attractions according to the 
category.csv file. As long as the review of an attraction contains at least one phrase belongs
to a category, we define that the attraction belongs to this category. 

* <code>merged_attrs.json</code>: the dataset we obtained after mergeing all the 189 json 
files in <code>reviews_dta</code>. 

* <code>attr_match_phrs.json</code>: the dataset that contains the phrases appeared in each
attractions and its number of occurrance. 


## For crawler.py, click.py 
* The data were collected around one month ago. By the time we did our final presentation, we
have successfully demonstrated how our crawler works. However, we found out that this crawler
function cannot work as expected on the submission date due to the modification of tripadvisor 
website. We feel appologized if you are unable to check our function implementation or
replicate our result. 
