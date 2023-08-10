# TalkingGame
An oTree game developed for the purpose of getting participants to communicate with each other. 


## Dependencies
- OTree: https://www.otree.org/

## How to run
Currently only the demo can be run. To run a devserver, cd into the [Otree Project Folder](MatchingFigures/), then run
```sh
otree devserver
```
Open [the link](http://localhost:8000) as prompted, click on either the session link or the single-use links. 
The page should like something like [this](https://github.com/moyasui/TalkingGame/blob/main/Demo/Figure%20Matching%20Game.html).

## Deployment
In your terminal, cd into this git repository, then 
```sh
cd MatchingFigures
```
```sh
otree zip
```
You should get something like:
```sh
Saved your code into file "MatchingFigures.otreezip"
```
Go to
[Otreehub](https://www.otreehub.com/my_projects/)
Click **upload** then choose the .otreezip file. 

### Create Sessions
If you don't create a session, demo version will be run with all the debug infomation. 
Go to Sessions, click **Create new session**. Create a new session for **EVERY EXPERIMENT**. 

