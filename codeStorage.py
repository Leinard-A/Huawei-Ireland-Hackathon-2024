# elif a_dSA < 0: # If value is negative, dismiss servers to meet demand (utilization)
        #     r_dASA = a_dSA * -1 # Remaining Actual Demanded Server Amount
        #     dcInd = []

        #     # Find datacentres with the same latency sensitivity
        #     for i, dc in enumerate(datacentres):
        #         if dc['latency_sensitivity'] == ls:
        #             dcInd.append(i)
            
        #     for i in dcInd:
        #         dc = datacentres[i]
        #         dcID = dc['ID']
        #         s = dc['servers']
        #         currentServers = s.loc[s['server_generation'] == generation] # Find servers the same the current server generation
        #         currentServerAmount = len(currentServers)

        #         if currentServerAmount <= 0:
        #             continue
                
                
        #         amount = 0
        #         if r_dASA <= currentServerAmount:
        #             amount = r_dASA

        #             r_dASA = 0
        #         else:
        #             amount = currentServerAmount

        #             r_dASA -= currentServerAmount
                
        #         dismissedServers = currentServers[:amount]
        #         dismissIndicies = dismissedServers.index.values.tolist()                
        #         datacentres[i]['servers'].drop(dismissIndicies, inplace=True)
        #         datacentres[i]['servers'] = datacentres[i]['servers'].reset_index(drop=True)

        #         dismissedServers = toDF(dismissedServers['server_id'], generation, timeStep, dcID)
        #         actions.extend(actionDict(dismissedServers, 'dismiss', timeStep))

        #         if r_dASA <= 0:
        #             break