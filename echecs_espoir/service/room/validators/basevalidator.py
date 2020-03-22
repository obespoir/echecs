# coding=utf-8

from wtforms import form


class InputWrapper(object):

    def __init__(self, multi_dict):
        self._wrapped = multi_dict

    def __iter__(self):
        return iter(self._wrapped)

    def __len__(self):
        return len(self._wrapped)

    def __contains__(self, item):
        return item in self._wrapped

    def __getitem__(self, item):
        return self._wrapped(item)

    def __getattr__(self, item):
        return self.__getitem__(item)

    def getlist(self, name):
        try:
            return [self.to_unicode(str(self._wrapped[name]))]
        except KeyError:
            return []

    @classmethod
    def to_unicode(cls, value):
        if isinstance(value, (str, type(None))):
            return value
        if not isinstance(value, bytes):
            raise TypeError("Expected bytes, unicode or None; got %r" % type(value))
        return value.encode("utf-8")


class ValidatorError(Exception):
    def __init__(self, error_code):
        super(ValidatorError, self).__init__(error_code)
        self.error_code = error_code


class BaseValidator(form.Form):
    """
    参数校验器
    """
    def __init__(self, handler, obj=None, **kwargs):
        self.handler = handler
        super(BaseValidator, self).__init__(handler.params, obj, **kwargs)

    def process(self, form_data=None, obj=None, data=None, **kwargs):
        if form_data is not None and not hasattr(form_data, "getlist"):
            form_data = InputWrapper(form_data)
        super(BaseValidator, self).process(form_data, obj, **kwargs)
        if not self.validate():
            error_code = self.errors.values()[0][0]
            raise ValidatorError(error_code)




