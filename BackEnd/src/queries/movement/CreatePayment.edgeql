with user:=(select global current_user_obj),
pay:= (select (insert Payment {
    name:= <str>$name,
    value:=to_decimal(<str>$value, 'FM999999999999D99'),
    interest:= <optional str>$interest,
    penalty:= <optional str>$penalty,
    ignore_in_totals:= <optional bool>$ignore_in_totals,
    category_tag:= <str>$category,
    subcategory_tag:= <optional str>$subcategory,
    payment_date:= <optional cal::local_date>$payment_date ?? <cal::local_date>$is_due,
    is_due:= <cal::local_date>$is_due,
    status:= <bool>$status,
    account:= assert_single((select BankAccount filter .id = <uuid>$account)),
    movement:= assert_single((select Movement filter .id = <uuid>$movement))
}){*}),
pay_event:= (insert Scheduler {
    type_tag:= pay.type_tag,
    name := pay.name,
    date:= pay.is_due,
    owner:= user
}),
pay_update:= (update pay set {
    event:= pay_event
}),
select (user, pay, pay_event, pay_update)
