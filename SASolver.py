from pyqubo import Constraint, Array, And, Or, Not
from util import getWeekendDate

import numpy as np
import pandas as pd

import neal
import time
import calendar
from console import Logger


class SimulatedAnnealingAlgorithm(object):

    def __init__(self):
        self.shift_name = ['Graveyard', 'Night', 'Day']
        self.sampler = neal.SimulatedAnnealingSampler()

        self.logger = Logger()
   
    def solve(self, **kwargs):

        per_grave = int(kwargs["per_grave"])
        n1 = int(kwargs["n1"])
        k = int(kwargs["k"])
        num_sweeps = int(kwargs["num_sweeps"]) 
        year = int(kwargs["year"])
        month = int(kwargs["month"])
        lmda = float(kwargs["lmda"])
        lmdb = float(kwargs["lmdb"])
        lmdc = float(kwargs["lmdc"])
        lmdd = float(kwargs["lmdd"])
        lmde = float(kwargs["lmde"])

        days = calendar.monthrange(year, month)[1]
        weekend = getWeekendDate(year, month)

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

        # Number of workers in each day
        whole_shift = []
        for i in range(days):
            col_sum = 0  # sum of each column
            for j in range(per_grave):
                col_sum = col_sum + X[j][i]
            whole_shift.append(col_sum)

        # k+1 days sum
        shift_kd = []
        for i in range(per_grave):
            per_sumkd = []
            for j in range(days - k):
                temp = sum(X[i][p] for p in range(j, j + k + 1))
                per_sumkd.append(temp)
            shift_kd.append(per_sumkd)

        # Limit of workers in each shift-period

        Ha = sum((whole_shift[i] - n1)**2 for i in range(days))

        # Limit of 2 - 5 days each cycle

        Hb = 0
        # the cycle of shift_kd would be (per_grave, days - k)
        cycle = len(shift_kd[0])
        self.logger.log(cycle)
        slack = Array.create(
            "slack",
            shape=(
                per_grave,
                cycle * k),
            vartype="BINARY")
        for i in range(per_grave):
            for j in range(cycle):
                # To adapt the condition k is not equal to 4, a for-loop needed
                Hb = Hb + (shift_kd[i][j] - sum(slack[i][l]
                           for l in range(k * j, k * j + k)))**2

        Hc = 0
        for i in range(per_grave):
            for j in range(days - 2):
                Hc = Hc + And(X[i][j + 1], 1 - Or(X[i][j], X[i][j + 2]))
            Hc = Hc + (And(X[i][0], Not(X[i][1]))) + \
                (And(X[i][days - 1], Not(X[i][days - 2])))

        # a weekday leave

        He = 0
        week_slack = Array.create(
            "slack2", shape=(
                per_grave, days), vartype="BINARY")

        for j in range(per_grave):
            for i in weekend[::2]:
                if i + 7 < days:
                    He = He + (sum(X[j][l] for l in range(i, i + 7)) -
                               sum(week_slack[j][l] for l in range(i, i + 5)))**2
                elif i + 5 < days and i + 7 > days:
                    He = He + (sum(X[j][l] for l in range(i, days)) -
                               sum(week_slack[j][l] for l in range(i, i + 5)))**2

        # Continuously 2-days leaves optimization

        Hd = 0
        for i in range(per_grave):
            for j in range(days - 1):
                Hd = Hd + (1 - X[i][j] * X[i][j + 1])

        # The Hamiltonian
        # H = lmda*Constraint(Ha,"eachshift") + lmdc*Constraint(Hb,"kdays") + lmdc*Constraint(Hc, "2days") + lmde*Constraint(He,"weekdayleave")
        H = lmda * Constraint(Ha,
                              "eachshift") + lmdc * Constraint(Hb,
                                                               "kdays") + lmdc * Constraint(Hc,
                                                                                            "2days") + lmde * Constraint(He,
                                                                                                                         "weekdayleave")
        model = H.compile()
        bqm = model.to_bqm()
        var = model.variables
        self.logger.log(len(var))

        data = []

        for i in range(10):
            start_time = time.process_time()
            sampleset = self.sampler.sample(
                bqm, num_reads=10, num_sweeps=num_sweeps)
            decoded_samples = model.decode_sampleset(sampleset)
            graveyard_sampleset = min(decoded_samples, key=lambda s: s.energy)
            graveyard_record = graveyard_sampleset.sample
            dec = model.decode_sample(graveyard_record, vartype='BINARY')
            end_time = time.process_time()
            process_time1 = end_time - start_time
            energy = dec.energy
            constraints = dec.constraints()
            self.logger.log(constraints)
            constraints1 = {}
            for key, value in constraints.items():
                constraints1[key] = value[1]
            # enter the data
            data_everytime = [
                per_grave,
                n1,
                len(var),
                energy,
                constraints1['weekdayleave'],
                constraints1['eachshift'],
                constraints1['kdays'],
                constraints1['2days'],
                process_time1,
                num_sweeps]
            data.append(data_everytime)

        # Output the DataFrame
        # Generate the empty shift table and lables
        label = [
            'per_grave',
            'shift_grave',
            'num_var',
            'energy',
            'weekdayleave',
            'eachshift',
            'kdays',
            '2days',
            'process_time',
            'num_sweeps']
        df = pd.DataFrame(data, columns=label)
        df = df.applymap(str)
        # filename = 'Graveyard_shift.csv'
        # df.to_csv(filename, index=False, quoting=csv.QUOTE_NONNUMERIC)

        graveyard_list = list(range(per_grave))
        graveyard_table = np.zeros(per_grave * days)
        for key, value in graveyard_record.items():
            if "Graveyard" in key and "*" not in key:
                newkey = int(key.replace("Graveyard[", "").replace("]", ""))
                graveyard_table[newkey] = value
        graveyard_table = graveyard_table.reshape(per_grave, days).astype(int)
        graveyard_dic = {
            graveyard_list[i]: graveyard_table[i].tolist() for i in range(per_grave)}

        self.logger.log(graveyard_table)

        self.shift_result = graveyard_table
        self.algorithm_data = data

        return pd.DataFrame(
            graveyard_table, columns=[
                str(i) for i in range(
                    1, days + 1)]), df
