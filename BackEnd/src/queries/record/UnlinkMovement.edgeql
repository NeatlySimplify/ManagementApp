update Record filter .id = <uuid>$record set {
    movement -= (select Movement filter .id = <uuid>$movement_id)
}
