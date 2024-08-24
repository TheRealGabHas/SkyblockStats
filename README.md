# Skyblock Stats

<p align="center">
  <img src="templates/assets/images/favicon.png" alt="Skyblock Stats">
</p>

## Description

This project has been inspired by [SkyCrypt](https://github.com/SkyCryptWebsite/SkyCrypt). The goal is to provide a 
user-friendly interface to the Hypixel Skyblock API. This website retrieves Skyblock player's data based on a given 
username. 

The retrieved data are for the latest played profile.

This project doesn't have any grand ambitions, it's just for fun and training.

## Technologies

This website is built with FastAPI in Python 3.12. A route is created for each page and a filled Jinja2 template is 
returned as an HTML document. The retrieved data are cached for a default period of 5 minutes to save up some internet 
traffic and shorten the page loading time.

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,fastapi,redis,html,css,javascript"/>
  </a>
</p>

- [Python 3.12+](https://python.org)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/en/2.10.x/)
- [Redis](https://redis.io/)

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

## Deployment

**Note:** A Redis database must be up and running in order for the project to run. 
(The connection can be configured on line 21 of the [`main.py`](main.py) file)

To run the project, the first step is to clone the repository :
```shell
git clone https://github.com/TheRealGabHas/SkyblockStats
```

Install the dependencies required to run the project :
```shell
pip install -r requirements.txt
```

The use uvicorn to run the server :
```shell
python -m uvicorn main:app --reload --no-server-header
```
- `--reload`: Allows hot reload without restarting the whole server on modification.
- `--no-server-header`: Removes information about the server from the request header (Apache, Nginx...).

The server will run on the port 8000. This value can be edited with the `--port [INTEGER]` parameter. 
For more information, see the list of all the [command line options](https://www.uvicorn.org/#command-line-options).

For security purpose, consider using a reverse proxy. Here is minimal example with Apache2 :
```bash
<VirtualHost *:443>
    ServerName skyblock.my-website.com
    
    RewriteEngine On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>
```

## Files and folders

The project is composed of several folders:
- [`stats_gather`](stats_gather) : Contains the Python file that gather and prepare the data that will be used in the 
templates
  - [`consts.py`](stats_gather/consts.py) : A Python file containing a lot of game constants (XP levels, items names...)
  - [`data_pickup.py`](stats_gather/data_pickup.py) : The file that collects every data and format it before sending 
  it to the template.
  - [`s_utils.py`](stats_gather/s_utils.py) : Some utility functions in Python
  - [`credentials.json`](stats_gather/credentials.json) : JSON file in which the API-Key must be filled 
  (see [API Key](#api-key))
  
- [`templates`](templates) : Contains all the Jinja2 templates and web resources (images, stylesheets...)

The [`main.py`](main.py) file runs the web server, references the routes and send the data to the Jinja2 templates.

The Python packages requirements are listed in the [`requirements.txt`](requirements.txt) file. They can be installed 
with :
```shell
python -m pip install requirements.txt
```

## Bug reporting guide

To report a bug, one must open an issue and fill in the following information :

- Reported behavior : What is the website actually doing
- Expected behavior : What the website should be doing
- Step to reproduce the bug
- Other information (only if relevant)

## Style guidelines

When editing and contributing to the project, one must follow these few rules:
- **Jinja2 template**
  - Indentation should be 4 spaces
  - Quotes contained in HTML tags should be double quotes
  - Quotes contained in Jinja2 expression should be single quote

- **CSS**
  - Indentation should be 4 spaces
  - Quotes should be double quotes

- **JavaScript**
  - Indentation should be 4 spaces
  - Quotes should always be double quotes

- **Python**
  - Indentation should be 4 spaces
  - Quotes should always be double-quotes except in dictionary access (for instance: `my_dict['key']`)

- **README**
  - Indentation should be 2 spaces

## Goals

- [ ] Add Chocolate Factory stats viewer
  - [x] Make it responsive
  - [ ] Add the rabbit list (can be toggled and sorted)
  - [ ] Add the chocolate per second rate
- [x] Add profile selector
- [x] Add icon for every field
- [x] Add and complete a page about user data, credits, legals...
- [ ] Implement a caching system with a 5 minutes caching duration
- [ ] Take skill level cap into account (Runecrafting, Taming, Foraging...)

## The tooltip system

Some text are intended to display a tooltip on hover. To do so, the concept from 
[Chris Bracco](https://codepen.io/cbracco/pen/nXEQLw) is implemented. 

The tooltip-related CSS code is contained in the 
[`tooltip.css`](templates/assets/stylesheet/tooltip.css).

To add a tooltip to an element, add the custom attribute `data-tooltip` to the HTML tag. For instance, the following 
code displays "This is the tooltip text" when hovering the `<p>` element.
```html
<p data-tooltip="This is the tooltip text">Hello world</p>
```