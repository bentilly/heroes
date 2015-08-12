# Import here all models, you want to be accessible in Admin CRUD
from heroes.countries.models import Country
from heroes.sports.models import Sport
from heroes.divisions.models import Division
from heroes.roles.models import Role
from heroes.teams.models import Team

# Register here your models as strings
MODELS = (
    'Country',
    'Sport',
    'Division',
    'Role',
    'Team',
)
