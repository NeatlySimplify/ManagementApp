with raw_value:= <optional str>$value,
decimal_value:= (to_decimal(raw_value, 'FM999999999999.99') if exists raw_value else <decimal>{})
update Record filter .id = <uuid>$id set {
    name:= <optional str>$name ?? .name,
    id_service := <optional str>$id_service ?? .id_service,
    status := <optional str>$status ?? .status,
    type:= <optional str>$type ?? .type,
    active:= <optional bool>$active ?? .active,
    value := decimal_value ?? .value,
    notes:=<optional json>$notes ?? .notes,
}
