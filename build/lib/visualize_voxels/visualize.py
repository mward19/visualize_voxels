""" 
Dependencies: 
    numpy
    matplotlib
    ipywidgets
    IPython
    imageio
    tqdm
"""

import numpy as np

import matplotlib.pyplot as plt

import ipywidgets as widgets
from IPython.display import Image
from IPython.display import display

import imageio.v2 as imageio
from PIL import Image as PILImage
import io
from tqdm.notebook import tqdm as tqdmn
from tqdm import tqdm

from collections.abc import Iterable

import warnings

def round_to_nearest(x, number_list):
    """ Rounds x to the nearest value in number_list. """
    # Find the nearest value
    nearest_value = min(number_list, key=lambda y: abs(y - x))
    return nearest_value

def reduce_dim(point, axis):
    """ 
    Takes a point, say [x, y, z], and removes the value on the `axis` dimension, i.e., returning [x, z] if `axis` is 1.
    """
    return [val for (index, val) in enumerate(point) if index != axis]

def in_notebook():
    """ Checks if the place where this function is run is a Python notebook. """
    try:
        return get_ipython().__class__.__name__ == 'ZMQInteractiveShell'
    except NameError:
        return False
    
def remove_duplicates(iterable):
    seen = set()
    return [x for x in iterable if not (x in seen or seen.add(x))]

def visualize(
            array, 
            filename=None,
            *, 
            scale=1.0,          # Scale image size
            slices=50,   # If int, number of slices to display. If list, slices to display.
            fps=10.,              # Frames per second
            axis=0,             # Axis to slice over
            interactive=False,  
            marks=[],           # List of 3D tuples to mark
            marksize=75,        # Size of marks in pixels
            gusmode=False,
            showaxes=True
    ):
    """
    Yields a notebook visualization of a 3D array `array` as a GIF.

    Args:
        array (nparray): 
            The array to visualize
        filename (string): 
            If set, saves the displayed GIF as `filename`. Outside of notebooks, this must be set.
    Keyword args:
        scale (float or int): 
            Scales the image size.
        slices (int or iterable of ints): 
            Number of slices or list of slices to display.
        fps (int): 
            Frames per second of the displayed GIF
        axis (int): 
            The axis to slice over
        interactive (bool): 
            If True, adds slider widgets to allow interaction. Only applies in notebook environments
        marks (list of 3-element indexables): 
            Points to mark in red
        marksize (float or int): 
            size of marks
        showaxes (bool)
            If True, displays all three axes.
        gusmode (bool): 
            If set, displays axes how Gus (and IMOD) likes it. Defaults to False
    """
    # Checks if the current environment is a notebook
    isnotebook = in_notebook()

    # If not a notebook and no filename is provided, this function cannot display the GIF
    if not isnotebook and filename is None:
        raise ValueError("If you are not in a notebook environment, you must provide a filename.")

    max_slice = array.shape[axis]
    
    if isinstance(slices, int):
        slice_indices = np.linspace(0, max_slice-1, slices, dtype=int)
    else:
        slice_indices = [int(s) for s in slices]

    slice_indices = remove_duplicates(slice_indices)    
    n_slices = len(slice_indices)
    
    # List to store frames for the GIF
    frames = []

    # Since we generally don't plot each slice, adjust `marks` to ensure each mark is shown
    marks_by_slice = dict()
    for mark in marks:
        # Convert mark to a list if it's a tuple to ensure mutability
        if isinstance(mark, tuple):
            mark = list(mark)
        mark[axis] = round_to_nearest(mark[axis], slice_indices)
        if mark[axis] not in marks_by_slice:
            marks_by_slice[mark[axis]] = [reduce_dim(mark, axis)]
        else:
            marks_by_slice[mark[axis]].append(reduce_dim(mark, axis))

    # Determine the axes to display
    not_slice_axes = [dim for dim in range(array.ndim) if dim != axis]
    x_axis = not_slice_axes[1]
    y_axis = not_slice_axes[0]
    
    # Determine the aspect ratio of each slice 
    # (`view_tuple` allows for slicing through an arbitrary axis)
    view_tuple = [slice(None)] * array.ndim
    view_tuple[axis] = 0
    slice_shape = array[tuple(view_tuple)].shape
    aspect_ratio = slice_shape[1] / slice_shape[0]
    figsize = (5*scale*aspect_ratio, 5*scale)

    # Initialize progress bar
    if isnotebook:
        progress_bar = tqdmn(
            total=n_slices, 
            desc="Generating visualization", 
            unit="slice", 
            unit_scale=True,
        )
    else:
        progress_bar = tqdm(
            total=n_slices, 
            desc="Generating visualization", 
            unit="slice", 
            unit_scale=True,
        )

    # Generate images of slices
    for slice_index in slice_indices:
        if gusmode:
            axislabels = ["Z axis", "Y axis", "X axis"]
        else:
            axislabels = ["Axis 0", "Axis 1", "Axis 2"]
        fig, ax = plt.subplots(figsize=figsize) # TODO: automate aspect ratio
        
        # `view_tuple` allows for slicing through an arbitrary axis
        view_tuple = [slice(None)] * array.ndim
        view_tuple[axis] = slice_index
        # Show the slice
        ax.imshow(array[tuple(view_tuple)], cmap='gray')
        if showaxes:
            ax.set_title(f"{axislabels[axis]}: Slice {slice_index}")
            ax.set_xlabel(axislabels[x_axis])
            ax.set_ylabel(axislabels[y_axis])
            ax.axis('on')
        else:
            ax.axis('off')
            # Remove the padding around the image
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        if len(marks_by_slice) > 0: # Don't bother with the overhead of marks if there are none
            # If there is a mark on or near this slice, show it
            for mark_slice_index, marks_on_slice in marks_by_slice.items():
                if mark_slice_index == slice_index:
                    x = [mark[0] for mark in marks_on_slice]
                    y = [mark[1] for mark in marks_on_slice]
                    # Reverse x and y axis labels because of imshow behavior
                    ax.scatter(y, x, c='red', s=marksize) 

        # Save the slice to a temporary file and read it back as an image
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)
        
        # Save the slice
        frame = imageio.imread(buf)
        frames.append(frame)

        progress_bar.update(1)
    progress_bar.close()
    
    
    if filename:
        # Save GIF to the specified filename
        with open(filename, 'wb') as f:
            imageio.mimwrite(f, frames, format='gif', fps=fps, loop=0)
        
    # If this is not a notebook, further interaction is not possible. Save the GIF
    if not isnotebook:
        return

    # ~~ From this point forward, it is assumed the user is in a notebook. ~~ 
    # Save all frames as a GIF to a buffer
    gif_buf = io.BytesIO()
    imageio.mimwrite(gif_buf, frames, format='gif', fps=fps, loop=0)
    gif_buf.seek(0)

    if interactive:
        def gif_frame(gif, frame):
            # Seek to the specific frame
            gif.seek(frame)
            # Display the specific frame
            display(gif)
        
        # Load the GIF from the buffer
        gif = PILImage.open(io.BytesIO(gif_buf.getvalue()))
        max_frame = n_slices
        frame_slider = widgets.IntSlider(
            min=0, 
            max=max_frame-1, 
            step=1, 
            value=max_frame // 2, 
            description="Frame index",
            layout=widgets.Layout(width='600px')
        )
        widgets.interact(
            gif_frame, 
            gif=widgets.fixed(gif), 
            frame=frame_slider
        )
        return Image(data=gif_buf.getvalue(), format='gif')
    
    # Return the raw GIF
    return Image(data=gif_buf.getvalue(), format='gif')

