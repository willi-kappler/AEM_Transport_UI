

# Python imports
import logging
import enum

logger = logging.getLogger(__name__)


class ATModelType(enum.Enum):
    AEM_Flow = 0
    AEM_Transport_horizontal = 1
    AEM_Transport_vertical = 2


class ATModelSettings:
    def __init__(self):
        self.aem_model_type: ATModelType = ATModelType.AEM_Flow

        self.domain_x_min: float = 0.0
        self.domain_y_min: float = 0.0
        self.domain_x_max: float = 100.0
        self.domain_y_max: float = 100.0

        self.aem_kf: float = 0.0
        self.aem_reference_head: float = 0.0
        self.aem_alpha_l: float = 0.0
        self.aem_alpha_t: float = 0.0

        self.aem_ca: float = 0.0
        self.aem_gamma: float = 0.0



    def set_aem_flow(self):
        self.aem_model_type = ATModelType.AEM_Flow

    def set_aem_transp_hor(self):
        self.aem_model_type = ATModelType.AEM_Transport_horizontal

    def set_aem_transp_ver(self):
        self.aem_model_type = ATModelType.AEM_Transport_vertical

    def is_aem_flow(self) -> bool:
        return self.aem_model_type == ATModelType.AEM_Flow

    def set_domain_extent(self, x_min: float, y_min: float, x_max: float, y_max: float):
        print(f"New domain: {x_min=}, {y_min=}, {x_max=}, {y_max=}")
        self.domain_x_min = x_min
        self.domain_y_min = y_min
        self.domain_x_max = x_max
        self.domain_y_max = y_max

    def get_domain_extend(self) -> tuple[float, float, float, float]:
        return (self.domain_x_min, self.domain_y_min, self.domain_x_max, self.domain_y_max)



