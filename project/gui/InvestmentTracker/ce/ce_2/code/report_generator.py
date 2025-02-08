def generate_report(investments):
    report = "Investment Report:\n"
    total_amount = sum(investment.amount for investment in investments)
    report += f"Total Investment Amount: {total_amount}\n"
    report += "Details:\n"
    for investment in investments:
        report += f"{investment.name} | {investment.type} | {investment.amount} | {investment.date}\n"
    return report