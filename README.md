`visualize_voxels` contains `visualize`, which allows for fast, easy visualization of 3D grayscale voxel images stored in the form of a 3D array of values.

Simply calling `visualize(data)` on a 3D numpy array `data` containing nearly 500 million voxels yields this:

![Example visualization](default_visualization.gif)

# Installation
Download the installation file at [this link](https://github.com/mward19/visualize_voxels/raw/master/dist/visualize_voxels-0.1-py3-none-any.whl), or use `wget`:

```shell
wget https://github.com/mward19/visualize_voxels/raw/master/dist/visualize_voxels-0.1-py3-none-any.whl
```

Use pip on the file you just downloaded to install it to a python environment:

```shell
pip install visualize_voxels-0.1-py3-none-any.whl
```

# Usage
Use the `visualize` function on a 3D image array in a script or Jupyter notebook to visualize it:

```python
from visualize_voxels import visualize
import numpy as np

number_generator = np.random.default_rng()
array_to_visualize = number_generator.normal(size=(100, 100, 100))

visualize(array_to_visualize)
```

`visualize` has many keyword arguments to customize display and plot points. See `demo_visualize.ipynb` for examples.

# Demo
The example data `run_6355.mrc` used in the included demo notebook `demo_visualize.ipynb` can be found at [the CryoET Data Portal](https://cryoetdataportal.czscience.com/runs/6355).
Download the exact file [here](https://cryoetdataportal.czscience.com/runs/6355?download-step=download&download-config=tomogram&tomogram-sampling=10.4&tomogram-processing=raw&file-format=mrc&download-tab=download). The demo notebook relies on the python library `mrcfile` to read `run_6355.mrc`, as well as `skimage`, which can both be installed with `pip`: 

```shell
pip install mrcfile scikit-image
```
