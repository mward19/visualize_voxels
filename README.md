`visualize.py` contains the function `visualize`, which allows for easy visualization of 3D grayscale voxel images stored in the form of a 3D array of values.
The example data used in the demo notebook, `run_6355.mrc`, can be found at [the CryoET Data Portal](https://cryoetdataportal.czscience.com/runs/6355).
Download the exact file [here](https://cryoetdataportal.czscience.com/runs/6355?download-step=download&download-config=tomogram&tomogram-sampling=10.4&tomogram-processing=raw&file-format=mrc&download-tab=download).

# Usage
- Download `visualize.py` and include it in your script or notebook with `import visualize` (assuming you have put `visualize.py` in the same directory as your project, or that you've put it on Python's path).
- Ensure that your volumetric image is stored as a 3D array, which we will call `data`.
- If you are using a Jupyter notebook, call `visualize(data)` to get a snapshot of the volumetric image.
- In a normal script (not a notebook), you must also include a filename to which the visualization will be saved as a `.gif`, i.e., `visualize(data, "output.gif")`.
- Other options are described in `visualize`'s docstring, including resizing the output, basic interactive output (for notebooks), and marking points on the volume. 
