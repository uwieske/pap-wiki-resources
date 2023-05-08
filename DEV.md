# Development

All development is taken place on de `dev` branch.

The main branch contains stable code. When the code on `dev` has reached a stable state, it will be merged with `main`.
Users can clone the repo and be sure that they will use the latest stable version(s).

To switch to `dev` branch, you will need to execute checkout command and switch to `dev` branch:

````
git checkout dev
````


## Environment

Updating environment with (added/removed/changed) dependencies:

````
conda env update --file environment-dev.yml --prune
````