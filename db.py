'''connect to backend database with SQLAlchemy'''
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm


class dbc:
    '''a datatbase connection.'''

    def __init__(self, uri):
        self.engine = sqlalchemy.create_engine(uri, echo=True)
        self.base = sqlalchemy.ext.declarative.declarative_base()
        self.Session = sqlalchemy.orm.sessionmaker()
        self.Session.configure(bind=self.engine)
        self.session = self.Session()

    def Query(self, model):
        return self.session.query(model)

    def init_title(self, group, title):
        title_item = self.Query(Title).filter_by(group_id=group).first()
        if title_item:
            title_item.title = title
        else:
            title_item = Title(group_id=group, title=title)
        self.session.add(title_item)
        self.session.commit()

    def update_title(self, group, title):
        title_item = self.Query(Title).filter_by(group_id=group).first()
        title_item.title = title
        self.session.add(title_item)
        self.session.commit()

    def delete_title(self, group):
        title_item = self.Query(Title).filter_by(group_id=group).first()
        self.session.delete(title_item)
        self.session.commit()


class Title(sqlalchemy.ext.declarative.declarative_base()):
    '''memos model'''
    __tablename__ = 'titles'
    group_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(128), index=True)

    def jsonify(self):
        return {'group_id': self.group_id, 'title': self.title}


def init(uri, *models):
    test_dbc = dbc(uri)
    for model in models:
        model.metadata.create_all(test_dbc.engine)


def usage():
    print("use --init after create configuration file :-)")


if __name__ == "__main__":
    try:
        import config
        import sys
        if "init" in sys.argv[1]:
            init(config.database, Title)
    except (ImportError, IndexError):
        usage()
