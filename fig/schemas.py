# JSON Schema Reference:
#   - https://json-schema.org/understanding-json-schema/reference/

question_full_properties = {
    "title": {
        "type": "object",
        "properties": {
            "on_rate": {"type": "string"},
            "on_display": {"type": "string"}
        },
        "additionalProperties": False
    },
    "include_in": {
        "type": "array",
        "items": {
            "type": "string",
            "enum": ["on_rate", "on_display"]
        },
        "uniqueItems": True,
        "minItems": 1,
        "maxItems": 2
    },
    "weight": {
        "type": "number"
    },
    "order": {
        "type": "number"
    },
    "status": {
        "type": "string"
    },
    "category": {
        "type": "string"
    }
}

add_question = {
    "type": "object",
    "properties": question_full_properties,
    "additionalProperties": False,
    "required": [
        "title",
        "include_in",
        "weight",
        "order",
        "status",
        "category"
    ]
}

update_question = {
    "type": "object",
    "properties": question_full_properties,
    "additionalProperties": False,
    "minProperties": 1
}
