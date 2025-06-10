select (insert Details {
    title:=<str>$title,
    field:=<str>$field,
    origin:= assert_single((select Link filter .id = <uuid>$id))
}){title, field, origin:{id}}
