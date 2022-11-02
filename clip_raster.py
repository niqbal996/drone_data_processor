import numpy as np
import rasterio as rio
import affine
import cv2

class ImageForClipModel:

    # Get band, band shape, dtype, crs and transform values
    def __init__(self, image_address, output_bands=[1, 2, 3]):
        self.dataset = rio.open(image_address)
        self.crs = self.dataset.crs
        self.b_trans = self.dataset.transform
        self.num_bands = self.dataset.count
        self.output_bands = output_bands
        self.clipped_images = []
        self.clipped_addresses = []

    # Function for clipping band
    def clip_raster(self, height, width, buffer=0,
                    save_mode=False, prefix='clipped_band_',
                    pass_empty=False):
        r_pos = 0
        clipped_image = np.zeros((height, width, len(self.output_bands)), dtype=np.uint16)
        self.band = self.dataset.read(1)
        self.band_shape = self.band.shape
        self.band_dtype = self.band.dtype
        while r_pos < self.band_shape[0]:
            col_pos = 0
            while col_pos < self.band_shape[1]:
                for band in self.output_bands:
                    clipped_image[:, :, band-1] = self.dataset.read(band)[r_pos:r_pos + height,
                                                                            col_pos:col_pos + width]

                    # Check if frame is empty
                    if pass_empty:
                        if np.mean(clipped_image) == 0:
                            print('Empty frame, not saved')
                            break

                    # Positioning
                    tcol, trow = self.b_trans * \
                                 (col_pos, r_pos)
                    new_transform = affine.Affine(self.b_trans[0],
                                                  self.b_trans[1],
                                                  tcol,
                                                  self.b_trans[3],
                                                  self.b_trans[4],
                                                  trow)
                    image = [clipped_image, self.crs, new_transform,
                             clipped_image.shape[0],
                             clipped_image.shape[1],
                             self.band_dtype]

                # Update column position
                col_pos = col_pos + width - buffer

                # Update row position
                r_pos = r_pos + height - buffer
        # Save or append into a set
        if save_mode:
            filename = prefix + 'x_' + \
                       str(col_pos) + '_y_' + \
                       str(r_pos) + '.tif'

            with rio.open(filename, 'w',
                          driver='GTiff',
                          height=image[3], width=image[4],
                          count=3, dtype=image[5],
                          crs=image[1],
                          transform=image[2]) as dst:
                dst.write(image[0], 1)
            self.clipped_addresses.append(filename)
        else:
            self.clipped_images.append(clipped_image)



        if save_mode:
            print('Tiles saved successfully')
            return self.clipped_addresses
        else:
            print('Tiles prepared successfully')
            return self.clipped_images
