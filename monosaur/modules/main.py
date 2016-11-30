from ofxparse import OfxParser

with open('statements/nd-amex-sample.ofx', mode='rb') as fileobj:
    ofx = OfxParser.parse(fileobj)

for transaction in ofx.account.statement.transactions:

    print(transaction.date)
    print(transaction.payee)
    print(transaction.amount)
