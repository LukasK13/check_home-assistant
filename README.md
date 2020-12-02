Plugin for checking a local Home-Assistant instance via the API using Icinga2 / nagios.

# Requirements
* Python package asyncws
* Home-assistant [system health component](https://www.home-assistant.io/integrations/system_health/)

# Usage

* **-u / --url** URL to the Home-Assistant API
* **-t / --token** Long live access token for Home-Assistant.
* **-s / --ssl** Use SSL for the connection to the Mailcow API
* **-i / --insecure** Don't verify the SSL certificate

# Icinga2 config
## Comand template
```
object CheckCommand "home-assistant" {
    import "plugin-check-command"
    command = [ PluginDir + "/check_home-assistant.py" ]
    arguments += {
        "-t" = {
            description = "Long live access token for Home-Assistant."
            required = true
            value = "$home-assistant_token$"
        }
        "-u" = {
            description = "URL to the Home-Assistant API."
            value = "$home-assistant_url$"
        }
        "-i" = {
            description = "Insecure connection. Don't verify the SSL certificate."
            set_if = "$mailcow_insecure$"
        }
        "-s" = {
            description = "Use SSL for the connection."
            set_if = "$mailcow_ssl$"
        }
    }
}
```

## Service template
```
template Service "check-home-assistant" {
    check_command = "home-assistant"
    command_endpoint = host_name
}
