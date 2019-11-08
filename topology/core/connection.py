import warnings
from topology.core.potential import Potential
from topology.core.site import Site
from topology.exceptions import TopologyError


class Connection(object):
    """ An abstract object that lists connected partners and their type
    This functions as a super-class for any connected groups (bonds,
    angles, dihedrals, etc), with a property for the conection_type

    Parameters
    ----------
    connection_members : list of topology.Site
        A list of constituents in this connection. Should be in order
    connection_type : topology.Potential
        An instance of topology.Potential that describes
        the potential function and parameters of this interaction
    name : string
        A unique name for the connection. Used for writing hoomdxml
        bonds/angles/dihedrals
        """
    def __init__(self, connection_members=None, connection_type=None, name="Connection"):
        if connection_members is None:
            connection_members = set()

        self._connection_members = _validate_connection_members(connection_members)
        self._connection_type = _validate_connection_type(connection_type)
        self._name = _validate_name(name)
        self._update_members()

    @property
    def connection_members(self):
        return self._connection_members

    @connection_members.setter
    def connection_members(self, connection_members):
        self._connection_members = _validate_connection_members(connection_members)

    @property
    def connection_type(self):
        return self._connection_type

    @connection_type.setter
    def connection_type(self, contype):
        self._connection_type = _validate_connection_type(contype)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, conname):
        self._name = _validate_name(conname)

    def _update_members(self):
        for partner in self.connection_members:
            if self not in partner.connections:
                partner.add_connection(self)

    def __repr__(self):
        descr = '<{}-partner Connection, id {}, '.format(
                len(self.connection_members), id(self))
        descr += 'type {}'.format(self.connection_type)
        if self.name:
            descr += ', name {}'.format(self.name)
        descr += '>'

        return descr


def _validate_connection_members(connection_members):
    for partner in connection_members:
        if not isinstance(partner, Site):
            raise TopologyError("Supplied non-Site {}".format(partner))

    if len(set(connection_members)) != len(connection_members):
        raise TopologyError("Error, cannot add connection between sites.")
    return connection_members


def _validate_connection_type(c_type):
    if c_type is None:
        warnings.warn("Non-parametrized Connection detected")
    elif not isinstance(c_type, Potential):
        raise TopologyError("Supplied non-Potential {}".format(c_type))
    return c_type


def _validate_name(conname):
    if not isinstance(conname, str):
        raise TopologyError("Supplied name {} is not a string".format(conname))
    return conname
