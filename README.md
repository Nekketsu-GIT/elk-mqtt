# elk-mqtt
## Goal

This is an example project how to manage an iot stack for predictive maintenance. We use a dataset containing data of machines sent by sensor, some machine fail. Our goal is to understand the data, in order to predict machine failure.
You can find in file that describe our dataset.
You can use this project with othe dataset and little understanding of the code.
To achieve it we use Docker, elastic and mqtt. Our script simulate sensors sending data continuously

## prerequists

- Docker
- Python

## Setup

  ### Part 0: Resample dataset, create virtualenv
  
  Our dataset have a little problem, it suffers a lack of data with machine failure at true. But don't worry there are some ways to handle it, we use upsampling method.
  So a script is created to obtain a new dataset. To run it:
    - Run `python -m venv env`
    - Run `.\env\Script\activate`
    - Run `pip install -r requirements.txt`
    

    
  ### Part 1: Collect data and train our model
  
  #### 1. Start docker and up containter
  - Open a terminal and run `docker-compose-up`

  #### 2. Run our publisher
  - Open a new terminal
  - Run `.\env\Script\activate` , Use source command in linux
  - Open mqtt_publisher file, uncomment line that publish into sensor-data, and comment the other line
  - Inside the last terminal, Run `python mqtt_publisher.py`

  #### 3. Create our model
  - After few time, our index should contain enough data. So go in kibana at localhost:5601, in machine learning section, setup our model and start it. There will be some setup to do...


  ### Part 2: Predictive maintenance flow
    
  #### 2. Run subscriber.py
  - Open a new terminal
  - Run `.\env\Script\activate` , Use source command in linux
  - Inside the terminal, Run `python subscriber.py`
    
    
