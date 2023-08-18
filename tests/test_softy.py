import unittest
import softy

class TestSofty(unittest.TestCase):

    def test_softy_dict(self):

        d = softy.softy()

        self.assertTrue(softy.isnull(d['234'].x.y[23].z))

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

        sbasket = softy.softy(basket)
        
        self.assertEqual('Red', sbasket.Blanket.Color)
        self.assertTrue(sbasket.Fruits[2].Color is softy.null)

