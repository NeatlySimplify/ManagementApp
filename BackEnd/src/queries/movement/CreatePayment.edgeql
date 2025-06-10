insert Payment {
    name:= <str>$name,
    value:=to_decimal(<str>$value, 'FM999999999999.99'),
    interest:= <optional str>$interest,
    penalty:= <optional str>$penalty,
    ignore_in_totals:= <optional bool>$ignore_in_totals,
    category:= <str>$category,
    subcategory:= <optional str>$subcategory,
    payment_date:= <optional cal::local_date>$payment_date ?? <cal::local_date>$is_due,
    is_due:= <cal::local_date>$is_due,
    status:= <bool>$status,
    account:= assert_single((select BankAccount filter .id = <uuid>$account)),
    user:= assert_single((select InternalUser filter .id = <uuid>$user)),
    movement:= assert_single((select Movement filter .id = <uuid>$movement))
}
