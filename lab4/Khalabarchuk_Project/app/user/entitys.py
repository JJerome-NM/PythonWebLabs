import datetime
import os.path
import secrets

from flask_login import UserMixin

from PIL import Image

from app import db, bcrypt, login_manager
from config import AVATARS_DIR_PATH, AVATAR_DEFAULT
