from flask import Request


def validate_configuration_request(request: Request) -> tuple[str, str, list[str]]:
    data = _validate_data(request)

    system_prompt = data.get("system_prompt")
    model_name = data.get("model_name")

    errors: list[str] = []
    if not isinstance(system_prompt, str) or not system_prompt.strip():
        errors.append("No system prompt provided")

    if not isinstance(model_name, str) or not model_name.strip():
        errors.append("No model name provided")

    if len(errors) > 0:
        print(errors)
        raise ValueError("Invalid request: " + ", ".join(errors))

    return str(system_prompt), str(model_name), errors


def validate_cag_chat_request(request: Request) -> str:
    data = _validate_data(request)

    query = data.get("query")
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Invalid request: No query provided")

    return query


def _validate_data(request: Request):
    data = request.get_json() if request.is_json else request.form
    if not data:
        raise ValueError("Invalid request: No data provided")
    return data


# TODO: Move to rag_service
# def validate_rag_configuration(request_rag_configuration: dict | None) -> dict | None:
#     if not request_rag_configuration or not isinstance(request_rag_configuration, dict):
#         print("No rag_configuration provided or it is not a dictionary")
#         return None

#     embed_model_name = request_rag_configuration.get("embed_model_name")

#     if not embed_model_name or not isinstance(embed_model_name, str):
#         raise ValueError("embed_model_name must be a non-empty string")

#     request_temperature = request_rag_configuration.get("temperature")
#     request_top_p = request_rag_configuration.get("top_p")
#     request_top_k = request_rag_configuration.get("top_k")

#     temperature = float(request_temperature) if request_temperature is not None else 0.0
#     do_sample = True if abs(temperature) < 1e-8 else False
#     top_p = float(request_top_p) if request_top_p is not None else 0.9
#     top_k = int(request_top_k) if request_top_k is not None else 50

#     return {
#         "embed_model_name": embed_model_name,
#         "temperature": temperature,
#         "do_sample": do_sample,
#         "top_p": top_p,
#         "top_k": top_k
#     }