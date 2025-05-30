update Address filter .id = <uuid>$address set {
    state:= <optional str>$state ?? .state,
    city:= <optional str>$city ?? .city,
    district:= <optional str>$district ?? .district,
    street:= <optional str>$street ?? .street,
    number:= <optional int64>$number ?? .number,
    complement:= <optional str>$complement ?? .complement,
    postal:= <optional str>$postal ?? .postal
}
