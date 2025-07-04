with isit:= <cal::local_date>$is_due,
event_:=(insert Scheduler{
    name:=<str>$name,
    date_beginning:=cal::to_local_datetime(<str>isit),
    status:=<bool>$status,
}),
insert Payment {
    name:= <str>$name,
    type_tag:=<str>$type_tag,
    value:=to_decimal(<str>$value, 'FM999999999999D99'),
    ignore_in_totals:= <optional bool>$ignore_in_totals,
    category_tag:= <str>$category,
    payment_date:= <optional cal::local_date>$payment_date ?? isit,
    is_due:= isit,
    status:= <bool>$status,
    account:= assert_single((select BankAccount filter .id = <uuid>$account)),
    movement:= assert_single((select Movement filter .id = <uuid>$movement)),
    event:=event_,
}
