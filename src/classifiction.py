from sklearn import svm


def readFeatures():
    pass


def classify(tr_features, labels, test_features):
    clf = svm.SVC(kernel='linear')
    clf.fit(tr_features, labels)
    labels_pred = clf.predict(test_features)
    return labels_pred

