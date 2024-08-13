`visualize.py` contains the function `visualize`, which allows for easy visualization of 3D grayscale voxel images stored in the form of a 3D array of values.
The example data used in the demo notebook, `run_6355.mrc`, can be found at [the CryoET Data Portal](https://cryoetdataportal.czscience.com/runs/6355).
Download the exact file [here](https://cryoetdataportal.czscience.com/runs/6355?download-step=download&download-config=tomogram&tomogram-sampling=10.4&tomogram-processing=raw&file-format=mrc&download-tab=download).

# Usage
In Unix terminals, enter the following command to download the installation file:

```shell
wget https://github.com/mward19/visualize_voxels/raw/master/dist/visualize_voxels-0.1-py3-none-any.whl
```

Use pip on the just downloaded file to install it to a python environment:

```shell
pip install visualize_voxels-0.1-py3-none-any.whl`
```

Then use the `visualize` function on a 3D image array in a script or Jupyter notebook to visualize it:

```python
from visualize_voxels import visualize
import numpy as np

number_generator = np.random.default_rng()
array_to_visualize = number_generator.normal(size=(100, 100, 100))

visualize(array_to_visualize)
```

`visualize` has many keyword arguments to customize display and plot points. See `demo_visualize.ipynb` for examples.
