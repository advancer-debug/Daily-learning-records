def to_dict(self): 
return {k:v for k,v in self.__dict__items() if
k!="_sa_instance_state"}

update更新时的目标必须整合为字典类型dict
