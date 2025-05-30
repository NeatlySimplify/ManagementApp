update Record filter .id = <uuid>$record set {
    movement += (select Movement filter .id = <uuid>$movement_id)
}
# This approach using type casting works too:
#update Record filter .id = <uuid>$record set {
#    movement += <Movement><uuid>$movement_id
#}
