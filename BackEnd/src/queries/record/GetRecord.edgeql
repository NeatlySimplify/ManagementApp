select Record {
    name,
    id_service,
    active,
    status,
    type_record:= .type,
    str_value:=to_str(.value),
    notes,
    entity: {
        id,
        name,
    },
    event: {
        id,
        name,
        type_entry:= .type,
        status,
        date
    },
    movement: {
        id,
        type_movement:= .type,
        str_value:=to_str(.value),
        installment,
        payment: {
            id,
            status,
            payment_date
        }
    }
} filter .id = <uuid>$id
