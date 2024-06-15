class AlreadyExistsException(BaseException):
    def __init__(self, entity: str, id: str):
        super(AlreadyExistsException, self).__init__(
            f'Entity {entity} already exists with identifier {id}')
