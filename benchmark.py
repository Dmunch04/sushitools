import timeit
from numpy import average

import json
from sushitools.json import JSONValue, to_json, other_to_json, JSONType


def test_std_json(data):
    encoded = json.dumps(data)


def test_sushi_json(value):
    #encoded = to_json(value)
    encoded = other_to_json(value)


def jsonvalue_to_raw(value: JSONValue, JSONType=JSONType):
    tt = value.get_type_tage()
    val = value.get_value()
    if tt == JSONType.OBJECT:
        obj = {}
        for key in val:
            obj[key] = jsonvalue_to_raw(val[key])
        return obj
    elif tt == JSONType.ARRAY:
        return [jsonvalue_to_raw(new) for new in val]
    else:
        return val


def test_json_value(value):
    raw = jsonvalue_to_raw(value)


if __name__ == '__main__':
    with open("./data.json", "r") as jdata:
        json_data = json.loads(jdata.read())
        json_value = JSONValue(json_data)

    run_std_test = "test_std_json(json_data)"
    run_sushi_test = "test_sushi_json(json_value)"
    run_json_value_test = "test_json_value(json_value)"

    #std_time = average(timeit.repeat(run_std_test, number=1000, repeat=10, globals=globals()))
    #sushi_time = average(timeit.repeat(run_sushi_test, number=1000, repeat=10, globals=globals()))
    json_value_time = average(timeit.repeat(run_json_value_test, number=1000, repeat=10, globals=globals()))

    #print(f'Average time for std:   {std_time} seconds')
    #print(f'Average time for sushi: {sushi_time} seconds')
    print(f'Average time for JSONValue conversion: {json_value_time} seconds')

    """
    Current benchmark results:
        Average time for std:   1.842028524899979 seconds
        Average time for sushi: 65.93311642699982 seconds
        
    very bad
    """
