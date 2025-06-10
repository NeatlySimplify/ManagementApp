select Movement{
    type,
    value,
    installment,
    details: {*},
    record: {
        id,
        name,
        id_service
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
