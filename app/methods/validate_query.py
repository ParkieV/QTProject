def validate_query_values(func, *args, **kwargs):
    def wrapper(values: dict, *args, **kwargs):
        for key in values:
            if isinstance(values[key], str):
                values[key] = f"\"{values[key]}\""
        result = func(values=values, *args, **kwargs)
        return result
    return wrapper
