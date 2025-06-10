select (insert PhoneNumber {
    title:=<str>$title,
    field:=<str>$field,
    origin:= assert_single((select Link filter .id = <uuid>$id))
}){id}
