from pydantic import BaseModel


class System(BaseModel):

    class Config:
        arbitrary_types_allowed = True

    modifier: str
    system: str
    company: str
    company: str

    def __init__(self, **kwargs) -> None:
        self.folder = {
            'preffix': None,
            'suffix': None
        }
        super().__init__(**kwargs)

    def get_modifier(self):
        def detect_modifier(name):
            if name.startswith("Unofficial - "):
                return "Unofficial"
            if name.startswith("Source Code - "):
                return "Source Code"
            if name.startswith("Non-Redump - "):
                return "Non-Redump"
            if name.startswith("Arcade - "):
                return "Arcade"
            return "Consoles"

        if self.modifier:
            return self.modifier
        self.modifier = detect_modifier(self.name)
        return self.modifier
