class Optimizer:
    def __init__(self, longdata):
        self.longdata = longdata
        self.cache = {}


    def optimize_season(self, week_start = 1, week_end = 17, blocked_teams = []):
        import numpy as np
        import pandas as pd
        import cvxpy as cp
        # we need to tuple blocked_teams because a list can't be hashed
        args = (week_start, week_end, tuple(blocked_teams))
        if args in self.cache:
            return self.cache[args]

        teams = self.longdata['team'].drop_duplicates()

        wts = []
        var_mappings = []

        week_range = range(week_start,week_end + 1)

        for wk in week_range:
            for t in teams:
                try:
                    var = self.longdata[(self.longdata.week==wk) & (self.longdata.team==t)]['wp'].values[0]
                except IndexError:
                    var = -1000

                wts.append(var)
                var_mappings.append([wk,t,var])

        weights = cp.Constant(wts)
        selects = cp.Variable(len(teams)*len(week_range), boolean=True)
        var_mappings = pd.DataFrame(var_mappings, columns=['week','team','prob'])

        #Create constraints, setting blocked teams == zero and included teams to <= 1
        constraints = []

        #Weekly constraints
        for e, wk in enumerate(week_range):
            indices = list(range(32 * e, 32 * (e+1)))
            constraints.append(sum(selects[indices]) == 1)

        #Team constraints
        for e,t in enumerate(teams):
            indices = [x + e for x in np.multiply(32,range(len(week_range)))]

            if t in blocked_teams:
                constraints.append(sum(selects[indices]) == 0)
            else:
                constraints.append(sum(selects[indices]) <= 1)

        #Create the objective function, problem, and optimize
        obj = cp.Maximize(np.multiply(weights,selects))
        prob = cp.Problem(obj,constraints)
        prob.solve()

        results = pd.DataFrame(columns=['week','team','prob'])
        for e,variable in enumerate(prob.variables()[0]):
            if np.round(variable.value)==1:
                results = results.append(var_mappings.iloc[e])

        self.cache[args] = results
        return results
