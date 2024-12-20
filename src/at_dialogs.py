

# Python imports
import logging

# External imports
from nicegui import binding, ui


logger = logging.getLogger(__name__)

class ATLogoutDialog(ui.dialog):
    def __init__(self):
        super().__init__()

        with self:
            with ui.card():
                ui.label("Logged out sucessfully!").classes("text-2xl")

class ATTransportDialog(ui.dialog):
    def __init__(self, model_settings, status_bar):
        super().__init__()

        self.model_settings = model_settings
        self.status_bar = status_bar

        with self:
            with ui.card():
                ui.label("Select AEM transport variant:")
                ui.select(["horizontal", "vertical"], on_change=self.set_variant)

    def set_variant(self, element):
        self.close()

        v = element.value
        match v:
            case "horizontal":
                self.model_settings.set_aem_transp_hor()
                self.status_bar.set_text("AEM model is now of type transport horizontal")
            case "vertical":
                self.model_settings.set_aem_transp_ver()
                self.status_bar.set_text("AEM model is now of type transport vertical")

class ATDomainExtendDialog(ui.dialog):
    def __init__(self, model_settings, status_bar):
        super().__init__()

        self.model_settings = model_settings
        self.status_bar = status_bar

        with self:
            with ui.card():
                ui.label("Set domain extend:")

                self.x_min = ui.number("x min", step=10.0)
                self.y_min = ui.number("y min", step=10.0)
                self.x_max = ui.number("x max", step=10.0)
                self.y_max = ui.number("y max", step=10.0)

                ui.button("OK", on_click=self.set_domain)

    def set_domain(self):
        self.close()

        x_min = self.x_min.value
        y_min = self.y_min.value
        x_max = self.x_max.value
        y_max = self.y_max.value

        self.status_bar.set_text(f"New domain extend: x_min: {x_min}, y_min: {y_min}, x_max: {x_max}, y_max: {y_max}")

        self.model_settings.domain_x_min = x_min
        self.model_settings.domain_y_min = y_min
        self.model_settings.domain_x_max = x_max
        self.model_settings.domain_y_max = y_max

        print(f"New domain: {x_min=}, {y_min=}, {x_max=}, {y_max=}")

    def open(self):
        (x_min, y_min, x_max, y_max) = self.model_settings.get_domain_extend()

        self.x_min.set_value(x_min)
        self.y_min.set_value(y_min)
        self.x_max.set_value(x_max)
        self.y_max.set_value(y_max)

        super().open()

class ATAquifierPropsDialog(ui.dialog):
    def __init__(self, model_settings, status_bar):
        super().__init__()

        self.model_settings = model_settings
        self.status_bar = status_bar

        with self:
            with ui.card():
                ui.label("Aquifer properties:")

                self.prop1 = ui.number("xxx", step=1.0)
                self.prop2 = ui.number("yyy", step=1.0)

                ui.button("OK", on_click=self.set_aquifier_props)

    def set_aquifier_props(self):
        self.close()

        if self.model_settings.is_aem_flow():
            self.model_settings.aem_kf = self.prop1.value
            self.model_settings.aem_reference_head = self.prop2.value
            self.status_bar.set_text(f"AEM flow aquifier properties: kf: {self.model_settings.aem_kf}, reference head: {self.model_settings.aem_reference_head}")
        else:
            self.model_settings.aem_alpha_l = self.prop1.value
            self.model_settings.aem_alpha_t = self.prop2.value
            self.status_bar.set_text(f"AEM transport aquifier properties: alpha_l: {self.model_settings.aem_alpha_l}, alpha_t: {self.model_settings.aem_alpha_t}")

    def open(self):
        if self.model_settings.is_aem_flow():
            self.prop1.props("label=kf")
            self.prop2.props("label='reference head'")

            self.prop1.set_value(self.model_settings.aem_kf)
            self.prop2.set_value(self.model_settings.aem_reference_head)
        else:
            self.prop1.props("label=alpha_l")
            self.prop2.props("label=alpha_t")

            self.prop1.set_value(self.model_settings.aem_alpha_l)
            self.prop2.set_value(self.model_settings.aem_alpha_t)

        super().open()

class ATChemicalParametersDialog1(ui.dialog):
    def __init__(self):
        super().__init__()

        with self:
            with ui.card():
                ui.label("Chemical parameters are only valid for AEM transport models!")

class ATChemicalParametersDialog2(ui.dialog):
    def __init__(self, model_settings, status_bar):
        super().__init__()

        self.model_settings = model_settings
        self.status_bar = status_bar

        with self:
            with ui.card():
                ui.label("Chemical parameters:")

                self.ca = ui.number("ca", step=1.0)
                self.gamma = ui.number("gamma", step=1.0)

                ui.button("OK", on_click=self.set_chemical_params)

    def set_chemical_params(self):
        self.close()

        self.model_settings.aem_ca = self.ca.value
        self.model_settings.aem_gamma = self.gamma.value
        self.status_bar.set_text(f"AEM chemical parameters: ca: {self.model_settings.aem_ca}, gamma: {self.model_settings.aem_gamma}")

    def open(self):
        self.ca.set_value(self.model_settings.aem_ca)
        self.gamma.set_value(self.model_settings.aem_gamma)

        super().open()

class ATAboutDialog(ui.dialog):
    def __init__(self):
        super().__init__()

        with self:
            with ui.card():
                ui.label("Supervisor: Prabhas Yadav")
                ui.label("Simulation: Anton Köhler")
                ui.label("GUI: Willi Kappler")

