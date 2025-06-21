select Movement{
    type_tag,
    value,
    installment,
    notes,
    record: {
        id,
        name,
        service_id
    },
    accounts:{
        id,
        account_name
    },
    payment: {
        id,
        name,
        status,
        value,
        payment_date,
        is_due,
    }
} filter .id = <uuid>$movement
