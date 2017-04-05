# coding=utf-8
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import XMLAdapterBase
from Products.MimetypesRegistry.interfaces import IMimetypesRegistryTool
import re

_FILENAME = 'mimetypes.xml'
_NAME = 'mimetypes'
_REG_ID = 'mimetypes_registry'
_REG_TITLE = 'MimeTypes Registry'
_BOOLEAN_OPTIONS = ('true', '1', 'on', 'yes')


def fix_unicode(attrs):
    ''' The values for the mimetype registry should be string non unicode
    '''
    for key in attrs:
        value = attrs.get(key, '')
        if isinstance(value, unicode):
            attrs[key] = value.encode('utf8')
        elif isinstance(value, tuple):
            attrs[key] = map(lambda val: val.encode('utf-8'),
                             map(safe_unicode, value))
    return attrs


class MimetypesRegistryNodeAdapter(XMLAdapterBase):
    """
    Node im- and export for mimetypes registry
    """

    __used_for__ = IMimetypesRegistryTool
    _LOGGER_ID = _NAME
    name = _NAME

    def _importNode(self, node):
        """
        Import the object from the DOM node.
        """
        self._initProvider(node)
        self._logger.info('Mimetype imported: %s' % `node`)

    def _initProvider(self, node):
        for child in node.childNodes:
            if child.nodeName != 'mimetype':
                continue
            if not self._check_attributes(child, ('mimetypes',)):
                continue

            id = self._get_as_tuple(child, 'mimetypes')[0]
            # check if it already exists
            existing_types = self.context.lookup(id)
            delete = self._get_as_boolean(child, 'delete')
            if delete:
                # delete, if existing
                if len(id)>0:
                    self.context.manage_delObjects((id,))
            elif len(existing_types)>0:
                # existing.. we always take the first one to update
                mt = existing_types[0]
                attrs = {
                    'name' : id,
                    'new_name' : child.getAttribute('name').strip() or mt.name(),
                    'mimetypes' : self._get_as_tuple(child, 'mimetypes', mt.mimetypes),
                    'extensions' : self._get_as_tuple(child, 'extensions', mt.extensions),
                    'icon_path' : child.getAttribute('icon_path') or mt.icon_path,
                    'binary' : self._get_as_boolean(child, 'binary', mt.binary),
                    'globs' : self._get_as_tuple(child, 'globs', mt.globs),
                    }
                self.context.manage_editMimeType(**fix_unicode(attrs))
            else:
                # create a new one
                if not self._check_attributes(child, ('name', 'mimetypes', 'extensions',
                                                      'icon_path')):
                    continue
                attrs = {
                    'id' : child.getAttribute('name').strip(),
                    'mimetypes' : self._get_as_tuple(child, 'mimetypes'),
                    'extensions' : self._get_as_tuple(child, 'extensions'),
                    'icon_path' : child.getAttribute('icon_path'),
                    'binary' : self._get_as_boolean(child, 'binary'),
                    'globs' : self._get_as_tuple(child, 'globs') or None,
                    }
                self.context.manage_addMimeType(**fix_unicode(attrs))

    def _check_attributes(self, node, attrs):
        for attr in attrs:
            if not node.getAttribute(attr).strip():
                self._logger.warning('Require attributes: "%s" for %s' %(
                        ', '.join(attrs),
                        node.toxml(),
                        ))
                return False
        return True

    def _get_as_tuple(self, node, attr, default=()):
        strval = node.getAttribute(attr).strip()
        if len(strval)==0:
            return default
        xpr = re.compile('[ \n]*')
        values = xpr.split(strval)
        values = [vv.strip() for vv in values]
        values = [isinstance(vv, unicode) and vv or vv.decode('utf8')
                  for vv in values]
        return tuple(values)

    def _get_as_boolean(self, node, attr, default=None):
        strval = node.getAttribute(attr)
        if len(strval)>0:
            return strval.strip().lower() in _BOOLEAN_OPTIONS
        else:
            return default

    def _exportNode(self):
        """ Export the mimetypes registry as dom node
        """
        fragment = self._doc.createElement('object')
        fragment.setAttribute('name', 'mimetypes_registry')
        fragment.setAttribute('meta_type', 'MimeTypes Registry')
        self._logger.info('Mimetypes registry exported.')
        for type_ in self.context.mimetypes():
            node = self._doc.createElement('mimetype')
            node.setAttribute('name', safe_unicode(type_.name()))
            node.setAttribute('mimetypes', u' '.join(map(safe_unicode, type_.mimetypes)))  # noqa
            node.setAttribute('extensions', u' '.join(map(safe_unicode, type_.extensions)))  # noqa
            node.setAttribute('globs', u' '.join(map(safe_unicode, type_.globs)))  # noqa
            node.setAttribute('icon_path', safe_unicode(type_.icon_path))
            node.setAttribute('binary', type_.binary and 'True' or 'False')
            fragment.appendChild(node)
        return fragment


def importMimetypes(context):
    """Import mimetypes registry.
    """
    site = context.getSite()
    tool = getToolByName(site, 'mimetypes_registry')

    importObjects(tool, '', context)


def exportMimetypes(context):
    """Export mimetypes registry
    """
    site = context.getSite()
    tool = getToolByName(site, 'mimetypes_registry', None)
    if tool is None:
        logger = context.getLogger('mimetypes')
        logger.info('Nothing to export.')
        return
    exportObjects(tool, '', context)
