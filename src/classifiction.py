from sklearn import svm
# from xlutils.copy import copy
from xlrd import open_workbook


def readFeatures():

    wb = open_workbook("xlwt example.xls")
    sheet = wb.sheet_by_index(0)
    features=[]
    for i in range(208):
        col=[]
        for j in range(361):
            val=sheet.cell_value(j,i )
            col.append(val)
        features.append(col)
        print(col)
    return features




def classify(tr_features, labels, test_features):
    clf = svm.SVC(kernel='linear')
    clf.fit(tr_features, labels)
    labels_pred = clf.predict(test_features)
    return labels_pred

