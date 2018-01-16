# Automated Movie Spoiler Tagging
# Comparing Character Level Deep LearningMmodels

**tl;dr:** TODO

## Intro

I'll be honest. I've  seen [Episode VIII](https://en.wikipedia.org/wiki/Star_Wars:_The_Last_Jedi), and I don't 
really care about spoilers.

However, I thought it would be interesting to train a model to determine if a post to the 
[r/StarWars](https://www.reddit.com/r/StarWars/) subreddit contained spoilers or not. More specifically, I was 
interested in comparing a few different model architectures (character embeddings, LSTM, CNN) and hyper-parameters 
(number of units, embedding size, many others) on a real world data set, with a challenging response variable. As with 
so many other things in my life, Star Wars was the answer. 

## Building

### Data Scraping
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

### Data Transformations
Once the data set was scraped from Reddit, I performed the following transformations to create the X matrix:

 - Post titles and content were joined with a single space
 - Text was lower cased
 - All character that were not in a pre-approved set were replaced with a space
 - All adjacent whitespaces were replaced with a single space
 - Start and end markers were added to the string
 - The string was converted to a fixed length pre-padded sequence, with a distinct padding character. 
 Sequences longer than the prescribed length were truncated.
 - Strings were converted from an array of characters to an array of indices
 
The y array, containing booleans, required no modification from the scraper. 

### Models

I chose to utilize a character level model, due to the large / irregular vocabulary of the data set. Additionally, this 
approach allowed me to evaluate character level model architectures I had not used before.
 
Moreover, I elected to use a character level embedding model. While a cursory analysis and past experience have 
shown little difference between an explicit embedding layer and feeding character indices directly into a dense layer, 
this makes post flight analysis of different characters and borrowing from other models easier. 

In addition to the embedding layer, I tried a few different architectures, including:

```python
    x = sequence_input
    x = embedding_layer(x)
    x = Dropout(.2)(x)
    x = Conv1D(32, 10, activation='relu')(x)
    x = Conv1D(32, 10, activation='relu')(x)
    x = MaxPooling1D(3)(x)
    x = Flatten()(x)
    x = Dense(128, activation='relu')(x)
    x = output_layer(x)
``` 
**CNN Architecture**

```python
    x = sequence_input
    x = embedding_layer(x)
    x = Dropout(.2)(x)
    x = LSTM(128)(x)
    x = output_layer(x)
```
**LSTM Architecture**

```python
    x = sequence_input
    x = embedding_layer(x)
    x = Dropout(.2)(x)
    x = Conv1D(32, 10, padding='valid', activation='relu')(x)
    x = Conv1D(32, 10, padding='valid', activation='relu')(x)
    x = MaxPooling1D(3)(x)
    x = LSTM(128)(x)
    x = output_layer(x)
```
**CNN, followed by LSTM architecture**

Though these architectures (and many variations on them) are common in literature for character models, I haven't seen 
many papers suggesting hyper-parameters, or guidance for when to use one architecture over another. This data set has 
proven to be a great opportunity to get hands-on experience.  

### Training

Due to the lengthy train time for LSTM models, I utilized a few p3.2xlarge EC2 instances (I had some free credits to 
burn). Model training wasn't too awful, with 300 epochs clocking in at a few hours for the deepest / widest models 
evaluated (~$12 / model).

Because I was exploring a wide variety models, I wasn't quite sure when each model would overfit. Accordingly, I set 
each model to fit for a large number of epochs (300), and stopped training each model when validation loss consistently 
increased. For the CNN model this was pretty early at around 9 epochs, but the LSTM models took considerably longer to 
saturate.  

## Wrap up

Overall, the models performed better than random, but more poorly than I expected:

| Model    | Validation loss | Epoch | Comment                    |
|----------|-----------------|-------|----------------------------|
| cnn      | 0.24            | 22    |                            |
| cnn lstm | 0.38            | 164   |                            |
| lstm     | 0.36            | 91    | Noisy loss over time graph |

It would appear that good ol' fashioned CNN models not only outperformed the LSTM model, but also outperformed a CNN / 
LSTM combo model. In the future, it would be great to look at bi-directional LSTM models, or a CNN model with a much 
shallower LSTM layer following it. 

### Future work

In addition to trying additional architectures and a more robust grid search of learning rates / optimizers, it would 
be interesting to compare these character level results with word level results. 

Additionally, it could be fun to look at a smaller time window; the 400 day window I looked at for this work actually 
a minor Star Wars movie and a major Star Wars movie. Additionally, it included a long period where there wasn't much 
new content to be spoiled. A more appropriate approach might be to train one model per spoiler heavy event, such as a 
single new film or book.

Moreover, the r/StarWars subreddit has a fairly unique device for tagging spoiler text within a post, utilizing a 
`span` tag. During a coffee chat, John Bohannon suggested it could be possible to summarize a movie from spoilers about 
it. This idea could take some work, but it seems readily feasible. I might propose a pipeline like:

 - Extract spoiler spans from posts. These will be sentence length strings containing some spoiler
 - Filter down to spoilers about a single movie
 - Aggregate spoilers into a synopsis

### Resources

As always, code and data are available on GitHub, at 
[https://github.com/bjherger/spoilers_model](https://github.com/bjherger/spoilers_model). Just remember, the best 
feature requests come as PRs. 