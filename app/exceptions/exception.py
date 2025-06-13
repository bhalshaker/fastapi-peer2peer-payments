class UserNotFoundException(Exception):
    """Exception raised when a user is not found."""
    def __init__(self, user_id:str):
        self.user_id = user_id
        super().__init__(self.user_id)