# Import here all models, you want to be accessible in Admin CRUD
from heroes.sports.models import Sport
from heroes.countries.models import Country
from heroes.teams.models import Team
from heroes.events.models import Event
from heroes.representatives.models import Representative
from heroes.representatives.models import Squad, ReprSquadState

# Register here your models as strings
MODELS = (
    'Sport',
    'Country',
    'Team',
    'Event',
    'Representative',
    'ReprSquadState',
    'Squad',
)
