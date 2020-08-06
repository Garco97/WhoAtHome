# WhoAtHome 
Python script that lets see who is at home. There is a configuration and a users json. Now it works with email. Static IPs needed.

## configuration.json
```json
{
    "email": "your email",
    "password":"your encrypted password",
    "leave": "message when someone leaves the house",
    "arrive": "message when someone enters the house",
    "subject": "Subject of the email",
    "first_ip": 200, 
    "last_ip": 205,
    "network": "192.168.1.0/24",
    "refresh": 10
}
```

## users.json
```json
[
    {
        "name": "name of the user",
        "email": "email of the user",
        "ip": "200",
        "active": 1
    },
]
```