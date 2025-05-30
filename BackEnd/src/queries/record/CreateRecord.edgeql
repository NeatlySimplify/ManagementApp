select (insert Record{
    user:= assert_single((select InternalUser filter .id = <uuid>$user)),
    name:= <str>$name,
    id_service := <optional str>$id_service,
    active:= <optional bool>$active ?? <bool>true,
    status := <optional str>$status,
    type:= <str>$type,
    value := <decimal>$value,
    details:= <optional json>$details,
    entity := assert_single((select Entity filter .id = <uuid>$entity))
}){
    id
}
