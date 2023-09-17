from phlogiston.datatypes import Sphere, Coordinates


def test_sphere_created():

    n = len(Sphere.list)
    Sphere("Realmspace", "Known as the sea of Night", Coordinates(0.1, 0.2, 0.3))
    assert Sphere.list[n].name == "Realmspace"
    assert Sphere.list[n].description == "Known as the sea of Night"
    assert Sphere.list[n].coords.x == 0.1
    assert Sphere.list[n].coords.y == 0.2
    assert Sphere.list[n].coords.z == 0.3

    Sphere("Dreamspace", "Known as the dream of Night", Coordinates(-1, 0.2, 4))
    assert Sphere.list[n+1].name == "Dreamspace"
    assert Sphere.list[n+1].description == "Known as the dream of Night"
    assert Sphere.list[n+1].coords.x == 0
    assert Sphere.list[n+1].coords.y == 0.24
    assert Sphere.list[n+1].coords.z == 1
