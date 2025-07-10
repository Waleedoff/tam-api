from datetime import datetime


def fill_placeholders(data_to_be_filled: dict, html_body: str):
    from_to = [("{{" + from_ + "}}", to) for from_, to in data_to_be_filled.items()]

    # commons values
    from_to.append(("{{now_date}}", datetime.now().strftime("%d/%m/%Y %I:%M:%S %p").replace("PM", "مساء")))

    for from_, to in from_to:
        html_body = html_body.replace(from_, str(to))

    return html_body
