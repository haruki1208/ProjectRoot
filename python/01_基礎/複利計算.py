def calculate_compound_interest(monthly_investment, annual_rate, years):
    """
    Calculate the total asset value after investing a fixed amount monthly
    with compound interest over a given number of years.

    :param monthly_investment: Amount invested every month (float)
    :param annual_rate: Annual interest rate in percentage (float)
    :param years: Number of years to invest (int)
    :return: Total asset value after the investment period (float)
    """
    months = years * 12
    monthly_rate = annual_rate / 100 / 12
    total = 0

    for month in range(1, months + 1):
        total = (total + monthly_investment) * (1 + monthly_rate)

    return total

def calculate_monthly_profit(total, monthly_investment, annual_rate):
    
    monthly_rate = annual_rate / 100 / 12
    total = total + monthly_investment
    monthly_profit = total * monthly_rate
    
    return monthly_profit


if __name__ == "__main__":
    try:
        monthly_investment = float(input("毎月の投資額を入力してください（円）: "))
        annual_rate = float(input("年利を入力してください（%）: "))
        years = int(input("投資年数を入力してください: "))

        total_assets = calculate_compound_interest(monthly_investment, annual_rate, years)
        monthly_profit = calculate_monthly_profit(total_assets, monthly_investment, annual_rate) # 1か月の利益

        print(f"{years}年後の資産総額は: {total_assets:,.0f}円です")
        print(f"{years}年後の1か月あたりの利益は: {monthly_profit:,.0f}円です")
    except ValueError:
        print("入力が無効です。数値を入力してください。")