import re

# TODO: 注意这里的正则匹配的表达式，只有 lt1 的是正确的，别的在 debug 的时候，注意一点

radar_type_pat_map = {
    'LT1': r'^LT1.*\.meta\.xml$',
    'BC3': 'bc3*slc*.xml',
    'GF3': 'GF3*.meta.xml',
    'FC1': 'spacety_SLC_SM_*.h5'
}

# 这个 map 是用来放不同类型的雷达数据 匹配 meta/xml 的正则项的
is_meta_file = {
    'LT1': lambda x: bool(re.search(r'^LT1.*\.meta\.xml$', x)),
    'BC3': lambda x: bool(re.search(r'bc3*slc*.xml', x)),
    'GF3': lambda x: bool(re.search(r'GF3*.meta.xml', x)),
    'FC1': lambda x: bool(re.search(r'spacety_SLC_SM_*.h5', x)),
}

# 这个 map 是用来放不同类型的雷达数据 匹配 data 的正则项的
is_data_file = { 
    'LT1': lambda x: bool(re.search(r'^LT1.*\.tiff$', x)),
    'BC3': lambda x: bool(re.search(r'bc3*slc*.h5', x)),
    'GF3': lambda x: bool(re.search(r'GF3*_(H|V)(H|V)_*.tiff', x)),
    'FC1': lambda x: bool(re.search(r'spacety_SLC_SM_*.h5', x)),
}

get_date_from_filename = { 
    'LT1': {'meta': lambda x: re.search(r'LT1.*_(20\d{6})', x).group(1),
            'data': lambda x: re.search(r'LT1.*_(20\d{6})', x).group(1)},
    'BC3': {'meta': lambda x: re.search(r'bc3.*_(\d{8})', x).group(1),
            'data': lambda x: re.search(r'bc3.*_(\d{8})', x).group(1)},     
    'GF3': {'meta': lambda x: re.search(r'GF3.*_(\d{8})', x).group(1),
            'data': lambda x: re.search(r'GF3.*_(\d{8})', x).group(1)},
    'FC1': {'meta': lambda x: re.search(r'spacety_SLC_SM_(\d{8})', x).group(1),
            'data': lambda x: re.search(r'spacety_SLC_SM_(\d{8})', x).group(1)}
}
