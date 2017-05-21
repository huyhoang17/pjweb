from django import template

register = template.Library()


@register.filter()
def convert_to_html(raw_string):
    output = []
    for line in raw_string.split("|"):
        output.append("<li>{}</li>".format(line.strip('-')))
    return "".join(output)


@register.filter()
def html_inline(raw_string):
    if raw_string is None:
        return "<small style='color: #000;'>Unknown</small>"
    output = raw_string.split("|")
    return "<small style='color: #000;'>{}</small>".format("".join(output))
