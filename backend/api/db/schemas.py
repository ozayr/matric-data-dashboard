from pydantic import BaseModel


class RequestRecord(BaseModel):
    emis : int
    centre_no : int
    name : str
    wrote_2014 : int
    passed_2014 : int
    wrote_2015 : int
    passed_2015 : int
    wrote_2016 : int
    passed_2016 : int
    province : str
    class Config:
        orm_mode = True

class ResponseRecord(BaseModel):
    emis : int
    centre_no : int
    name : str
    wrote_2014 : int
    passed_2014 : int
    wrote_2015 : int
    passed_2015 : int
    wrote_2016 : int
    passed_2016 : int
    province : str
    pass_rate_2014 : float
    pass_rate_2015 : float
    pass_rate_2016 : float
    class Config:
        orm_mode = True
