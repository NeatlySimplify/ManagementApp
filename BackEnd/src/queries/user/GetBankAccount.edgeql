select BankAccount {
    bank_name,
    account_name,
    balance,
    details: {*},
    ignore_on_totals,
    category,
    type
} filter .id = <uuid>$bank_account
