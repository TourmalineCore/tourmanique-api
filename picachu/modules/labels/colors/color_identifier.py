from sklearn.cluster import KMeans
from collections import Counter

from picachu import config
from picachu.modules.photos.photo_preprocessing import preprocess_photo


class ColorIdentifier:
    def __init__(self):
        self.clf = KMeans(n_clusters=int(config.colors_number))

    def get_colors(self, photo):
        preprocessed_photo = preprocess_photo(photo)

        labels = self.clf.fit_predict(preprocessed_photo)

        counts = Counter(labels)
        counts = dict(sorted(counts.items()))

        center_colours = self.clf.cluster_centers_
        ordered_colours = [center_colours[i] for i in counts.keys()]

        colors = [ordered_colours[i].astype(int) for i in counts.keys()]

        colors = list(map(lambda color: {"red": color[0], "green": color[1], "blue": color[2]},
                          colors))

        return colors
