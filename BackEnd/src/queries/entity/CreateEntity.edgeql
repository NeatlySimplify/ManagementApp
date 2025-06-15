select (insert Entity {
    user:= <InternalUser><uuid>$user,
    email:= <str>$email,
    type:= <str>$type,
    id_type:= <str>$id_type,
    status:= <optional bool>$status,
    govt_id:= <str>$govt_id,
    name:= <str>$name,
    sex:= <optional str>$sex,
    notes:=<optional json>$notes,
    relationship_status:= <optional str>$relationship_status,
    birth:= <optional cal::local_date>$birth
}){id}
