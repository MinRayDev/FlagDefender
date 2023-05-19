import enum


class Fonts(str, enum.Enum):
    """Class 'Fonts'.

        Extends 'str' and 'Enum'.

        :cvar chickenic: The chickenic font.
        :cvar product_sans: The product sans font.

    """
    chickenic = "./resources/fonts/Chickenic.ttf"
    product_sans = "./resources/fonts/ProductSans-Regular.ttf"
