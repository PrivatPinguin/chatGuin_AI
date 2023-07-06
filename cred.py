def getCred(credName):
    if credName == 'BOTAPIKEY':
        return 'discord_bot_API_key'
    elif credname == 'WEATHERAPIKEY':
        return '_open_weather_API_key'
    elif credname == 'NASAAPIKEY':
        return 'NASA_API_key'
    return ''