from ajax.models import UploadedImage
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError

register = template.Library()

@register.simple_tag(takes_context=True)
def step_picture(context, form, token):
    value = form.get("step-picture-id_"+str(token), '')
    context['stepimageid']=value
    return value



@register.tag("picture_from_id")
def do_picture_from_id(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, picture_id = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

    return PictureUrlNode(picture_id)


class PictureUrlNode(template.Node):
    def __init__(self, picture_id):
        self.picture_id = template.Variable(picture_id)

    def render(self, context):
        try:
            picture_id = self.picture_id.resolve(context)
            if picture_id:
                image = UploadedImage.objects.get(id=picture_id).image
                if image and image.url:
                    return image.url
            else:
                return ''
        except template.VariableDoesNotExist:
            return ''
        except DatabaseError:
            return ''
        except ObjectDoesNotExist:
            return ''
