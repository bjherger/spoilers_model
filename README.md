# Spoilers model

**tl;dr:** Determining which Reddit posts contain Star Wars spoilers, using a series of character level deep learning 
models. 

## Getting started

### Repo structure
 - `bin/main.py`: Code entry point
 - `conf.yaml.template`: Configuration file
 - `docs/results`: Serialized, pre-trained models
 - `bin/reddit_scraper.py`: A reddit scraper

### Python Environment
Python code in this repo utilizes packages that are not part of the common library. To make sure you have all of the 
appropriate packages, please install [Anaconda, for Python 2](https://www.continuum.io/downloads), and install the environment 
described in environment.yml (Instructions [here](http://conda.pydata.org/docs/using/envs.html)). 

### To run code
  
To run the Python code, complete the following:
```bash

# Install anaconda spoilers
conda env create -f environment.yml 

# Activate environment
source activate spoilers

# Run script
cd bin/
python main.py
```

This will train a model using a serialized (already scraped data set). These models can take hours to run on expensive 
GPUs; I'd highly suggest setting the `test_run` flag to `true` in `confs.yaml` during any development work. 

### Configuration file


### Confs

This application has a number of configurations that can (and should) be modified. Please use the commands below to set up the 
configs:

```bash
# Create configuration file
cp conf/confs.yaml.template conf/confs.yaml

# Fill out confs (This requires work on your end!)
open conf/confs.yaml
```

A few interesting configurations to be aware of:

 - `test_run`: If true, the app will randomly sample a small number of observations from the data set. This is great 
 for testing features before big data runs
 - `new_data_pull`: If true, the app will attempt to scrape a new data set from Reddit. Setting this flag to true 
 requires `client_secret` and `client_id` to be set. 
 - `client_secret` and `client_id`: Credentials for a [Reddit bot](https://github.com/reddit/reddit/wiki/OAuth2). 


## Contact
Feel free to contact me at 13herger `<at>` gmail `<dot>` com
