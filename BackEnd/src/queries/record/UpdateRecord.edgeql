with raw_value:= <optional str>$value,
decimal_value:= (to_decimal(raw_value, 'FM999999999999.99') if exists raw_value else <decimal>{})
update Record filter .id = <uuid>$id set {
    name:= <optional str>$name ?? .name,
    service_id := <optional str>$service_id ?? .service_id,
    status := <optional bool>$status ?? .status,
    type_tag:= <optional str>$type ?? .type_tag,
    optional_status:= <optional str>$optional_status ?? .optional_status,
    value := decimal_value ?? .value,
    notes:=<optional json>$notes ?? .notes,
}
