function gif_components(mouthmouth_bytes){
  //header
  header = mouthmouth_bytes.slice(0,6)
  mouthmouth_bytes = mouthmouth_bytes.slice(6,mouthmouth_bytes.length)

  //logical_screen_descriptor
  logical_screen_descriptor = mouthmouth_bytes.slice(0,7)
  logical_screen_descriptor = {
    full_string: logical_screen_descriptor,
    width: logical_screen_descriptor.slice(0,2),
    height: logical_screen_descriptor.slice(2,4),
    packed_byte: logical_screen_descriptor.slice(4,5),
    background_color_index: logical_screen_descriptor.slice(5,6),
    pixel_aspect_ratio: logical_screen_descriptor.slice(6,7)
  }
  packed_byte = logical_screen_descriptor.packed_byte.toString()
  packed_byte_binary = hex2bin(packed_byte);
  packed_field = {
    full_string: packed_byte,
    global_color_table_flag: packed_byte_binary.slice(0,1),
    color_resolution: packed_byte_binary.slice(1,4),
    sort_flag:packed_byte_binary.slice(1,4),
    size_of_global_color_table: bin_to_dec(packed_byte_binary.slice(5,8))
  }
  logical_screen_descriptor.packed_field = packed_field;
  mouthmouth_bytes = mouthmouth_bytes.slice(7, mouthmouth_bytes.length)

  gct_f = 0;
  if (logical_screen_descriptor.packed_field.global_color_table_flag == 1){
    //global color table
    gct_f = 1;
    global_color_table_length = Math.round(3*(2 ** (logical_screen_descriptor.packed_field.size_of_global_color_table + 1)))
    global_color_table = mouthmouth_bytes.slice(0, global_color_table_length)
    colors = []
    mouthmouth_bytes = mouthmouth_bytes.slice(global_color_table_length,mouthmouth_bytes.length)
    and_the_rest = mouthmouth_bytes.slice(global_color_table_length,mouthmouth_bytes.length)
  }

  total_package = {
    header:header,
    logical_screen_descriptor:logical_screen_descriptor,
    global_color_table:global_color_table,
    and_the_rest: and_the_rest
  }

  return total_package
}
