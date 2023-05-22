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

from Solver import Solver


with open("config.yml", "r") as f:
    config = yaml.safe_load(f)
    client_id = config["client_id"]
    client_secret = config["client_secret"]
    my_api_key = config["my_api_key"]


class QuantumAnnealingAlgorithm(Solver):

    def __init__(self):
        super().__init__()
        pass

    def solve(self, **kwargs):

        # Define API endpoint and parameters
        # Please replace the client_id and client_secret to yours
        # client_id = "your client id"
        # client_secret = "your client secret"
        # my_api_key = "your api key"

        per_grave = int(kwargs["per_grave"])
        n1 = int(kwargs["n1"])
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
        self.logger.log(cycle)
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
        DA_Solver['num_run'] = int(kwargs['num_run'])
        DA_Solver['num_group'] = int(kwargs['num_group'])
        DA_Solver['num_output_solution'] = int(kwargs['num_output_solution'])
        DA_Solver['gs_level'] = int(kwargs['gs_level'])
        DA_Solver['gs_cutoff'] = int(kwargs['gs_cutoff'])
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
        self.logger.log(job_id)

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
        self.logger.log(solution.json())
        while (solution.json()["status"] == "Running" or solution.json()[
               "status"] == "Waiting"):
            solution = requests.get(
                url + "/da/v3/async/jobs/result/" + job_id,
                headers=solution_header)
            self.logger.log(solution.json()['status'] + "...")
            time.sleep(30)

        if solution.json()["qubo_solution"]["result_status"]:
            self.logger.log(solution.json()["qubo_solution"]["result_status"])
        else:
            self.logger.log("FALSE")

        solve_time = solution.json()["qubo_solution"]["timing"]["solve_time"]

        data = []
        solutions = []
        qubo_solution = solution.json()['qubo_solution']
        for i in range(len(qubo_solution['solutions'])):
            configuration = qubo_solution['solutions'][i]['configuration']
            solution_dict = {}
            for j in var:
                if configuration[str(var.index(j))]:
                    solution_dict[j] = 1
                else:
                    solution_dict[j] = 0
            dec = model.decode_sample(solution_dict, vartype='BINARY')
            constraints = dec.constraints()
            self.logger.log(constraints)
            constraints1 = {}
            for key, value in constraints.items():
                constraints1[key] = value[1]
            pyqubo_energy = dec.energy                

            solve_energy = qubo_solution["solutions"][i]["energy"]
            self.logger.log(solve_time, solve_energy + offset)
            instance = {
                "job_id" : job_id,
                "per_grave": per_grave,
                "shift_grave": n1,
                'num_var': len(var),
                'weekdayleave': constraints1['weekdayleave'],
                'eachshift': constraints1['eachshift'],
                'kdays': constraints1['kdays'],
                '2days': constraints1['2days'],
                "solve_energy": solve_energy,
                "offest": offset,
                "energy+offest": solve_energy + offset,
                "pyqubo_energy": pyqubo_energy,
                "solve_time": solve_time,
                "time_limit_sec": time_limit_sec,
                "penalty_coef": penalty_coef,
                "gs_level" : int(kwargs['gs_level']),
                "gs_cutoff" : int(kwargs['gs_cutoff']),
            } 
            data.append(instance)
            solutions.append(solution_dict)
        

        # 儲存的資料夾
        with open('./jobs/result' + job_id + '.json', 'w') as f:
            # json.dump(json.dumps(problem_body, default=int), f, indent=4)
            json.dump(solution.json(), f, indent=4)

        # delete job id

        response_delete = requests.delete(
            url + "/da/v3/async/jobs/result/" + job_id,
            headers=solution_header)
        # self.logger.log(response_delete.json())
        self.logger.log(job_id + " is deleted")

        return solutions, pd.DataFrame(data)
