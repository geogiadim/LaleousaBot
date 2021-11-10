# LaleousaBot

### About 
___
This is a discord music bot that plays music from YouTube in discord voice channels.
- Follow the [installation guide](#installation-guide)
- After install [requirements](#requirements)
- Then [connect this bot with your Discord Application](#connect-this-bot-with-your-discord-application)
- Finally, [run](#run) this bot!!!

### Installation Guide 
___

1. Fork this project.
2. Clone this repository into a directory on your local machine.
3. Install a python virtual environment inside your new directory
    ```
    $ pip install virtualenv
    $ virtualenv -p python3 venv
    ```
    For Linux or Mac OS
    ```  
    $ virtualenv venv 
    ```
    For Windows
    ```
    $ virtualenv -p python3 venv
    ```
   
4. Activate the installed venv using below commands  
    For Linux:
    ```
    $ . venv/bin/activate
    ```
    For Windows:
    ```
    $ venv\Scripts\activate
    ```
  
### Requirements 
___
In the project directory, install the required packages inside your activated ```venv``` using
```
$ pip install -r requirements.txt
```

### Connect this bot with your Discord Application
___
Create a Bot from the [Discord Developer Portal](https://discord.com/developers/docs/intro), generate a Bot Token and copy to your clipboard the Bot token.  
Then create a ```.env``` file and paste the Token.
```
TOKEN = "Bot token here" 
```
### Run
___
In order to run this Discord Bot run below command inside your activated ```venv```
```
$ python app.py
```

### Bot Commands
___

Bot's prefix is ```?```  

| Command | Description |
|---------|-------------|
|join | Connects to a voice channel |
|play "youtube_url or query" | Adds in queue or plays the song given by YouTube url or query|
|skip| Skips the current music track|
|q| Prints music queue|
|cq| Clears music queue|
|pause| Pause playing music|
|resume| Resume playing music|
|leave| Disconnects from the voice channel|