# Matrix Cribbage Bot

A bot using the [matrix-nio](https://github.com/poljar/matrix-nio) that lets
you play the game of [Cribbage](https://en.wikipedia.org/wiki/Cribbage) with
friends on Matrix :)

Currently in a very early stage of development.

## Production

Install with `pip`:

```
pip install matrix-cribbage-bot
```

Generate a config file:

```
matrix-cribbage-bot -g [path/to/config.yaml]
```

Modify the config file to your liking.

Then start the bot:

```
matrix-cribbage-bot [-c path/to/config.yaml]
```

In both config generation and running the bot, it will default to `./config.yaml`.

## Development

Set up a virtual environment with Python 3.5+:

```
virtualenv -p python3 env
source env/bin/activate
```

Install the development dependencies:

```
pip install -e .[dev]
```

Generate a config file with:

```
matrix-cribbage-bot -g [path/to/config.yaml]
```

Run the bot:

```
matrix-cribbage-bot [-c path/to/config.yaml]
```

Start hacking away :)
