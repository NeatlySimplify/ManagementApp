update Contact filter .id = <uuid>$contact set{
    name:= <optional str>$name ?? .name,
    email:= <optional str>$email ?? .email
}
