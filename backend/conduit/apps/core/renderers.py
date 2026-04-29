from rest_framework.renderers import JSONRenderer


class ConduitJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'
    pagination_object_label = 'objects'
    pagination_object_count = 'count'

    def render(self, data, media_type=None, renderer_context=None):

        if data is None:
            data = {}

        if isinstance(data, dict) and data.get('results') is not None:
            data = {
                self.pagination_object_label: data['results'],
                self.pagination_object_count: data['count']
            }
            return super().render(data, media_type, renderer_context)

        if isinstance(data, dict) and data.get('errors') is not None:
            return super().render(data, media_type, renderer_context)

        return super().render({self.object_label: data}, media_type, renderer_context)