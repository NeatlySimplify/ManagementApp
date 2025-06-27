update Contact filter .id = <uuid>$contact set{
    type_tag:= <optional str>$type_tag ?? .type_tag,
    complement:=<optional str>$notes ?? .complement,
    number:= <optional str>$number ?? .number,
}
