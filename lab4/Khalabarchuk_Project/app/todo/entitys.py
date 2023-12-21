from app import db


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    completed = db.Column(db.Boolean)
    status = db.Column(db.String(20))

    def complete(self):
        self.completed = True
        self.status = ToDo.Status.COMPLETED

    class Status:
        COMPLETED = "COMPLETED"
        IN_PROGRESS = "IN_PROGRESS"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed,
            'status': self.status
        }
