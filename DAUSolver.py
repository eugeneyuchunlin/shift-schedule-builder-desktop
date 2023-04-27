from datetime import datetime
from pyqubo import Binary, Constraint, Placeholder, Array, And, Or, Not
from pytz import timezone
from util import getWeekendDate

import numpy as np
import pandas as pd

import requests
import base64
import time
import json
import yaml
import calendar



with open("config.yml", "r") as f:
    config = yaml.safe_load(f)
    client_id = config["client_id"]
    client_secret = config["client_secret"]
    my_api_key = config["my_api_key"]



class QuantumAnnealingAlgorithm(object):

    def __init__(self):

        pass

    def solve(self, **kwargs):

        # Define API endpoint and parameters
        # Please replace the client_id and client_secret to yours
        # client_id = "your client id"
        # client_secret = "your client secret"
        # my_api_key = "your api key"

        per_grave = int(kwargs["per_grave"])
        per_num = int(kwargs["per_num"])
        per_night = int(kwargs["per_night"])
        n1 = int(kwargs["n1"])
        n2 = int(kwargs["n2"])
        n = int(kwargs["n"])
        k = int(kwargs["k"])
        year = int(kwargs["year"])
        month = int(kwargs["month"])
        lmda = float(kwargs["lmda"])
        lmdb = float(kwargs["lmdb"])
        lmdc = float(kwargs["lmdc"])
        lmdd = float(kwargs["lmdd"])
        lmde = float(kwargs["lmde"])
        time_limit_sec = int(kwargs["time_limit_sec"])
        penalty_coef = int(kwargs["penalty_coef"])
        

        url = "https://api.aispf.global.fujitsu.com"

        request_body = {
            "grant_type": "client_credentials"
        }

        # Encode client_id and client_secret in Base64 for Authorization header
        client_str = client_id + ":" + client_secret
        client_b64 = base64.b64encode(
            client_str.encode('utf-8')).decode('utf-8')

        # Define headers with required Content-Type and Accept headers
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "Authorization": "Basic " + client_b64
        }

        # Send POST request to API with request_body, headers
        response = requests.post(
            url + "/auth/v2/tokens",
            headers=headers,
            data=request_body)  # , auth=(client_id, client_secret))

        # Extract token from API response and store in JSON file
        token = response.json()['access_token']

        # Put the token in the later query
        print(token)

        # setup

        # Kinds of shift
        shift_name = ['Graveyard', 'Night', 'Day']

        # Number of person, period length
        firstday, days = calendar.monthrange(year, month)

        if firstday == 6:
            firstSat = 6
            firstSun = 0
        else:
            firstSat = int(5 - firstday)
            firstSun = firstSat + 1
        weekend = []
        for i in range(days):
            if i % 7 == firstSat or i % 7 == firstSun:
                weekend.append(i)

        # m1, m2: the numbers of nurses on duty each month for graveyard shifts and night shifts
        # n1, n2: the numbers of nurses on duty per day for graveyard shifts and
        # night shifts

        # k: the max number of consecutive graveyard shifts and of consecutive
        # night shifts

        # n: the numbers of nurses on duty each pay
        # n3: the numbers of nurses on duty per day for day shifts
        n3 = n - n1 - n2

        # Grouping
        group = list(range(per_num))
        graveyard_list = group[:per_grave]
        night_list = group[per_grave:per_grave + per_night]
        day_list = group[per_grave + per_night:]

        # Graveyard shift
        # Generate Binary table of Graveyard shift

        X_initial = Array.create(
            "Graveyard",
            shape=per_grave * days,
            vartype="BINARY")
        X = np.zeros(per_grave * days).reshape(per_grave, days)
        X = X.tolist()
        for i in range(per_grave):
            for j in range(days):
                X[i][j] = X_initial[days * i + j]

        # Number of workers in each shift-period
        total_shift = []
        for i in range(days):
            col_sum = 0
            for j in range(per_grave):
                col_sum = col_sum + X[j][i]
            total_shift.append(col_sum)

        # k+1 days sum
        shift_kd = []
        for i in range(per_grave):
            per_sumkd = []
            for j in range(days - k):
                temp = sum(X[i][p] for p in range(j, j + k + 1))
                per_sumkd.append(temp)
            shift_kd.append(per_sumkd)

        # Limit of workers in each shift-period
        lmda = 1.5
        Ha = sum((total_shift[i] - n1)**2 for i in range(days))

        # Limit of 2 - 5 days each cycle
        lmdb = 0.5
        Hb = 0
        cycle = len(shift_kd[0])
        print(cycle)
        slack_initial = Array.create(
            "slack1",
            shape=per_grave * cycle * k,
            vartype="BINARY")
        slack = np.zeros(per_grave * cycle * k).reshape(per_grave, cycle * k)
        slack = slack.tolist()

        for i in range(per_grave):
            for j in range(cycle * k):
                slack[i][j] = slack_initial[cycle * k * i + j]

        for i in range(per_grave):
            for j in range(cycle):
                # To adapt the condition k is not equal to 4, a for-loop needed
                Hb = Hb + (shift_kd[i][j] - sum(slack[i][l]
                                                for l in range(k * j, k * j + k)))**2

        lmdc = 0.5
        Hc = 0
        for i in range(per_grave):
            for j in range(days - 2):
                Hc = Hc + And(X[i][j + 1], 1 - Or(X[i][j], X[i][j + 2]))
            Hc = Hc + (And(X[i][0], Not(X[i][1]))) + \
                (And(X[i][days - 1], Not(X[i][days - 2])))

        # a weekday leave
        lmde = 0.5
        He = 0
        week_slack_initial = Array.create(
            "slack2",
            shape=per_grave * days,
            vartype="BINARY")
        week_slack = np.zeros(per_grave * days).reshape(per_grave, days)
        week_slack = week_slack.tolist()
        for i in range(per_grave):
            for j in range(days):
                week_slack[i][j] = week_slack_initial[days * i + j]
        for j in range(per_grave):
            for i in weekend[::2]:
                if i + 7 < days:
                    He = He + (sum(X[j][l] for l in range(i, i + 7)) -
                               sum(week_slack[j][l] for l in range(i, i + 5)))**2
                elif i + 5 < days and i + 7 > days:
                    He = He + (sum(X[j][l] for l in range(i, days)) -
                               sum(week_slack[j][l] for l in range(i, i + 5)))**2

        # Continuously 2-days leaves optimization

        lmdd = 0.1
        Hd = 0
        for i in range(per_grave):
            for j in range(days - 1):
                Hd = Hd + (1 - X[i][j] * X[i][j + 1])

        # H = lmda*Constraint(Ha,"eachshift") + lmdb*Constraint(Hb,"kdays") + lmde*Constraint(He,"weekdayleave")
        H = lmda * Constraint(Ha,
                              "eachshift") + lmdb * Constraint(Hb,
                                                               "kdays") + lmdc * Constraint(Hc,
                                                                                            "2days") + lmde * Constraint(He,
                                                                                                                         "weekdayleave")
        model = H.compile()
        bqm = model.to_bqm()

        qubo = model.to_qubo()
        bqm_dict = qubo[0]
        offset = qubo[1]
        var = model.variables
        Matrix_term = []
        for key, value in bqm_dict.items():
            terms = {}
            terms["coefficient"] = value
            terms["polynomials"] = [0, 0]
            for i in range(2):
                terms["polynomials"][i] = var.index(key[i])
            Matrix_term.append(terms)

        bin_poly = {}
        bin_poly["terms"] = Matrix_term
        problem_body = {}
        DA_Solver = {}
        DA_Solver["time_limit_sec"] = time_limit_sec
        DA_Solver["penalty_coef"] = penalty_coef
        problem_body["fujitsuDA3"] = DA_Solver
        problem_body["binary_polynomial"] = bin_poly

        problem_header = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            # "X-Access-Token": token
            "X-Api-Key": my_api_key
        }
        # print(json.dumps(problem_header,indent=4))

        # Submit the job and get the job_id
        # print(json.dumps(problem_body, indent=4))
        response = requests.post(
            url + "/da/v3/async/qubo/solve",
            headers=problem_header,
            data=json.dumps(
                problem_body,
                default=int))  # json.dumps(problem_body,indent=4,default=int))

        job_id = response.json()['job_id']
        print(job_id)

        solution_header = {
            "Job_ID": job_id,
            "Accept": "application/json",
            # "X-Access-Token": token
            "X-Api-Key": my_api_key
        }
        # print(solution_header)

        # polling the result

        solution = requests.get(
            url + "/da/v3/async/jobs/result/" + job_id,
            headers=solution_header)
        print(solution.json())
        while (solution.json()["status"] == "Running" or solution.json()[
               "status"] == "Waiting"):
            solution = requests.get(
                url + "/da/v3/async/jobs/result/" + job_id,
                headers=solution_header)
            print(solution.json()['status'] + "...")
            time.sleep(5)

        if solution.json()["qubo_solution"]["result_status"]:
            print(solution.json()["qubo_solution"]["result_status"])
        else:
            print("FALSE")

        solve_time = solution.json()["qubo_solution"]["timing"]["solve_time"]
        solve_energy = solution.json(
        )["qubo_solution"]["solutions"][0]["energy"]
        print(solve_time, solve_energy + offset)

        solution_set = solution.json()["qubo_solution"]["solutions"][0]
        solution_configuration = solution_set['configuration']
        solution_dict = {}
        for i in var:
            if solution_configuration[str(var.index(i))]:
                solution_dict[i] = 1
            else:
                solution_dict[i] = 0
        decoded_sample2 = model.decode_sample(solution_dict, vartype='BINARY')
        print(type(decoded_sample2))
        print(decoded_sample2.energy, decoded_sample2.constraints())
        print(solution_dict)

        graveyard_list = list(range(per_grave))
        graveyard_table = np.zeros(per_grave * days)
        for key, value in solution_dict.items():
            if "Graveyard" in key and "*" not in key:
                newkey = int(key.replace("Graveyard[", "").replace("]", ""))
                graveyard_table[newkey] = value
        graveyard_table = graveyard_table.reshape(per_grave, days).astype(int)
        graveyard_dic = {graveyard_list[i]: graveyard_table[i].tolist()
                         for i in range(per_grave)}

        print(graveyard_table)

        # 下面的google drive路徑要自己改成你想要儲存的資料夾
        with open('./jobs/result' + job_id + '.json', 'w') as f:
            # json.dump(json.dumps(problem_body, default=int), f, indent=4)
            json.dump(solution.json(), f, indent=4)

        # delete job id

        response_delete = requests.delete(
            url + "/da/v3/async/jobs/result/" + job_id,
            headers=solution_header)
        # print(response_delete.json())
        print(job_id + " is deleted")

        # If you want to list all the jobs, use the following
        # Please delete the job if the job is finished and you had downloaded
        # the result

        job_list = requests.get(
            url + "/da/v3/async/jobs",
            headers=problem_header)
        print(job_list.json())

        # Save the results in job list
        response_dict = json.loads(json.dumps(job_list.json()))

        # 設定台灣時區
        tz = timezone('Asia/Taipei')

        # 遍歷物件取出資料
        for job_status in response_dict['job_status_list']:
            job_id = job_status['job_id']
            status = job_status['job_status']
            start_time_utc = datetime.strptime(
                job_status['start_time'], '%Y-%m-%dT%H:%M:%SZ')
            start_time_tw = start_time_utc.astimezone(tz)
            print('Job ID:', job_id)
            print('Job Status:', status)
            # print('Start Time (UTC):', start_time_utc)
            print('Start Time (TW):', start_time_tw)
            print()  # 空行分隔
            job_txt = {
                'Job ID': job_id,
                'Job Status': status,
                'Start Time': job_status['start_time']
            }
            # output solution as a file
            solution_header = {
                "Job_ID": job_id,
                "Accept": "application/json",
                # "X-Access-Token": token
                "X-Api-Key": my_api_key
            }
            solution = requests.get(
                url + "/da/v3/async/jobs/result/" + job_id,
                headers=solution_header)
            with open('./jobs/result' + job_id + '.json', 'w') as f:
                json.dump(json.loads(json.dumps(job_txt)), f, indent=4)
                json.dump(solution.json(), f, indent=4)

        data = [
            per_grave,
            n1,
            k,
            year,
            month,
            lmda,
            lmdb,
            lmdc,
            lmdd,
            lmde,
            solve_time,
            solve_energy +
            offset]

        data = {
            "job_id": [job_id],
            "per_grave": [per_grave],
            "n1": [n1],
            "k": [k],
            "solve_energy": [solve_energy],
            "offest": [offset],
            "energy+offest": [solve_energy + offset],
            "solve_time": [solve_time],
        }

        return pd.DataFrame(
            graveyard_table, columns=[
                str(i) for i in range(
                    1, days + 1)]), pd.DataFrame(data)


