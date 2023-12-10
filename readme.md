# Discord Bot Template

## Overview

This project demonstrates a modular application structure using the concept of 'cogs', which are portable and
compartmentalized parts of the app. Each cog represents a distinct piece of functionality, making the application easy
to maintain and extend.

The application is Docker-ready, with a Dockerfile for building the Docker image and a docker-compose.yaml.

### Pre-commit Hooks

The project uses pre-commit hooks to maintain code quality. These hooks, defined in .pre-commit-config.yaml, automate
tasks like code formatting, linting, and more, ensuring that all commits meet the project's coding standards

## Getting Started

### Setting Up the Environment

You will need an API key for your app. Follow instructions [here](https://discord.com/developers/docs/getting-started)
to get started. This app is configured to expect "all intents", which is generally fine for a personal project but not
appropriate for a production app. Once you have an API key:

- Copy the `.env.example` file to a new file named `.env`
- Add your API key to the `.env` file

### Building and Running with Docker

To build and run the application using Docker:

```shell
docker-compose up
```

### Pre-commit

If you like, this project contains a boilerplate pre-commit configuration that will run code quality checks on every
commit. To use:

- Install pre-commit on your local machine. Follow the instructions [here](https://pre-commit.com/#install)
- Run `pre-commit install` in your project directory install to set up the git hook scripts

## Extending the Project

### Adding New Cogs

To add a new cog:

- Create a new directory in the root of the project, e.g. `./my-cog`
  - Create `./my-cog/cog.py` and `./my-cog/models.py` in the new directory
- Implement your cog following the structure shown in `example/cog.py`

```python
# ./my-cog/cog.py
...
class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Define your additionaly commands here

# Must include this line at the bottom so that the cog loads
def setup(bot):
    bot.add_cog(MyCog(bot))
```
- Register the new cog in config.py under the COGS list
```python
# ./config.py
...
# Define attached cogs here
COGS = [
    "example",
    "my-cog"
]
```

### Database Extension

The application uses a Peewee ORM for database interactions, as shown in `./database.py`. Peewee is a simple, file based
database that is not suitable for production use, but more than adequate for simple applications. To extend the
database simply add your models to `./my-cog/models.py`. They will be automatically loaded and registered when you app
is initialized.

```python
# `./my-cog/models.py`
import peewee

from database import BaseModel


class MyModel(BaseModel):
    text = peewee.CharField(null=False)
    big_int = peewee.BigIntegerField(null=False)
```
