import vlcapi
def get_media_info():
    status=vlcapi.status()
    if not "information" in status:
        return "Please load music","No music is loaded"
    metadata=status["information"]["category"]["meta"]
    
    return metadata["album"], metadata["filename"].split(".")[0]