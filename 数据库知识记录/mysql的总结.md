def to_dict(self): 
return {k:v for k,v in self.__dict__items() if
k!="_sa_instance_state"}