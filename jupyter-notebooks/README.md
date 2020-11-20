# jupyter-notebooks
This directory serves as a playground to test different python libraries as, e.g., fbprophet or creme-ml, within jupyter notebooks. 

## Maintainers / Developers
* Niklas Wilcke <niklas.wilcke@uniberg.com>
* Christoph Ölschläger <christoph.oelschlaeger@uniberg.com>
* David Bröhan <david.broehan@uniberg.com>

## Project State
For now, there is a notebook to test the fbprophet library..

## Requirements
Python 3.8.5
packages in requirements.txt

### Usage
´´´
# Build the docker image
docker build -t jupyter-notebook-prophet .
# Run the docker image
docker run -p "8888:8888" jupyter-notebook-prophet
# Open URL in the logs containg the secret token
# Open the notebook playground.ipynb
# To terminate the notebook server hit ctrl-c
```
