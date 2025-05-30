update Record filter .id = <uuid>$id set {
    name:= <optional str>$name ?? .name,
    id_service := <optional str>$id_service ?? .id_service,
    status := <optional str>$status ?? .status,
    type:= <optional str>$type ?? .type,
    active:= <optional bool>$active ?? .active,
    value := <optional decimal>$value ?? .value,
    details:= <optional json>$details ?? .details,
}
