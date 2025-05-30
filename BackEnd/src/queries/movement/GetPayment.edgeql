select Payment {
    name,
    type,
    value,
    ignore_in_totals,
    interest,
    penalty,
    category,
    subcategory,
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
