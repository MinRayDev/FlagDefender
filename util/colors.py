import enum

from catppuccin import Flavour


class Colors(tuple[int, int, int], enum.Enum):
    white = (255, 255, 255)
    red = Flavour.frappe().red.rgb
    text_color = Flavour.frappe().pink.rgb
    text = Flavour.frappe().text.rgb
    surface1 = Flavour.frappe().surface1.rgb
    surface2 = Flavour.frappe().surface2.rgb
    hover_color = Flavour.frappe().overlay0.rgb
    button_base_color = Flavour.frappe().surface0.rgb
    base_color = Flavour.frappe().base.rgb
    mantle = Flavour.frappe().mantle.rgb
    crust = Flavour.frappe().crust.rgb
    subtext0 = Flavour.frappe().subtext0.rgb
