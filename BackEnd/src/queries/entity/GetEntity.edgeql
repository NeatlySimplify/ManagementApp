select Entity {
    email,
    type_entity:= .type,
    id_type,
    status,
    govt_id,
    name,
    sex,
    relationship_status,
    notes,
    birth,
    phone: {*},
    address: {*}
} filter .id = <uuid>$entity
