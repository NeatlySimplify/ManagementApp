select Record {
    name,
    id_service,
    active,
    status,
    type,
    str_value:=to_str(.value),
    details: {*},
    entity: {
        id,
        name,
    },
    event: {
        id,
        name,
        type,
        status,
        date
    },
    movement: {
        id,
        type,
        str_value:=to_str(.value),
        installment,
    }
} filter .id = <uuid>$id
