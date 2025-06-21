with user:= (select global current_user_obj),
insert Entity {
    name:= <str>$name,
    email:= <str>$email,
    type_tag:= <str>$type_tag,
    document_type:= <str>$document_type,
    document:= <str>$document,
    status:= <optional bool>$status,
    sex:= <optional str>$sex,
    notes:=<optional json>$notes,
    relationship_status:= <optional str>$relationship_status,
    birth:= <optional cal::local_date>$birth,
    owner:= user
}
