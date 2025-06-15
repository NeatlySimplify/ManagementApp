select (insert Record{
    user:= assert_single((select InternalUser filter .id = <uuid>$user)),
    name:= <str>$name,
    id_service := <optional str>$id_service,
    active:= <optional bool>$active ?? <bool>true,
    status := <optional str>$status,
    type:= <str>$type,
    value := to_decimal(<str>$value, 'FM999999999999.99'),
    notes:=<optional json>$notes,
    entity := assert_single((select Entity filter .id = <uuid>$entity))
}){
    id
}
