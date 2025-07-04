select Payment {
    name,
    type_tag,
    value,
    ignore_in_totals,
    category_tag,
    payment_date,
    is_due,
    status,
    account:{
        id,
        account_name,
    },
    event: {
        id,
        date_beginning,
    },
    movement:{id}
} filter .id = <uuid>$payment
