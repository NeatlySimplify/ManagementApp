with new_account:= <optional uuid>$account,
bank_account := (select BankAccount filter .id = new_account) if exists new_account else {},
update Payment filter .id = <uuid>$payment_id set {
    name:= <optional str>$name ?? .name,
    value:= <optional decimal>$value ?? .value,
    interest:= <optional float64>$interest ?? .interest,
    penalty:= <optional decimal>$penalty ?? .penalty,
    ignore_in_totals:= <optional bool>$ignore_in_totals ?? .ignore_in_totals,
    category:= <optional str>$category ?? .category,
    subcategory:= <optional str>$subcategory ?? .subcategory,
    payment_date:= <optional cal::local_date>$paymentDate ?? .payment_date,
    is_due:= <optional cal::local_date>$is_due ?? .is_due,
    status:= <optional bool>$status ?? .status,
    account:= bank_account ?? .account

}
