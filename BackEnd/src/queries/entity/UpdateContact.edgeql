update Contact filter .id = <uuid>$contact set{
    name:= <optional str>$name ?? .name,
    email:= <optional str>$email ?? .email,
    notes:=<optional json>$notes ?? .notes,
    number:= <optional json>$number ?? .number,
}
