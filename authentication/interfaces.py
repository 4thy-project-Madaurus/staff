from typing import TypedDict
""" 

type LightUser struct {
	Email    string `json:"email"`
	Username string `json:"username"`
	Role     string `json:"role"`
	ID       string `json:"id"`
	Avatar   string `json:"avatar"`
	Group    string `json:"group"`
	Year     string `json:"year"`

}
"""
class UserClaim(TypedDict):
    # same from LightUser
    email: str
    username: str
    role: str
    id: str
    avatar: str
    group: str
    year: str
