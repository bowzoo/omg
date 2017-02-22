import mortgage

import click
import decimal

"""
zchao@Syrup:~/my_shit/omg$ python ./stk_w_mrtg.py -i 3.25 -m 360 -a 380000 -s 6000   100 20 3
Loan Amount: 380000
Yearly Interest Rate: 3.25 %
Months of loan 360
Extra payments for principles: [100.0, 20.0, 3.0]
Stock money for extra payment or stock: 6000
Total Tax Rate 38.5 %
=======================

Monthly payment: 1653.79
Without any extra principle payments:
Total Payout: 595364.40
With extra principle payments: [100.0, 20.0, 3.0]
Total Payout: 595159.42
Total saving: 204.98
=======================

Pay extra 6000 NOW, payout=585630.39, can save another extra 9529.03
After 1 month(s), stock profit return_rate must be >= 00.44 % in order to make even for paying now
After 2 month(s), stock profit return_rate must be >= 00.88 % in order to make even for paying now
After 3 month(s), stock profit return_rate must be >= 01.32 % in order to make even for paying now
After 4 month(s), stock profit return_rate must be >= 01.77 % in order to make even for paying now
After 5 month(s), stock profit return_rate must be >= 02.21 % in order to make even for paying now
After 6 month(s), stock profit return_rate must be >= 02.66 % in order to make even for paying now
After 7 month(s), stock profit return_rate must be >= 03.11 % in order to make even for paying now
After 8 month(s), stock profit return_rate must be >= 03.56 % in order to make even for paying now
After 9 month(s), stock profit return_rate must be >= 04.01 % in order to make even for paying now
After 10 month(s), stock profit return_rate must be >= 04.46 % in order to make even for paying now
After 11 month(s), stock profit return_rate must be >= 04.91 % in order to make even for paying now
"""

@click.command()
@click.option('-a', '--amount', type=int, help='amount of loan')
@click.option('-i', '--interest', type=float, help='% of yearly interest rate')
@click.option('-m', '--months', type=int, help='months')
@click.option('-s', '--stockmoney', type=int, default=0, help='stock money u wanna put')
@click.option('-t', '--tax', type=float, default=38.5, help='total tax rate including both federal and state')
@click.argument('extras', nargs=-1, type=click.UNPROCESSED)
def hellokitty(amount, interest, months, stockmoney, tax, extras):
    extra_ps = [float(p) for p in extras]

    click.echo('Loan Amount: %s' % amount)
    click.echo('Yearly Interest Rate: %s %%' % interest)
    click.echo('Months of loan %s' % months)
    click.echo('Extra payments for principles: %s' % extra_ps)
    click.echo('Stock money for extra payment or stock: %s' % stockmoney)
    click.echo('Total Tax Rate %s %%' % tax)
    click.echo('=======================\n')

    interest = interest/100
    m = mortgage.Mortgage(interest=interest, amount=amount, months=months)
    org_payout = m.total_payout()
    payout_extra = m.total_payout(extra_principle_payments=extra_ps)

    click.echo('Monthly payment: %s' % m.monthly_payment())
    click.echo('Without any extra principle payments:\nTotal Payout: %s' % org_payout)
    click.echo('With extra principle payments: %s\nTotal Payout: %s' % (extra_ps, payout_extra))
    click.echo('Total saving: %s' % (org_payout - payout_extra))
    click.echo('=======================\n')

    if stockmoney != 0:
        extra_payment_w_stockmoney = extra_ps + [stockmoney]
        pay_extra_stock_now_payout = m.total_payout(extra_principle_payments=extra_payment_w_stockmoney)
        click.echo('Pay extra %s NOW, payout=%s, can save another extra %s' % ( stockmoney, pay_extra_stock_now_payout, payout_extra -pay_extra_stock_now_payout))

        monthly_payments_w_stockmoney = list(m.monthly_payment_schedule(extra_principle_payments=extra_payment_w_stockmoney))
        monthly_payments = list(m.monthly_payment_schedule(extra_principle_payments=extra_ps))

        for n in xrange(1,12):
            _, _, _, balance_w_stockmoney = monthly_payments_w_stockmoney[len(extra_ps) + n] # principle, interest, extra_principle, blance
            _, _, _, balance = monthly_payments[len(extra_ps) + n]

            min_return_rate = (balance - balance_w_stockmoney - decimal.Decimal(stockmoney))/decimal.Decimal(stockmoney)/decimal.Decimal(1-tax/100)
            click.echo('After %s month(s), stock profit return_rate must be >= %05.2f %% in order to make even for paying now' % (n, min_return_rate *100))

if __name__ == '__main__':
    hellokitty()
