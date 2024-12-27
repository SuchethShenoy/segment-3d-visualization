# segment-3d-visualization

A class implementation to provide 3D visualization for [Cheetah](https://github.com/desy-ml/cheetah) Segment objects.

Generates an interactive 3D plot window with the beam and segment elements such as Dipoles and Quadrupoles positioned according to the lattice description as defined in the Cheetah Segment object.

Uses [PyVista](https://docs.pyvista.org/) for 3D visualization and [Trimesh](https://trimesh.org/) for loading 3D Mesh Objects.

## Installation

To install the requirements for the segment-3d-visualization, run

```
pip install -r requirements.txt
```

## How To Use

1. Initialize a ```Segment3DPlotter``` object for the Cheetah Segment.
2. Use the class function ```plot_segment()``` to generate a 3D plot for the Segment.
3. Use the class function ```show()``` to render the 3D plot in an interactive Plot Window.

You can check the [example.py](example.py) file for a simple example of the class usage.
```
python3 example.py
```

## Additional Instructions for 3D Model Files

Check out the instructions at [3D_models/MODELS.md](3D_models/MODELS.md).
