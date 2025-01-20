# By importing the following models in an __init__.py file,
# you can import them directly insted of the specific submodule.
from models.checkin_questions import CQModel
from models.custom_checkin_questions import CCQModel
from models.users import UserModel, FriendshipModel

# Example import: from models import UserModel
# Instead of: from models.users import UserModel
