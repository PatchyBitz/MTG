#!/bin/bash
#PAM_RHOST, PAM_RUSER, PAM_SERVICE, PAM_TTY, PAM_USER and PAM_TYPE

/usr/bin/curl "https://discord.com/api/webhooks/1204975377085374474/6brdbDPHm8aDT0OuyVAVqWqNJskvgCudKy9DMjrUaq1FAhKXgdffPXO8iZI6pqU77iH0" -H "Content-Type: application/json" -d "{\"content\": \"PAM_RHOST: $PAM_RHOST\\nPAM_RUSER: $PAM_RUSER\\nPAM_SERVICE: $PAM_SERVICE\\nPAM_TTY: $PAM_TTY\\nPAM_USER: $PAM_USER\\nPAM_TYPE: $PAM_TYPE\"}"
