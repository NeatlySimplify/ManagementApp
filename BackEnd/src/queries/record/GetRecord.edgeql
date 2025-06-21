select Record {
    name,
    service_id,
    status,
    optional_status,
    type_tag,
    str_value:=to_str(.value),
    notes,
    entity: {
        id,
        name,
    },
    event: {
        id,
        name,
        type_tag,
        status,
        date
    },
    movement: {
        id,
        type_tag,
        str_value:=to_str(.value),
        installment,
        payment: {
            id,
            status,
            payment_date
        }
    }
} filter .id = <uuid>$id
