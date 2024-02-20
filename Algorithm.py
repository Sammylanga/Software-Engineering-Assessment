
def percentage_allocation(assets,percentages,asset_cap):

    sum_pec = 1.0
    total_assets = len(percentages)

    if asset_cap < 1/total_assets:
        for i in range(total_assets):
            assets[i].append(False)
            assets[i].append((1/total_assets)*100)
        return assets

    for i in range(total_assets):
        if percentages[i] > asset_cap :
            assets[i].append(False)
            assets[i].append(asset_cap*100)
            sum_pec -= asset_cap
        else :
            assets[i].append(True)
            assets[i].append(percentages[i]*100)

    if sum_pec == 1:
        return assets

    new_total_m_cap = sum(asset[1] for asset in assets if asset[3])
    new_percentages = [asset[1] / new_total_m_cap for asset in assets if asset[3]]
    
    index = 0
    for i in range(total_assets):
        if assets[i][3]: 
            assets[i][4] = sum_pec*new_percentages[index]*100
            index += 1

    return assets


def rebalance_crypto_index_fund(assets, total_capital,asset_cap):
    total_m_cap = sum(asset[1] for asset in assets)
    percentages = [asset[1] / total_m_cap for asset in assets]
    percentage_allocation(assets, percentages, asset_cap)

    print("             Amount      USD Value                          %")

    for i in range(len(assets)):
        assets[i][3] = (assets[i][4]/100) * total_capital/10 # made an assumptions that we use 10% of the total capital seems that out of 10,000  1,000 was used 
        assets[i][2] = assets[i][3]/assets[i][2]
        
        print(f'{assets[i][0]} { assets[i][2]} {assets[i][3]}   {assets[i][4]}      ')

    return 1

#input example 
assets = [
    ["BTC", 20000, 50],
    ["ETH", 10000, 25],
    ["LTC", 5000, 10]
]

total_capital = 10000
asset_cap = 0.5

rebalance_crypto_index_fund(assets, total_capital, asset_cap)
