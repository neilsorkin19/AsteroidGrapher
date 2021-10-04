import numpy as np
import matplotlib.pyplot as plt
import os

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rows = 511
    columns = 512
    # used for removing noise
    filter_quantile = 0.90
    filtered_multiplier = 0.01

    directory = 'data_maps\\'
    # used to add images and remove noise
    summed_arrays = np.zeros((rows, columns))

    # makes nice diagram of plots
    fig, axs = plt.subplots(nrows=2, ncols=4, figsize=(9, 6),
                            subplot_kw={'xticks': [], 'yticks': []})

    for filename, ax in zip(os.listdir(directory), axs.flat):
        # read and convert to big endian
        array = np.fromfile(directory + filename, np.dtype('<i4'), -1, "", 0)
        # filter noise / background
        filtered_array = np.where(array < np.quantile(array, filter_quantile), array * filtered_multiplier, array)
        # shape into 2d array
        mapped = np.reshape(filtered_array, (rows, columns))
        # add it to the combined image
        summed_arrays = np.array([summed_arrays, mapped]).sum(axis=0)
        # add it to the 2d matrix of plots
        ax.imshow(mapped)
        # name using file info
        ax.set_title(str(filename)[13:21])

    plt.imshow(summed_arrays)
    plt.show()

    # filter the summed image further
    filtered_summed_arrays = np.where(summed_arrays < np.quantile(summed_arrays, filter_quantile), 0, summed_arrays)
    plt.imshow(filtered_summed_arrays)
    plt.suptitle('Asteroid 2016 AJ193')
    plt.tight_layout()
    plt.show()
