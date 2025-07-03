insert Record{
    name:= <str>$name,
    service_id := <optional str>$id_service,
    status:= <optional bool>$status ?? <bool>true,
    optional_status := <optional str>$optional_status,
    type_tag:= <str>$type_tag,
    value := to_decimal(<str>$value, 'FM999999999999.99'),
    notes:=<optional json>$notes,
    entity := (select Entity filter .id in array_unpack(<array<uuid>>$entities))
}
