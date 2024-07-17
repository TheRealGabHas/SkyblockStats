# Skyblock Stats

![Skyblock Stats](templates/assets/images/favicon.png)

## Description

This project has been inspired by [SkyCrypt](https://github.com/SkyCryptWebsite/SkyCrypt). The goal is to provide a 
user-friendly interface to the Hypixel Skyblock API. This website retrieves Skyblock player's data based on a given 
username. 

The retrieved data are for the latest played profile.

This project doesn't have any grand ambitions, it's just for fun and training.

## Technologies

- [Python 3.12+](https://python.org)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/en/2.10.x/)

**Note:** This project utilize some feature from Python 3.12 (like some f-string shenanigans) that could be easily 
adapted for older version of Python.

## API Key

The Hypixel API key must go in the `stats_gather/credentials.json` file following this format : 
```json
{
    "API-Key": "00000000-0000-0000-0000-000000000000"
}
```
**Note:** You must create this file.

## Files and folders

The project is composed of several folders:
- [`stats_gather`](stats_gather) : Contains the Python file that gather and prepare the data that will be used in the 
templates
- [`templates`](templates) : Contains all the Jinja2 templates and web resources (images, stylesheets...)

The [`main.py`](main.py) file runs the web server, references the routes and send the data to the Jinja2 templates.