def filtrar_passes(eventos):
    passes = eventos[eventos['type'] == "Pass"]
    return passes

def filtrar_chutes(eventos):
    chutes = eventos[eventos['type'] == "Shot"]
    return chutes

def preparar_chutes(chutes):    
    chutes = chutes.copy()    
    chutes['x'] = chutes['location'].apply(lambda location: location[0])
    chutes['y'] = chutes['location'].apply(lambda location: location[1])
    return chutes

def preparar_passes(passes):
    passes = passes.copy()
    passes['x'] = passes['location'].apply(
        lambda location: location[0]
    )
    passes['y'] = passes['location'].apply(
        lambda location: location[1]
    )
    passes['end_x'] = passes['pass_end_location'].apply(
        lambda location: location[0]
    )
    passes['end_y'] = passes['pass_end_location'].apply(
        lambda location: location[1]
    )    
    return passes