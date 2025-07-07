from teresa.dump.lt1_dump_data import lt1_dump_data
from teresa.dump.lt1_dump_header2doris import lt1_dump_header2doris

dump_header2doris_funcs = {
    'LT1': lt1_dump_header2doris,
    'BC3': 'bc3_dump_header',
    'GF3': 'dump_header_gf3',
    'FC1': 'dump_header_fc1'
}

dump_data_funcs = {
    'LT1': lt1_dump_data,
    'BC3': 'bc3_dump_data',
    'GF3': 'dump_data_gf3'
}
