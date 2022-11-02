import rasterio as rio
from rasterio.plot import show
import matplotlib.pyplot as plt
from clip_raster import ImageForClipModel
import numpy as np
import glob

# uos_raster = rio.open('/media/niqbal/T7/raw_datasets/DRONE_UOS/ortho.tif')
# print('CRS of Raster Data: ' + str(uos_raster.crs))
# print('Number of Raster Bands: ' + str(uos_raster.count))
# print('Interpretation of Raster Bands: ' + str(uos_raster.colorinterp))
# blue = uos_raster.read(1)[0:100, 0:100]
# green = uos_raster.read(2)
# red = uos_raster.read(3)
print('hold')

test_image = '/media/niqbal/T7/raw_datasets/DRONE_UOS/ortho.tif'
clipper = ImageForClipModel(image_address=test_image)

clipper.clip_raster(height=2560,    #Quad HD
                    width=1440,
                    buffer=0,
                    save_mode=True,
                    prefix='/media/niqbal/T7/raw_datasets/DRONE_UOS/clipped/clipped_band_',
                    pass_empty=False)

# Show test image
# with rio.open(test_image, 'r') as src:
#     img = src.read(1)
#     img = img.astype(np.float32)
#     img = img / np.max(img)
#     img[img <= 0] = np.nan
# images = glob.glob('/media/niqbal/T7/raw_datasets/DRONE_UOS/clipped/*.tif')
#
# for image in images:
#     image = rio.open(image)
#     b = image.read(1)
#     g = image.read(2)
#     r = image.read(3)
#     plt.figure(figsize=(12, 12))
#     plt.imshow(image)
#     plt.show()