# Import here all models, you want to be accessible in Admin CRUD
from heroes.sports.models import Sport
from heroes.countries.models import Country

# Register here your models as strings
MODELS = (
    'Sport',
    'Country',
)
