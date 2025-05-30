update Contact filter .id = <uuid>$contact set{
    number:= <optional json>$number ?? .number,
    name:= <optional str>$name ?? .name,
    details:= <optional json>$details ?? .details,
    email:= <optional str>$email ?? .email
}
