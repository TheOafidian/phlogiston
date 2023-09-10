from phlogiston.datatypes import Sphere, Coordinates


def test_sphere_created():

    Sphere("Realmspace", "Known as the sea of Night", Coordinates(0.1, 0.2, 0.3))
    assert Sphere.list[0].name == "Realmspace"
    assert Sphere.list[0].description == "Known as the sea of Night"
    assert Sphere.list[0].coords.x == 0.1
    assert Sphere.list[0].coords.y == 0.2
    assert Sphere.list[0].coords.z == 0.3

    Sphere("Dreamspace", "Known as the dream of Night", Coordinates(-1, 0.2, 4))
    assert Sphere.list[1].name == "Dreamspace"
    assert Sphere.list[1].description == "Known as the dream of Night"
    assert Sphere.list[1].coords.x == 0
    assert Sphere.list[1].coords.y == 0.24
    assert Sphere.list[1].coords.z == 1
