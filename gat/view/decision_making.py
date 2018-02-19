from flask import Flask, render_template, request, jsonify, Blueprint
from gat.dm.runner import DMRunner

app = Flask(__name__)
# Key is the case number string, value is the runner instance
runners = {}
# Key is the case number ID string, value is the message results
results = {}

dm_blueprint = Blueprint('dm_blueprint', __name__)


@dm_blueprint.route('/dm_landing/', methods=["GET", "POST"])
def dm_landing():
    if request.method == 'GET':
        return render_template('dm_submit_page.html')
    else:
        case_num = request.args.get("case_num", None)
        number_of_runs = 1
        if request.form['action'] == 'Batch Run':
            number_of_runs = int(request.form['number_of_runs'])
        runners[case_num] = DMRunner(number_of_runs=number_of_runs)
        runners[case_num].start()
        results[case_num] = []
        return render_template('dm_result_page.html', case_num=case_num)


@dm_blueprint.route('/dm_progress/', methods=["GET"])
def dm_progress():
    case_num = request.args.get("case_num", None)
    if case_num is not None:
        if case_num in runners and runners[case_num]:
            runner = runners[case_num]
            runner.message_lock.acquire()
            results[case_num] = runner.messages
            runner.message_lock.release()
            if results[case_num][-1] == '###ALL FINISHED###':
                del runners[case_num]
        if case_num in results:
            return jsonify(results[case_num])
    return jsonify([])
