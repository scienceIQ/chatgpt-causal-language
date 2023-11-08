from sklearn.metrics import confusion_matrix, f1_score, cohen_kappa_score, classification_report
import numpy as np

def get_confusion_matrix(data, label1, label2, output_dir):
    true, pred = data[label1], data[label2]
    true = true.to_numpy().reshape(-1)
    pred = pred.to_numpy().reshape(-1)
    mt = confusion_matrix(true, pred)

    with open(output_dir.format('confusion_matrix'), 'a') as f:
        f.write(f'---{label1} & {label2} Matrix---\n')
        f.write(np.array2string(mt)+'\n\n')
    
def get_macrof1_score(data, label1, label2, output_dir):
    true, pred = data[label1], data[label2]
    score = f1_score(true, pred, average='macro')
    report = classification_report(true, pred, digits=3)
    print(f"Macro f1-score between {label1} & {label2}: {round(score, 3)}")
    print('---Classification Report created')

    with open(output_dir.format('macro_f1score'), 'a') as f:
        f.write(f"Macro f1-score between {label1} & {label2}: {round(score, 3)}\n")
        f.write(report+'\n')

def get_kappa_score(data, label1, label2, output_dir):
    true, pred = data[label1], data[label2]
    score = cohen_kappa_score(true, pred)
    print(f"Cohen Kappa score between {label1} & {label2}: {round(score, 3)}")

    with open(output_dir.format('cohenKappa'), 'a') as f:
        f.write(f"Cohen Kappa score between {label1} & {label2}: {round(score, 3)}\n")