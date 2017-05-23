
main:
  clear filters
  filterop and
  table orders

  clear filter
  filter field,give_asset
  filter op,==
  filter value,PEPEBALT
  push filter

  clear filter
  filter field,give_quantity
  filter op,>=
  filter value,5
  push filter

  get_table list.0

  load_len list.0,int.0

loop: rlcmp int.0,0
  jz endloop
  rlsum int.0,-1
  movr int.0
  loadob 0,list.0
  call process_order
  jmp loop

process_order: obcmp 0,get_asset,XCP
  jnz process_order_skip
  ;do something, like creating a buy order if below some point
  print XCPforPEPEBALT
process_order_skip:  return
process_order_assert: throw no_valid_type

endloop: finish
