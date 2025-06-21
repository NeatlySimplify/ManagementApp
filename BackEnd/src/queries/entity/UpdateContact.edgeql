update Contact filter .id = <uuid>$contact set{
    type_tag:= <optional str>$type_tag ?? .type_tag,
    extra_email:= <optional str>$extra_email ?? .extra_email,
    notes:=<optional json>$notes ?? .notes,
    number:= <optional str>$number ?? .number,
}
