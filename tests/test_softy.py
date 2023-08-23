import unittest
import softy

class TestSofty(unittest.TestCase):

    def test_softy_dict(self):

        d = softy.soften(dict())

        self.assertTrue(softy.isnull(d.s234.x.y.i(23).z))

    def test_softy_basket(self):
        basket = {
            "Fruits": [
                {
                    "Type": "Apple",
                    "Color": "Green"
                },
                {
                    "Type": "Apple",
                    "Color": "Red"
                }
            ],
            "Blanket": {
                "Material": "Cotton",
                "Color": "Red"
            }
        }

        sbasket = softy.soften(basket)

        self.assertEqual('Red', sbasket.Blanket.Color)
        self.assertTrue(sbasket.Fruits.i(2).Color is softy.null)

        self.assertRaises(KeyError, lambda : basket['NotExists'])
        self.assertRaises(IndexError, lambda : basket['Fruits'][2])

