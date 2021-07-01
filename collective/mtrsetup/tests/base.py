"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
"""
from xml.dom.minidom import parseString
from six import StringIO

from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig
from plone.testing import z2

from collective.mtrsetup.handler import MimetypesRegistryNodeAdapter
from Products.GenericSetup.tests.common import DummyImportContext
from Products.GenericSetup.tests.common import DummyExportContext


class MtrsetupLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '  <include package="collective.mtrsetup.tests" file="test.zcml" />'
            "</configure>",
            context=configurationContext,
        )

        z2.installProduct(app, "collective.mtrsetup")

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, "collective.mtrsetup:default")

        roles = ("Member", "Contributor")
        portal.portal_membership.addMember("contributor", "secret", roles, [])


MTRSETUP_FIXTURE = MtrsetupLayer()
MTRSETUP_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MTRSETUP_FIXTURE,), name="collective.mtrsetup:Integration"
)


def purge_registry(registry):
    """Deletes all mimetypes from the given mimetypes registry."""
    a = False
    for type_ in registry.mimetypes():
        registry.unregister(type_)


def import_mimetypes_registry(registry, xml_filecontent):
    """Imports the given xml filecontent directly into the mimetypes registry"""
    portal = registry.portal_url.getPortalObject()
    tool = portal.portal_setup
    imp = DummyImportContext(portal, purge=True, tool=tool)
    doc = parseString(xml_filecontent)
    node = doc.firstChild
    adapter = MimetypesRegistryNodeAdapter(registry, imp)
    adapter._importNode(node)
    return imp.getLogger(adapter._LOGGER_ID)._messages


def export_mimetypes_registry(registry):
    """Exports the mimetypes registry as xml string"""
    portal = registry.portal_url.getPortalObject()
    tool = portal.portal_setup
    imp = DummyExportContext(portal, tool=tool)
    adapter = MimetypesRegistryNodeAdapter(registry, imp)
    adapter._doc.appendChild(adapter._exportNode())
    writer = StringIO()
    adapter._doc.writexml(writer, addindent="  ", newl="\n")
    writer.seek(0)
    return writer.read().strip()
