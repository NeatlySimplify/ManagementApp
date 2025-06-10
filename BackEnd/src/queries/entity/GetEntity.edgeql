select Entity {
    email,
    type,
    id_type,
    status,
    govt_id,
    name,
    sex,
    relationship_status,
    details: {*},
    birth,
    phone: {*, number:{*}},
    address: {*}
} filter .id = <uuid>$entity
