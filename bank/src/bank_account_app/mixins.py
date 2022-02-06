class ValidateCleanModelMixin(object):
    '''Mixin to call `clean` method before every save and update actions.'''

    def save(self, *args, **kwargs):
        self.clean()
        super(ValidateCleanModelMixin, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.clean()
        super(ValidateCleanModelMixin, self).update(*args, **kwargs)
