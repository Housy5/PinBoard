import random

class Pin:
    
    _used_ids: list[str] = []
    
    def _random_char(self) -> str:
        return hex(random.randint(0, 0xf))[2:]
    
    def _generate_id(self) -> str:
        chars = []
        length: int = 4
        while length > 0:
            length -= 1
            chars.append(self._random_char())
        return ''.join(chars)
    
    def _to_sentence_case(self, data: str) -> str:
        if len(data) == 1:
            return data.upper()
        return data[0].upper() + data[1:]
    
    def _init_id(self):
        while (id := self._generate_id()) in self._used_ids:
            pass
        self._id = id
        self._used_ids.append(id)
        
    def __init__(self, message: str):
        self._init_id()
        self._msg = self._to_sentence_case(message)
    
    def assign(self):
        if self._id not in self._used_ids:
            self._used_ids.append(self._id)
    
    def get_message(self) -> str:
        return self._msg
    
    def get_id(self) -> str:
        return self._id
    
    def __str__(self) -> str:
        return f"Message: {self.get_message()}, ID: {self.get_id()}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Pin):
            return False
        return self.get_id() == other.get_id() and self.get_message() == other.get_message()

    def __delete__(self):
        index = self._used_ids.index(self.get_id())
        del(self._used_ids[index])

class NoSuchIDException(Exception):
    pass

class PinBoard():
    
    def __init__(self):
        self.board: list[Pin] = []
    
    def add_pin(self, pin: Pin) -> bool:
        if pin in self.board:
            return False
        self.board.append(pin)
        return True

    def find_index_for(self, pin: Pin) -> int:
        result = -1
        for cursor in range(len(self.board)):
            x = self.board[cursor]
            if x == pin:
                result = cursor
                break
        return result

    def find_pin_by_id(self, id: str) -> Pin:
        for x in self.board:
            if x.get_id() == id:
                return x
        raise NoSuchIDException("There is no pin with the specified ID!")

    def remove_pin(self, pin: Pin) -> bool:
        index: int = self.find_index_for(pin)
        if index == -1:
            return False
        del(self.board[index])
        return True

    def scan_pins(self):
        for x in self.board:
            x.assign()
