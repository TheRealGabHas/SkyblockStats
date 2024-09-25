# Skyblock Stats

<p align="center">
  <img src="src/templates/assets/images/favicon.png" alt="Skyblock Stats">
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

> <img src="https://skillicons.dev/icons?i=docker"/> 
>
>This web application can also be deployed with [Docker](https://docker.com),
see the [docker deployment](#docker-deployment-recommended) section.


## Configuration file and API Key

The project configuration file is `config/settings.json`. It must be manually created and follow this format :
The Hypixel API key must be replaced with a real one.
A copy of this configuration can be found in [`config/default_settings.json`](src/config/default_settings.json).
```json
{
  "hypixel-api-key": "00000000-0000-0000-0000-000000000000",
  "redis": {
    "host": "localhost",
    "port": 6379,
    "cache-retention-duration": 300
  },
  "logging": {
    "enabled": false,
    "log-file-path": "/dev/null"
  }
}
```
**Note:** You must create this file.

## Deployment

### Docker deployment (recommended)

To deploy this project with Docker, one must have installed Docker on the machine.
Installation instructions can be found at [get.docker.com](https://get.docker.com).

The first step is to clone the project:
```shell
git clone https://github.com/TheRealGabHas/SkyblockStats .
```

You should now create the `src/config/settings.json` file based on 
[`src/config/default_settings.json`](src/config/default_settings.json) and paste your Hypixel API key in it:
```shell
cp src/config/default_settings.json src/config/settings.json
```

The `src/config/settings.json` file should look like this:
```json
{
  "hypixel-api-key": "00000000-0000-0000-0000-000000000000",
  "redis": {
    "host": "skyblockstats-database",
    "port": 6379,
    "cache-retention-duration": 300
  },
  "logging": {
    "enabled": false,
    "log-file-path": "/dev/null"
  }
}
```

Then run the following command from the folder containing [`compose.yaml`](compose.yaml):
```shell
docker compose -p skyblockstats up -d
```
Here is a breakdown of the command:
- `docker compose up`: Creates and starts containers based on the [`compose.yaml`](compose.yaml) file.
- `-p skyblockstats`: Specifies the project name (optional)
- `-d`: Run containers in the background (optional)

In this case, 2 containers will start running :
- `skyblockstats-database`: The Redis database
- `skyblockstats-app`: The Python web application

At this point, accessing `http://127.0.0.1:8000` should display the web application.

<hr>

### Manual deployment

**Note:** A Redis database must be up and running in order for the project to run. 
(The connection can be configured in the `src/config/settings.json` file created as specified 
in [this section](#configuration-file-and-api-key))

**Note:** Make sure that Python 3.12+ is already installed on the machine.

To run the project, the first step is to clone the repository :
```shell
git clone https://github.com/TheRealGabHas/SkyblockStats
```

Install the dependencies required to run the project :
```shell
pip install -r src/requirements.txt
```

You should now create the `src/config/settings.json` file based on 
[`src/config/default_settings.json`](src/config/default_settings.json) and paste your Hypixel API key in it:
```shell
cp src/config/default_settings.json src/config/settings.json
```

**Note:** Make sure to change the `host` value in the `redis` section to `localhost`.

The `src/config/settings.json` file should look like this:
```json
{
  "hypixel-api-key": "00000000-0000-0000-0000-000000000000",
  "redis": {
    "host": "localhost",
    "port": 6379,
    "cache-retention-duration": 300
  },
  "logging": {
    "enabled": false,
    "log-file-path": "/dev/null"
  }
}

```
Finally, use uvicorn to run the server :
```shell
python -m uvicorn main:app --reload --no-server-header
```
- `--reload`: Allows hot reload without restarting the whole server on modification. (optional)
- `--no-server-header`: Removes information about the server from the request header (Apache, Nginx...). (optional)

At this point, accessing `http://127.0.0.1:8000` should display the web application.

### Changing the ports

#### Docker

The server will run by default on the port 8000. This value can be edited in the [`compose.yaml`](compose.yaml) by 
changing the ports settings in the following part :
```yaml
app:
  build: .
  ports:
    - "8000:8000"
  volumes:
    - "./src/config:/app/config"
  network_mode: host
```
Here is an example of running the application on the port `1234`:
```yaml
  ports:
    - "1234:8000"
```

You can also change the port used by Redis in the [`compose.yaml`](compose.yaml) the same way. But you will also need to
update it in the `src/config/settings.json` file:
```json
{
  "redis": {
    "host": "skyblockstats-database",
    "port": 6379,
    "cache-retention-duration": 300
  }
}
```

#### Manual

The server will run by default on the port 8000. This value can be edited with the `--port [INTEGER]` parameter.
Here is an example of the launch command for the port 1234:
```shell
python -m uvicorn main:app --no-server-header --port 1234
```

For more information, see the list of all the uvicorn [command line options](https://www.uvicorn.org/#command-line-options).

If you Redis database is running on a non-default port (not 6379), you should edit the `src/config/settings.json` file:
```json
{
  "redis": {
    "host": "localhost",
    "port": 6379,
    "cache-retention-duration": 300
  }
}
```
**Note:** Make sure to change the `host` value in the `redis` section to `localhost`.

### Example of reverse proxy

For security purpose, consider using a reverse proxy. Here is minimal example with Apache2 :
```bash
<VirtualHost *:443>
    ServerName skyblock.my-website.com
    
    RewriteEngine On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>
```


### Logging

To enabled request logging, the `enabled` value in the `config/settings.json` must be set to `true` as show here:
```json
{
  "hypixel-api-key": "00000000-0000-0000-0000-000000000000",
  "redis": {
    "host": "localhost",
    "port": 6379,
    "cache-retention-duration": 300
  },
  "logging": {
    "enabled": true,
    "log-file-path": "/dev/null"
  }
}
```

**Note:** The `log-file-path` must also be changed to a valid file. Permissions must be configured so that the program
can write in this file.


## Files and folders

All the code relevant to the project itself is located in the [`src`](src) folder. However, some files have been created
to make the development and deployment of this application easier :
- `.gitignore`: Specifies which files must be ignored and therefor shouldn't be in the public repository.
- `LICENSE`: Specifies the license that rules the project. (Apache2)
- `README.md`: A guide full of information about this project. (involved technologies, deployment, goals...)
- `Dockerfile`: A set of instructions to build a container that runs the Python web application.
- `compose.yaml`: A file that defines what containers to create and how to run them. 

The project is composed of several folders:
- [`stats_gather`](src/stats_gather) : Contains the Python file that gather and prepare the data that will be used in the 
templates
  - [`consts.py`](src/stats_gather/consts.py) : A Python file containing a lot of game constants (XP levels, items names...)
  - [`data_pickup.py`](src/stats_gather/data_pickup.py) : The file that collects every data and format it before sending 
  it to the template.
  - [`s_utils.py`](src/stats_gather/s_utils.py) : Some utility functions in Python
  - `settings.json` : JSON file in which the API-Key must be filled (must be created manually, 
  see [this section](#configuration-file-and-api-key))
  - [`miscellaneous`](src/stats_gather/miscellaneous) : A folder that will store some utility scripts and assets.
  
- [`templates`](src/templates) : Contains all the Jinja2 templates and web resources (images, stylesheets...)

The [`main.py`](src/main.py) file runs the web server, references the routes and send the data to the Jinja2 templates.

The Python packages requirements are listed in the [`requirements.txt`](src/requirements.txt) file. They can be installed 
with :
```shell
python -m pip install -r requirements.txt
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

- [x] Add Chocolate Factory stats viewer
  - [x] Make it responsive
  - [x] Add the rabbit list (can be toggled and sorted)
  - [x] Add the chocolate per second rate
- [x] Add profile selector
- [x] Add icon for every field
- [x] Add and complete a page about user data, credits, legals...
- [x] Implement a caching system with a 5 minutes caching duration
- [ ] Take skill level cap into account (Runecrafting, Taming, Foraging...)
- [ ] Read items from inventory and accessory bag
  - [ ] Magical power calculator
  - [x] Detect the chocolate talisman to more accurately estimate the chocolate production
- [x] Add a logging system
- [x] Perform some basic check on the user form input to prevent injection
- [x] Rework the file structure of the project to implement a "config" section

## The tooltip system

Some text are intended to display a tooltip on hover. To do so, the concept from 
[Chris Bracco](https://codepen.io/cbracco/pen/nXEQLw) is implemented. 

The tooltip-related CSS code is contained in the 
[`tooltip.css`](src/templates/assets/stylesheet/tooltip.css).

To add a tooltip to an element, add the custom attribute `data-tooltip` to the HTML tag. For instance, the following 
code displays "This is the tooltip text" when hovering the `<p>` element.
```html
<p data-tooltip="This is the tooltip text">Hello world</p>
```