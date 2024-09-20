import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


# Read the data of each user from the text files. it should be row data of 128 columns comma separated
user1 = pd.read_csv('user1.txt', sep = ',', header=None)
user2 = pd.read_csv('user2.txt', sep = ',', header=None)
user3 = pd.read_csv('user3.txt', sep = ',', header=None)

# Get the number of samples for each user
samples1 = len(user1)
samples2 = len(user2)
samples3 = len(user3)

# Remove the last column which is empty
user1 = np.array(user1)[:,:-1]
user2 = np.array(user2)[:,:-1]
user3 = np.array(user3)[:,:-1]
# Stack the data of each user to create a single array
users = np.vstack([user1, user2, user3])

print(users.shape)

# Define the PCA model and fit the data
pca = PCA(n_components=2)
pca_data = pca.fit_transform(users)

# Plot the PCA visualization of the face encodings
fig2 = plt.figure(figsize=(8, 6))
plt.scatter(pca_data[:samples1, 0], pca_data[:samples1, 1], color='red', label='User 1')
plt.scatter(pca_data[samples1:samples1+samples2, 0], pca_data[samples1:samples1+samples2, 1], color='blue', label='User 2')
plt.scatter(pca_data[samples1+samples2:, 0], pca_data[samples1+samples2:, 1], color='green', label='User 3')
plt.legend()
plt.title('PCA visualization of face encodings')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.show()