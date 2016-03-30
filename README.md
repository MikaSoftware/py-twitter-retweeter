# py-twitter-retweeter
## Description
A python script which retweets tweet with specific hashtags to a twitter account.

## Features
* Get the latest tweets using Twitter Stream API
* Re-tweet tweets specific text and hashtags

## System Requirements
* Python 3.4.x+
* pip 6.1.1+
* virtualenv 12.1.1+

## Dependencies
* tweepy 3.5.0

## Build Instructions
1. First clone the project locally and then go into the directory

  ```bash
  git clone https://github.com/MikaSoftware/py-twitter-retweeter.git
  cd py-twitter-retweeter
  ```


2. Setup our environment:

  ```bash
  (OSX)
  python3 -m venv env

  (Linux/FreeBSD)
  virtualenv env
  ```


3. Activate "virtualenv" for this script:

  ```bash
  source env/bin/activate
  ```


4. Confirm we are using Python3

  ```bash
  python --version  # Should return Python 3.x
  ```


5. Now let's install the required libraries:

  ```bash
  pip3 install -r requirements.txt
  ```
  
  
6. Bugfix an error with **tweepy** by reading the instructions here: https://github.com/tweepy/tweepy/issues/615


7. Go to http://apps.twitter.com and create an app. Once finished, be sure to make a copy of the following data:
  * Consumer Key
  * Consumer Secret
  * Access Token
  * Access Secret


8. Go into the source folder and change the **secret_settings.py** file by entering the values you saved from step (5).

  ```bash
  cp src/secret_settings_example.py src/secret_settings.py
  vi src/secret_settings.py
  ```

9. Replace the values with your *Twitter API Keys/Tokens*.



### Usage
To run the application, simply enter the following line:

  ```bash
  python retweeterbot.py
  ```


## License
BSD 


## Donate
* Bitcoin: 17VEy2fps6nJCUhWsvhJ4h42omWMJZUjcm
