with new_account:= <optional uuid>$account,
bank_account := (select BankAccount filter .id = new_account) if exists new_account else <BankAccount>{},
raw_value:= <optional str>$value,
decimal_value:= (to_decimal(raw_value, 'FM999999999999.99') if exists raw_value else <decimal>{})
update Payment filter .id = <uuid>$payment_id set {
    name:= <optional str>$name ?? .name,
    value:= decimal_value ?? .value,
    interest:= <optional str>$interest ?? .interest,
    penalty:= <optional str>$penalty ?? .penalty,
    ignore_in_totals:= <optional bool>$ignore_in_totals ?? .ignore_in_totals,
    category:= <optional str>$category ?? .category,
    subcategory:= <optional str>$subcategory ?? .subcategory,
    payment_date:= <optional cal::local_date>$paymentDate ?? .payment_date,
    is_due:= <optional cal::local_date>$is_due ?? .is_due,
    status:= <optional bool>$status ?? .status,
    account:= bank_account ?? .account
}
