# dhub-image-cleaner

This script will delete all but the 10 most recent tags of a Docker Hub repository.
(The number could easily be changed in the script code.)
I use it for a repository that sees frequent automated builds.

## Setup

- Update values `USERNAME` and `REPOSITORY` in `cleanup.py`
- Create a file `.env` and set `ACCESS_TOKEN` to your Docker Hub access token

## Run

```sh
uv run cleanup.py
```
