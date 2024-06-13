class NotFoundException(Exception):
    def __init__(self, entity: str, id: str):
        super(NotFoundException, self).__init__(
            f'Not found entity {entity} with identifier {id}. Check Name and Password.')
