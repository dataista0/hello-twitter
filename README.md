# hello-twitter
Playing with twitter API

# Installation

1) Make sure you have python-dev, which is required for numpy

Run `sudo apt-get install python-dev`

2) Install required packages

Run `sudo pip install -U -r requirements.txt`


3) Obtain and set twitter authentication data
Get authentication access to twitter api. Read here: dev.twitter.com/oauth/overview

Run `mv auth_data.py.example auth_data.py && vim auth_data.py`

Fill the information

4) You should download nlkt stopwords.
ipython
nltk.download()
d
stopwords


# Actually running stuff

Run `python basic.py --help`

Run `python trends.py` to enter an interface to access trending topics per world place

Run `python trends.py Berlin` to display the actual TTs in Berlin
