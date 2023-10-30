def validate_query_values(func, *args, **kwargs):
    def wrapper(values, *args, **kwargs):
        if "description" in values:
            values["description"] = f"""
                "{values["description"]}"
            """
        result = func(values=values, **kwargs)
        return result
    return wrapper
