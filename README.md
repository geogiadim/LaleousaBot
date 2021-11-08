# LaleousaBot

### About 
___
This is a discord music bot that plays music from YouTube in discord voice channels.

### Installation Guide 
___

- Clone this repository into a directory.
- Open your terminal (for linux) or cmd (for windows) inside the new directory.
- Install a python virtual environment inside your new directory:
  ```
  $ pip install virtualenv
  $ virtualenv -p python3 venv
  ```
  For linux:
  ```  
  $ virtualenv venv 
  ```
  For windows:
  ```
  $ virtualenv -p python3 venv
  ```
- Activate the installed venv:
  <br><br>For Windows:
  ```
  $ venv\Scripts\activate
  ```
  For Linux:
  ```
  $ . venv/bin/activate
  ```
  
### Requirements 
___
In the project directory, install the packages using:
```
pip install -r requirements.txt
```
### Run
___
In order to run this Bot run below command inside your activated venv:
```
$ python main.py
```

### Bot Commands
___

Join in a voice channel and play given YouTube url:
```
?play "youtube_url"
``` 

Resume playing music:
```
?resume
``` 

Pause playing music:
```
?pause
```

Disconnect from the voice channel: 
```
?leave
```
