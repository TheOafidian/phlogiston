# Phlogiston

A python package that allows visualization (in 2 or 3D) of fictional starcharts. 
Written to be used for a D&D Spelljammer campaign.

# Installation

Installation can currently be done from the repo itself.
```
git clone https://github.com/TheOafidian/phlogiston.git
cd phlogiston
pip install -r requirements.txt
pip install .
```

# Usage
```usage: phlogiston [-h] {chart,random}```

Phlogiston has two modes: 
- chart: reads coordinate data and plots them in a plotly graph.
- random: generates a random starchart and saves the coordinates to a file (can be modified and used as input for chart). 

## Chart command

```
usage: phlogiston chart [-h] [--output OUTPUT] [--extension {html,pdf,png}] [--dimensions {2,3}] [--radius RADIUS] [--distance_metric DISTANCE_METRIC] [--name NAME] [--dtime DTIME] filename

positional arguments:
  filename

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Name of file to save output map to.
  --extension {html,pdf,png}, -e {html,pdf,png}
                        Extension to save output as.
  --dimensions {2,3}, -n {2,3}
                        Amount of dimensions to plot.
  --radius RADIUS, -r RADIUS
                        Relative distance two spheres can maximally have to draw routes between them (0-1).
  --distance_metric DISTANCE_METRIC, -p DISTANCE_METRIC
                        Minkowski distance metric to use.
  --name NAME, -s NAME  Name of the starchart. Gets added to the top of the figure.
  --dtime DTIME, -t DTIME
                        Modifier to the distance in time betweeen different spheres.
```

The Minkowski distance metric determines how distances are calculated (1 and 2 for Manhattan and Euclidean distances respectively), but  other values can also be explored to simulate the Phlogiston's properties.

An example of how to visualiwe the effect of the parameter on distances from Wikipedia:

![Minkowski distance](https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/2D_unit_balls.svg/1451px-2D_unit_balls.svg.png)

## Random command
```
usage: phlogiston random [-h] [--spheres SPHERES] [--max-length MAX_LENGTH] [--seed SEED] filename

positional arguments:
  filename

optional arguments:
  -h, --help            show this help message and exit
  --spheres SPHERES, -n SPHERES
                        The amount of spheres to populate the chart with.
  --max-length MAX_LENGTH, -l MAX_LENGTH
                        The max distance between two spheres that is still counted as 'connected'. Relative between
                        0-1.
  --seed SEED, -s SEED  A seed for reproducible random charting.
```
