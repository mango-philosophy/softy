# Softy

[![license](https://img.shields.io/github/license/jackmuskopf/softy.svg)](https://github.com/jackmuskopf/softy/blob/main/LICENSE)

Soft access of nested data for more readable code
- Lightweight
- Pure Python
- One source file
- < 150 lines of code
- No dependencies


An item:
```python
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
```

Before:
```python
# get the blanket color
blanket = basket.get('Blanket')
blanket_color = None
if blanket:
    blanket_color = blanket.get('Color')
if blanket_color is not None:
    print(f'Blanket is {blanket_color}')
else:
    print('Unspecified blanket color')

# get the color of the third fruit
fruits = basket.get('Fruits')
fruit_color = None
if fruits is not None:
    if len(fruits) > 2:
        fruit_color = fruits[2].get('Color')
if fruit_color is not None:
    print(f'3rd fruit color is {fruit_color}')
else:
    print('Unspecified 3rd fruit color')
```


After:
```python
import softy
basket = softy.soften(basket)

# get the blanket color
if basket.Blanket.Color is not softy.null:
    print(f'Blanket is {basket.Blanket.Color}')
else:
    print('Unspecified blanket color')

# get the color of the third fruit
if basket.Fruits[2].Color is not softy.null:
    print(f'3rd fruit color is {fruit_color}')
else:
    print('Unspecified 3rd fruit color')


```