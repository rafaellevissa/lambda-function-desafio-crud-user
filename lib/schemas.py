register_user_schema = {
  "type" : "object",
  "properties" : {
    "name" : {"type" : "string"},
    "username" : {"type" : "string"},
    "password" : {"type" : "string"},
  },
  "required": ["username", "name", "password"]
}

login_schema = {
  "type" : "object",
  "properties" : {
    "username" : {"type" : "string"},
    "password" : {"type" : "string"},
  },
  "required": ["username", "password"]
}