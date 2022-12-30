# One Gotta Go UI

This is the user interface written in Flask and Bootstrap.

## Installation

### Via Docker

**Prerequisitie** - Need to already have docker installed on your system.

1. clone the `onegottago` repo
2. `cd {installdir}/onegottago_ui`
   
```bash
docker build -t onegottago_ui .

docker run -d -p 8080:8080 onegottago_ui
```

Verify that it worked:
http://127.0.0.1:8080/

## Deployment