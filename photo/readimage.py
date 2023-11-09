from scipy import datasets
import imageio

# face = datasets.face()
# imageio.imsave('face.png', face) # uses the Image module (PIL)
face = imageio.v2.imread('face.png')
print(type(face))
print(f'shape: {face.shape} dtype: {face.dtype}')
import matplotlib.pyplot as plt
plt.imshow(face, cmap=plt.cm.gray)