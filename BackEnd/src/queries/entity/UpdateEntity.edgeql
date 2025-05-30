update Entity filter .id = <uuid>$entity set {
    email:= <optional str>$email ?? .email,
    type:= <optional str>$type ?? .type,
    id_type:= <optional str>$id_type ?? .id_type,
    status:= <optional bool>$status ?? .status,
    govt_id:= <optional str>$govt_id ?? .govt_id,
    name:= <optional str>$name ?? .name,
    sex:= <optional str>$sex ?? .sex,
    relationship_status:= <optional str>$relationship_status ?? .relationship_status,
    details:= <optional json>$details ?? .details,
    birth:= <optional cal::local_date>$birth ?? .birth
}
