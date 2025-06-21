with old_entity:=(select Entity filter .id = <uuid>$entity)
update old_entity set {
    email:= <optional str>$email ?? .email,
    type_tag:= <optional str>$type_tag ?? .type_tag,
    document_type:= <optional str>$document_type ?? .document_type,
    status:= <optional bool>$status ?? old_entity.status,
    document:= <optional str>$document ?? .document,
    name:= <optional str>$name ?? old_entity.name,
    sex:= <optional str>$sex ?? old_entity.sex,
    relationship_status:= <optional str>$relationship_status ?? old_entity.relationship_status,
    notes:=<optional json>$notes ?? .notes,
    birth:= <optional cal::local_date>$birth ?? old_entity.birth
}
