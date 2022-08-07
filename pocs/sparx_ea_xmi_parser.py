import typing
import xmltodict
import pydantic
import pydantic.utils

file = 'input.xml'

IDS = {}


class XMIBase(pydantic.BaseModel):
    xmi_type: str = pydantic.Field(alias='@xmi:type', repr=False)
    xmi_id: str = pydantic.Field(alias='@xmi:id', repr=False)

    def __init__(self, **data: typing.Any) -> None:
        super().__init__(**data)

        assert self.xmi_id not in IDS
        IDS[self.xmi_id] = self


class Type(pydantic.BaseModel):
    id_ref: str = pydantic.Field(alias='@xmi:idref')

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        try:
            ref = IDS[self.id_ref]
        except KeyError:
            ref = self.id_ref

        return f'Type(ref={repr(ref)})'


class MemberEnd(pydantic.BaseModel):
    id_ref: str = pydantic.Field(alias='@xmi:idref')


class LowerValue(XMIBase):
    value: str = pydantic.Field(alias='@value')


class OwnedAttribute(XMIBase):
    name: typing.Optional[str] = pydantic.Field(alias='@name')

    # Recursive child elements
    lower_value: typing.Optional[LowerValue] = pydantic.Field(alias='lowerValue')
    type: Type


class PackagedElement(XMIBase):
    name: typing.Optional[str] = pydantic.Field(alias='@name')
    visibility: typing.Optional[str] = pydantic.Field(alias='@visibility', repr=False)

    # Recursive child elements
    elements: typing.List['PackagedElement'] = pydantic.Field(default_factory=list, alias='packagedElement')
    attributes: typing.List[OwnedAttribute] = pydantic.Field(default_factory=list, alias='ownedAttribute')
    ends: typing.List[MemberEnd] = pydantic.Field(default_factory=list, alias='memberEnd')

    @pydantic.validator('elements', 'attributes', 'ends', pre=True)
    def make_single_elem_list(cls, val):
        """
        xmltodict knows nothing about the XML schema.
        It just parses the XML as is.
        This means that xmltodict parses non repeating elements as dicts:
            <parent>                    {
                <child></child>   ==>     'child': {}
            </parent>                   }

        On the other hand xmltodict parses repeating elements as lists:
            <parent> 
                <child></child>         {
                <child></child>   ==>     'child': [{}, {}, {}]
                <child></child>         }
            </parent>

        In order to make pydantic parse the object correctly, this method transforms
        all scalar elements - that are actual sequences - to lists.
        """
        if hasattr(val, 'keys'):
            return [val, ]

        return val


def print_elem(p: PackagedElement, ident=0):
    print(
        '  ' * ident + '>', p.name,
        f'({p.attributes})'
    )
    ident += 1
    for c in p.elements:
        print_elem(c, ident)
    ident -= 1


def print_connections(p: PackagedElement):

    if len(p.ends) == 2:
        x, y = p.ends


        try:
            e1 = IDS[x.id_ref].name
        except KeyError:
            e1 = 'NaN'

        try:
            e2 = IDS[y.id_ref].name
        except KeyError:
            e2 = 'NaN'

        print(f'{e1} <-- {p.name} --> {e2}')

    for c in p.elements:
        print_connections(c)


# Driver Code
with open(file, 'rb') as fd:
    result = xmltodict.parse(fd)
    xmi = result['xmi:XMI']
    model = xmi['uml:Model']
    packaged_element = PackagedElement.parse_obj(model['packagedElement'])

    print_elem(packaged_element)
    print_connections(packaged_element)

    print(len(IDS.keys()))
