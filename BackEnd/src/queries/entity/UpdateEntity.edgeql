with raw_email:= <optional str>$email,
str_email:=(raw_email if exists raw_email else <str>{}),
old_entity:=(select Entity filter .id = <uuid>$entity)
update old_entity set {
    email:= str_email ?? .email,
    type:= <optional str>$type ?? old_entity.type,
    id_type:= <optional str>$id_type ?? old_entity.id_type,
    status:= <optional bool>$status ?? old_entity.status,
    govt_id:= <optional str>$govt_id ?? old_entity.govt_id,
    name:= <optional str>$name ?? old_entity.name,
    sex:= <optional str>$sex ?? old_entity.sex,
    relationship_status:= <optional str>$relationship_status ?? old_entity.relationship_status,
    birth:= <optional cal::local_date>$birth ?? old_entity.birth
}
