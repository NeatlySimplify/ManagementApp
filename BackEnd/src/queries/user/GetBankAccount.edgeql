select BankAccount {
    bank_name,
    account_name,
    type_tag,
    balance,
    notes,
    ignore_on_totals,
    category_tag,
} filter .id = <uuid>$bank_account
