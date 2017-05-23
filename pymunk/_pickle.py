class PickleMixin(object):
    """PickleMixin is used to provide base functionality for pickle/unpickle 
    and copy.
    """

    def __getstate__(self):
        """Return the state of this object
        
        This method allows the usage of the :mod:`copy` and :mod:`pickle`
        modules with this class.
        """
        
        attrs_init = []
        attrs_general = []
        for t in list(type(self).__bases__) + [type(self)]:
            if hasattr(t, '_pickle_attrs_init'):
                attrs_init += t._pickle_attrs_init
            if hasattr(t, '_pickle_attrs_general'):
                attrs_general += t._pickle_attrs_general
            
        d = {
            'init':[], # arguments for init
            'general':[], # general attributes 
            'custom':[], # custom attributes set by user
            'special':[] # attributes needing special handling
        }
        for a in attrs_init:
            d['init'].append((a, self.__getattribute__(a)))

        for a in attrs_general:
            d['general'].append((a, self.__getattribute__(a)))
        
        for k,v in self.__dict__.items():
            if k[0] != '_':
                d['custom'].append((k,v))
        
        return d

    def __setstate__(self, state):
        """Unpack this object from a saved state.

        This method allows the usage of the :mod:`copy` and :mod:`pickle`
        modules with this class.
        """
        
        init_attrs = []

        init_args = [v for k,v in state['init']]
        self.__init__(*init_args)

        for k,v in state['general']:
            self.__setattr__(k,v)

        for k,v in state['custom']:
            self.__setattr__(k,v)

        