def optimize_season(week_start = 1, week_end = 17, blocked_teams = [], ):
    blocked_teams = ['BAL','DAL','PHI','NYG','CIN']
    week_start = 6 #inclusive
    week_end = 15 #inclusive
    wts = []
    selects = []
    var_mappings = []

    week_range = range(week_start,week_end + 1)

    for wk in week_range:
        for t in teams:
            try:
                var = longdata[(longdata.week==wk) & (longdata.team==t)]['wp'].values[0]
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