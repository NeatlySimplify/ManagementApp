select BankAccount {
    bank_name,
    account_name,
    type_account:= .type,
    balance,
    notes,
    ignore_on_totals,
    category,
} filter .id = <uuid>$bank_account
