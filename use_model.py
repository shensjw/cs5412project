import json
import numpy as np
import pandas as pd
import joblib

## Global variables for model paths
Model_Path = "./model/"
Estrus_Model_Path = "estrus-model.pkl"
Preg_Model_Path = "pregprob-model.pkl"


def run(model, data):
    try:
        result = model.predict(data)
        return True, result.tolist()
    except Exception as e:
        result = str(e)
        return False, result


def model_predict(d_yield, d_fat, d_protein, d_cond, d_lactose, d_scc, d_blood):
    model_estr = joblib.load(Estrus_Model_Path)
    model_preg = joblib.load(Preg_Model_Path)

    input_data = pd.DataFrame({'Yield': pd.Series(d_yield, dtype='float64'),
                               'Fat': pd.Series(d_fat, dtype='float64'),
                               'Protein': pd.Series(d_protein, dtype='float64'),
                               'Conductivity': pd.Series(d_cond, dtype='float64'),
                               'Lactose': pd.Series(d_lactose, dtype='float64'),
                               'Scc': pd.Series(d_scc, dtype='float64'),
                               'Blood': pd.Series(d_blood, dtype='float64')})

    res_estr = run(model_estr, input_data)
    res_preg = run(model_preg, input_data)
    print(res_estr)
    print(res_preg)
    if not res_estr[0] or not res_preg[0]:
        return False, res_estr[1], res_preg[1]
    return True, res_estr[1], res_preg[1]


def fromTestFile(filename):
    line0 = []
    line1 = []
    line2 = []
    line3 = []
    line4 = []
    line5 = []
    line6 = []
    label = []
    with open(filename, encoding='latin-1') as f:
        lines = csv.reader(f)
        i = 0
        for line in lines:
            i += 1
            if i == 1: continue
            line0.append(line[0])
            line1.append(line[1])
            line2.append(line[2])
            line3.append(line[3])
            line4.append(line[4])
            line5.append(line[5])
            line6.append(line[6])
            label.append(int(float(line[7])))
    return line0, line1, line2, line3, line4, line5, line6, label


if __name__ == "__main__":
    # input_sample = pd.DataFrame({'Yield': pd.Series(['39359.0'], dtype='float64'), 'Fat': pd.Series(['4.11'], dtype='float64'), 'Protein': pd.Series(['3.07'], dtype='float64'), 'Conductivity': pd.Series(['8.9'], dtype='float64'), 'Lactose': pd.Series(['4.65'], dtype='float64'), 'Scc': pd.Series(['2667906.0'], dtype='float64'), 'Blood': pd.Series(['0.01'], dtype='float64')})
    # output_sample = np.array([0])

    model = joblib.load('./model/pregprob-model.pkl')
    line0, line1, line2, line3, line4, line5, line6, label = fromTestFile('./data/p_prob_test.csv')
    input_data = pd.DataFrame({'Yield': pd.Series(line0, dtype='float64'),
                'Fat': pd.Series(line1, dtype='float64'),
                'Protein': pd.Series(line2, dtype='float64'),
                'Conductivity': pd.Series(line3, dtype='float64'),
                'Lactose': pd.Series(line4, dtype='float64'),
                'Scc': pd.Series(line5, dtype='float64'),
                'Blood': pd.Series(line6, dtype='float64')})
    print(input_data)
    _, result = run(model, input_data)
    #print(result)
    tmp_result = result[12:-2]
    result_list = tmp_result.split(',')

    for_label_result = []
    count_1 = 0
    for i in range(len(result_list)):
        result_list[i] = float(result_list[i].strip())
        if result_list[i] > 0.5:
            for_label_result.append(1)
            count_1 += 1
        else: for_label_result.append(0)
    print(len(result_list))

    print(count_1)

    correct = 0
    for i in range(len(label)):
        if label[i] == for_label_result[i] and label[i] == 1:
            correct += 1
    print(correct)

    accuracy = 0
    for i in range(len(label)):
        if label[i] == for_label_result[i]:
            accuracy += 1
    print("accuracy:", accuracy/len(label))
