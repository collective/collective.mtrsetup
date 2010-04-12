collective.mtrsetup
===================

collective.mtrsetup provides a GenericSetup extension for importing and exporting mimetypes
to / from the mimetypes registry.


How to use
----------

* Add `collective.mtrsetup` as dependency to your `setup.py`
* Add a zcml-include to your `configure.zcml` or `dependency.zcml`
* Add a dependency to `profile-collective.mtrsetup:default` to your `metadata.xml` in your generic setup profile
* Create a `mimetypes.xml` as showed below in your generic setup profile



OpenOffice / Office 2007
------------------------

There is a additional generic setup profile provided in this 
package (`profile-collective.mtrsetup:default`) which adds icons for OpenOffice (with
backwards compatiblity to StarOffice) and adds the already used ms-office-icons to the
new office 2007 mimetypes.
The official Office 2007 icons are not added because of the license.



Examples
--------

Here are some examples of how to use it.

Setup some testing stuff:

>>> from collective.mtrsetup.tests.base import purge_registry, import_mimetypes_registry, \
...                                            export_mimetypes_registry
>>> registry = self.portal.mimetypes_registry
>>> purge_registry(registry)
>>> len(registry.mimetypes())
0


We can add new mimetypes with a simple mimetype tag in a *mimetypes.xml* in our generic setup
profile:

>>> filedata = """
... <?xml version="1.0"?>
... <object name="mimetypes_registry" meta_type="MimeTypes Registry">
...  <mimetype name="Any type" mimetypes="image/any"
...            extensions="any" globs="*.any" binary="True"
...            icon_path="any.png" />
... </object>
... """.strip()
>>> import_mimetypes_registry(registry, filedata)
[(20, 'mimetypes', 'Mimetype imported: <DOM Element: object at ...>')]

Now we should be able to export the current configuration:

>>> print export_mimetypes_registry(registry)
<?xml version="1.0"?>
<object name="mimetypes_registry" meta_type="MimeTypes Registry">
  <mimetype name="Any type" binary="True" extensions="any" globs="*.any"
      icon_path="any.png" mimetypes="image/any"/>
</object>


We can also just modify a existing one:

>>> filedata = """
... <object name="mimetypes_registry" meta_type="MimeTypes Registry">
...  <mimetype name="Any type" mimetypes="image/any image/another" />
... </object>
... """.strip()
>>> import_mimetypes_registry(registry, filedata)
[(20, 'mimetypes', 'Mimetype imported: <DOM Element: object at ...>')]

The above notiation just updates the mimetype record, where *image/any is the first
mimetype*:

>>> print export_mimetypes_registry(registry)
<?xml version="1.0"?>
<object name="mimetypes_registry" meta_type="MimeTypes Registry">
  <mimetype name="Any type" binary="True" extensions="any" globs="*.any"
      icon_path="any.png" mimetypes="image/any image/another"/>
</object>


Finally we can delete a mimetype by just adding the delete flag:

>>> filedata = """
... <object name="mimetypes_registry" meta_type="MimeTypes Registry">
...  <mimetype name="Any type" mimetypes="image/any" delete="True" />
... </object>
... """.strip()
>>> import_mimetypes_registry(registry, filedata)
[(20, 'mimetypes', 'Mimetype imported: <DOM Element: object at ...>')]
>>> print export_mimetypes_registry(registry)
<?xml version="1.0"?>
<object name="mimetypes_registry" meta_type="MimeTypes Registry"/>


You have to add at least one mimetype, otherwise the import will fail:

>>> filedata = """
... <object name="mimetypes_registry" meta_type="MimeTypes Registry">
...  <mimetype mimetypes="" />
... </object>
... """.strip()
>>> import_mimetypes_registry(registry, filedata)
[(30, 'mimetypes', u'Require attributes: "mimetypes" for <mimetype mimetypes=""/>'), (20, 'mimetypes', 'Mimetype imported: <DOM Element: object at ...>')]
