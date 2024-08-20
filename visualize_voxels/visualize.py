import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
mpl.rcParams['animation.embed_limit'] = 500.0  # Size limit in MB

import ipywidgets as widgets
from IPython.display import Image
from IPython.display import display
from IPython.display import HTML

from tqdm.notebook import tqdm as tqdmn
from tqdm import tqdm


def set_conditional_backend():
    """Sets the Matplotlib backend based on the environment."""
    try:
        # Check if Tkinter is available for GUI support
        import tkinter  # Attempt to import Tkinter
        # If available, use TkAgg for interactive plots
        mpl.use('TkAgg')
    except ImportError:
        # If Tkinter is not available, fall back to Agg for file-based output
        mpl.use('Agg')
        print("Tkinter not found. Using Agg backend. Interactive output will not be possible in .py scripts.")

# Call the function to set the backend
set_conditional_backend()

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
        title=None,
        scale=1.0,          # Scale image size
        slices=50,          # If int, number of slices to display. If list, slices to display.
        fps=10.,            # Frames per second
        axis=0,             # Axis to slice over
        marks=[],           # List of 3D tuples to mark
        marksize=75,        # Size of marks in pixels
        markalpha=1,
        imodmode=False,
        showaxes=True
    ):
    """
    Yields a notebook visualization of a 3D array `array` as an animation using FuncAnimation.

    Args:
        array (nparray): 
            The array to visualize
        filename (string): 
            If set, saves the displayed animation as `filename`.
    Keyword args:
        title (string):
            A title for the plot
        scale (float or int): 
            Scales the image size.
        slices (int or iterable of ints): 
            Number of slices or list of slices to display.
        fps (int): 
            Frames per second of the displayed animation
        axis (int): 
            The axis to slice over
        marks (list of 3-element indexables): 
            Points to mark in red
        marksize (float or int): 
            size of marks
        markalpha (float):
            transparency of marks
        showaxes (bool)
            If True, displays all three axes.
        imodmode (bool): 
            If set, displays axes how IMOD does (Z Y X). Defaults to False
    """
    isnotebook = in_notebook()
    if isnotebook:
        plt.ion()
    else:
        plt.ioff()

    max_slice = array.shape[axis]
    
    if isinstance(slices, int):
        slice_indices = np.linspace(0, max_slice-1, slices, dtype=int)
    else:
        slice_indices = [int(s) for s in slices]

    slice_indices = remove_duplicates(slice_indices)
    n_slices = len(slice_indices)

    marks_by_slice = dict()
    for mark in marks:
        if isinstance(mark, tuple):
            mark = list(mark)
        mark[axis] = round_to_nearest(mark[axis], slice_indices)
        if mark[axis] not in marks_by_slice:
            marks_by_slice[mark[axis]] = [reduce_dim(mark, axis)]
        else:
            marks_by_slice[mark[axis]].append(reduce_dim(mark, axis))

    not_slice_axes = [dim for dim in range(array.ndim) if dim != axis]
    x_axis = not_slice_axes[1]
    y_axis = not_slice_axes[0]
    
    view_tuple = [slice(None)] * array.ndim
    view_tuple[axis] = 0
    slice_shape = array[tuple(view_tuple)].shape
    aspect_ratio = slice_shape[1] / slice_shape[0]
    figsize = (5 * scale * aspect_ratio, 5 * scale)

    fig, ax = plt.subplots(figsize=figsize)

    frames_processed = set() # Keeps track of processed frames, for progress bar
    
    def update(slice_index):
        ax.clear()
        if imodmode:
            axislabels = ["Z axis", "Y axis", "X axis"]
        else:
            axislabels = ["Axis 0", "Axis 1", "Axis 2"]

        view_tuple[axis] = slice_indices[slice_index]
        ax.imshow(array[tuple(view_tuple)], cmap='gray')

        if showaxes:
            if title is None:
                ax.set_title(f"{axislabels[axis]}: Slice {slice_indices[slice_index]}")
            else:
                ax.set_title(f"{title}\n{axislabels[axis]}: Slice {slice_indices[slice_index]}")
            ax.set_xlabel(axislabels[x_axis])
            ax.set_ylabel(axislabels[y_axis])
            ax.axis('on')
        else:
            ax.axis('off')
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        

        if slice_indices[slice_index] in marks_by_slice:
            marks_on_slice = marks_by_slice[slice_indices[slice_index]]
            x = [mark[0] for mark in marks_on_slice]
            y = [mark[1] for mark in marks_on_slice]
            ax.scatter(y, x, c='red', s=marksize, alpha=markalpha)

        # Manage progress bar
        if slice_index not in frames_processed:
            progress_bar.update(1)
            frames_processed.add(slice_index)

    # Load the animation
    anim = FuncAnimation(
        fig, 
        update, 
        frames=n_slices, 
        interval=1000/fps,
        repeat=True
    )

    # Initialize a progress bar to monitor the animation loading
    if isnotebook:
        progress_bar = tqdmn(
            total=n_slices,
            desc="Rendering visualization",
            unit="frame"
        )
    else:
        progress_bar = tqdm(
            total=n_slices,
            desc="Rendering visualization",
            unit="frame"
        )

    if isnotebook:
        display(HTML(anim.to_jshtml(default_mode='reflect')))
    else:
        plt.show()

    if filename:
        frames_processed = set()
        progress_bar.reset()
        progress_bar.desc = "Saving visualization"
        anim.save(filename, writer='imagemagick', fps=fps)
        display(f"Visualization saved as {filename}")
    
    progress_bar.close()    
    plt.close(fig)


