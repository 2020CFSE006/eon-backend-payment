PAYMENT_CONSTANTS = dict(
    status=[(0, "CREDIT"), (3, "REFUND")],
    values=dict(
        status=dict(CREDIT=0, REFUND=3),
    ),
)
APPLICATION_CONSTANTS = dict(transaction=PAYMENT_CONSTANTS)
