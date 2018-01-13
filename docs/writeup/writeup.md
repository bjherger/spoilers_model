TODO Better title
# Spoiler or not
# Comparing Character Level Deep Learning models

**tl;dr:** TODO

## Intro

I'll be honest; I've already seen [Episode VIII](https://en.wikipedia.org/wiki/Star_Wars:_The_Last_Jedi), and I don't 
really care about spoilers.

However, I thought it would be interesting to train a model to determine if a post to the 
[r/StarWars](https://www.reddit.com/r/StarWars/) subreddit contained any spoilers or not. Really, I was interested in 
comparing a few different model architectures (character embeddings, LSTM, CNN) and hyperparameters (number of nodes, 
embedding size, many others) on a real world data set, with a challenging response variable. As with so many other 
things in my life, Star Wars was the answer. 

## Building

### Data

#### Scraping
I utilized the Reddit scraper from my [Shower Thoughts Generator](https://github.com/bjherger/Shower_thoughts_generator) 
project to scrape all post from a 400 day period. Conveniently, Reddit includes a (well policed) `spoilers` flag, which 
I utilized for my response variable. The API includes many additional fields, including:

| variable     | type   |
|--------------|--------|
| title        | string |
| selftext     | string |
| url          | string |
| ups          | int    |
| downs        | int    |
| score        | int    |
| num_comments | int    |
| over_18      | bool   |
| spoiler      | bool   |

I chose to utilize the [r/StarWars](https://www.reddit.com/r/StarWars/) subreddit, which is a general purpose subreddit 
to discuss the canon elements of the Star Wars universe. Around the time I picked up this project 
[Episode VIII](https://en.wikipedia.org/wiki/Star_Wars:_The_Last_Jedi)-- a major Star Wars film-- was released, meaning 
that there were many spoiler-filled posts.

All together, I scraped 45978 observations, of which 7511 (16%) were spoilers. This data set comprised of all visible 
posts from 2016-11-22 to 2017-12-27, a period covering 400 days.    

#### Transforming
Once the data set was scraped from Reddit, I performed the following transformations to create the X matrix:

 - Post titles and content were joined with a single space
 - Text was lower cased
 - All character that were not in a pre-approved list were replaced with a space
 - All adjacent whitespaces were replaced with a single space
 - Start and end markers were added to the string
 - The string was converted converted to a fixed length pre-padded sequence, with a distinct padding character. 
 Sequences longer than the prescribed length were truncated.
 - Strings were converted from an array of characters to an array of indices
 
The y array, containing booleans, required no modification from the scraper. 

### Models

I chose to utilize a character level model, due to the large / irregular vocabulary of the data set inherent to Star 
Wars and and internet forum (`porgs` anybody?). Additionally, this approach allowed me to evaluate character level model 
architectures I had not used before.
 

Additionally, I elected to use a character level embedding model

### Training

## Wrap up