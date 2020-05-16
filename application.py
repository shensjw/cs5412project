from flask import Flask, request, redirect, render_template, url_for
from use_model import model_predict

## App settings
DEBUG = True
app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'prediction':
            return redirect(url_for('prediction'))
        elif action == 'visualization':
            return redirect(url_for('visualization'))
    return render_template('index.html')


@app.route('/prediction', methods=['GET','POST'])
def prediction():
    ERROR = 0
    Error_Message = ""
    input_text = ""
    if request.method == 'POST':
        if "home" in request.form:
            return redirect(url_for('index'))
        elif "submit" in request.form:
            input_text = request.form['input']
            lines = input_text.splitlines()
            num_data = len(lines)

            ## data processing
            data_yield, data_fat, data_prot, data_cond, data_lact, data_scc, data_blood = [], [], [], [], [], [], []
            try:
                if num_data == 0:
                    Error_Message = "Please input data!"
                    raise Exception(Error_Message)
                for line in lines:
                    data_str_list = line.split(',')
                    if len(data_str_list) != 7:
                        Error_Message = "Missing input data!"
                        raise Exception(Error_Message)
                    data_line = []
                    for d_s in data_str_list:
                        try:
                            d = float(d_s)
                        except ValueError:
                            Error_Message = "Unknown input data!"
                            raise Exception(Error_Message)
                        else:
                            data_line.append(d)
                    data_yield.append(data_line[0])
                    data_fat.append(data_line[1])
                    data_prot.append(data_line[2])
                    data_cond.append(data_line[3])
                    data_lact.append(data_line[4])
                    data_scc.append(data_line[5])
                    data_blood.append(data_line[6])

                success, res_estr, res_preg = model_predict(data_yield, data_fat, data_prot, data_cond, data_lact, data_scc, data_blood)

                if not success:
                    Error_Message = res_estr
                    raise Exception(Error_Message)
            except:
                ERROR = 1
                return render_template('prediction.html', input=input_text, error=ERROR, error_message=Error_Message, output=[])
            else:
                ## compose result into json
                res_json = []
                for i in range(len(lines)):
                    estrus = res_estr[i]
                    preg = round(res_preg[i], 3)  # round prob to 3 decimals
                    if not estrus:
                        preg = 'N/A'
                    res_json.append({'#': i+1,
                                     'Yield': data_yield[i],
                                     'Fat(%)': data_fat[i],
                                     'Protein(%)': data_prot[i],
                                     'Conductivity': data_cond[i],
                                     'Lactose(%)': data_lact[i],
                                     'SCC': data_scc[i],
                                     'Blood(%)': data_blood[i],
                                     'Estrus(T/F)': estrus,
                                     'Pregnant Probability': preg
                                    })
                return render_template('prediction.html', input=input_text, error=ERROR, error_message=Error_Message, output=res_json)

    return render_template('prediction.html', input=input_text, error=ERROR, error_message=Error_Message, output=[])


@app.route('/visualization', methods=['GET','POST'])
def visualization():
    if request.method == 'POST':
        print(request.url)
        print(url_for('index'))
        if "home" in request.form:
            return redirect(url_for('index'))
    return render_template('visualization.html')


if __name__ == "__main__":
    app.run(debug=DEBUG)
