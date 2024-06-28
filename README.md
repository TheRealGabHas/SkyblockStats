# Skyblock Stats

![Skyblock Stats](templates/assets/images/favicon.png)

## Description

This project has been inspired by [SkyCrypt](https://github.com/SkyCryptWebsite/SkyCrypt). The goal is to provide a 
user-friendly interface to the Hypixel Skyblock API. This website retrieves Skyblock player's data based on a given 
username. 

The retrieved data are for the latest played profile.

This project doesn't have any grand ambitions, it's just for fun and training.

## Technologies

- FastAPI
- Jinja2 Templates

## API Key

The Hypixel API key must go in the `stats_gather/credentials.json` file following this format : 
```json
{
    "API-Key": "00000000-0000-0000-0000-000000000000"
}
```
**Note:** You must create this file.