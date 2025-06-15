with movement_:= assert_single((select Movement filter .id = <uuid>$movement)),
update movement_ set {
    notes:=<optional json>$notes ?? .notes,
}
