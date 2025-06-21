select Payment {
    name,
    type_tag,
    value,
    ignore_in_totals,
    interest,
    penalty,
    category_tag,
    subcategory_tag,
    payment_date,
    is_due,
    status,
    account:{
        id,
        account_name,
    },
    event: {
        id,
        date,
    },
    movement:{id}
} filter .id = <uuid>$payment
