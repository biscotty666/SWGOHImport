from swimport.models import Guild, Player, Toon, Mod, Skill, Equipped, ModStat

def run():
  import json
  import os
  
  with open('./swimport/config.json') as f:
    config = json.load(f)
    
  from .api_swgoh_help import api_swgoh_help

  allycode = config['allycode']
  client = api_swgoh_help({'username': config['credname'], 'password': config['credpass']})

  def getGuild(api_client, allycode):
      """ :parameters api_swgoh_help instance and player allycode """
      payload = {'allycodes': [allycode], 'language': "eng_us", 'enums': True}
      result = api_client.fetchGuilds(payload)
      return result


  # def getGuildAllycodes(guild_dict):
  #     allycodes = []
  #     g_members = guild_dict[0]['roster']
  #     for g_member in g_members:
  #         try:
  #             allycodes.append(g_member['allyCode'])
  #         except Exception as e:
  #             print("Exception caught: {0}".format(str(e)))
  #             print("Guild member: {0}".format(g_member))
  #             print("Input type: {}".format(type(guild_dict)))
  #             # pprint.pprint(guild_dict)
  #             return ([])
  #     return allycodes


  # Fetch a list of guild member allycodes
  members = getGuild(client, allycode)
  with open('response.json', 'w') as f:
    json.dump(members, f)
  
  # with open('response.json', 'r') as f:
  #   members = json.load(f)
  
  guildResponse = members[0]
  
  
  if myGuild := Guild.objects.get(guildId=guildResponse['id']):
    myGuild.name = guildResponse['name']
    myGuild.desc = guildResponse['desc']
    myGuild.members = guildResponse['members']
    myGuild.status = guildResponse['status']
    myGuild.required = guildResponse['required']
    myGuild.gp = guildResponse['gp']
    myGuild.bannerColor = guildResponse['bannerColor']
    myGuild.bannerLogo = guildResponse['bannerLogo']
    myGuild.message = guildResponse['message']
    print('Guild updated')
  else:
    newGuild = Guild.objects.create(
      guildId = guildResponse['id'],
      name = guildResponse['name'],
      desc = guildResponse['desc'],
      members = guildResponse['members'],
      status = guildResponse['status'],
      required = guildResponse['required'],
      gp = guildResponse['gp'],
      bannerColor = guildResponse['bannerColor'],
      bannerLogo = guildResponse['bannerLogo'],
      message = guildResponse['message']
    )
    print('Guild created')
    
  playersResponse = guildResponse['roster']
  
  all_players = Player.objects.all()
  for player in all_players:
    if player not in playersResponse:
      player.active = False
      player.save()
      
  playersList = [player for player in playersResponse]
  guild = Guild.objects.all()[0]
  # for player in playersList:
  #   player.update({"guild": guild})
    
  # [player.update({"guild": guild}) for player in playersList]
  newPlayersObjs = []
  for player in playersList:
    try: 
      oldPlayer = Player.objects.get(playerId = player['id'])
      oldPlayer.name = player['name']
      oldPlayer.allycode = player['allyCode']
      oldPlayer.level = player['level']
      oldPlayer.gp = player['gp']
      oldPlayer.gpChar = player['gpChar']
      oldPlayer.gpShip = player['gpShip']
      oldPlayer.guildMemberLevel = player['guildMemberLevel']
      oldPlayer.active = True
      oldPlayer.save()
      print(oldPlayer.name)
    except:
      newPlayersObjs.append(Player(
        name = player['name'],
        playerId = player['id'],
        allycode = player['allyCode'],
        level = player['level'],
        gp = player['gp'],
        gpChar = player['gpChar'],
        gpShip = player['gpShip'],
        active = True,
        guildMemberLevel = player['guildMemberLevel'],
        guild = guild
      ))

  objs = Player.objects.bulk_create(newPlayersObjs)
  allycodeList = []
  # # allycodeList = [984519997,911364662,885976194,856572921]
  [allycodeList.append(player['allyCode']) for player in playersList]
  print('Requesting rosters for guild members')
  playersResponse = client.fetchPlayers(allycodeList) 
  with open('players.json', 'w') as f:
    json.dump(playersResponse, f)
  # with open('players.json', 'r') as f:
    # playersResponse = json.load(f)

  Mod.objects.all().delete()
  Skill.objects.all().delete()
  Toon.objects.all().delete()
  ModStat.objects.all().delete()
  Equipped.objects.all().delete()
  
  for player in playersResponse:
    playerObj = Player.objects.get(playerId=player['id'])
    print(f'Import for {playerObj.name}')
    toons = player['roster']
    for toon in toons:
      relic = toon['relic']
 
      if toon['relic']==None or toon['relic']['currentTier']==1:
        relic=0
      else:
        relic=toon['relic']['currentTier']-2
      if toon['primaryUnitStat']==None:
        pus=0
      else:
        pus=toon['primaryUnitStat']
      
      newToonsObj = []

      newToonsObj.append(Toon(
      # Toon.objects.create(
        player = playerObj,
        toonID = toon['id'],
        toonName = toon['defId'],
        nameKey = toon['nameKey'],
        rarity = toon['rarity'],
        toonLevel = toon['level'],
        xp = toon['xp'],
        gp = toon['gp'],
        gearLevel = toon['gear'],
        primaryUnitStat = pus,
        relic = relic,
        combatType = toon['combatType'],
      ))
      objs = Toon.objects.bulk_create(newToonsObj)
      toonObj = Toon.objects.get(toonID=toon['id'])
      print(f'Added toons for {playerObj.name}')
      
      skills = toon['skills']
      newSkillsObj = []
      for skill in skills:
        newSkillsObj.append(Skill(
          toon = toonObj,  
          skillId = skill['id'],
          tier = skill['tier'],
          nameKey = skill['nameKey'],
          isZeta = skill['isZeta'],
          tiers = skill['tiers']
        ))
      objs = Skill.objects.bulk_create(newSkillsObj)
      print(f'Added skills for {playerObj.name}')
      
      equippeds = toon['equipped']
      newEqippedObj = []
      for equipment in equippeds:
        newEqippedObj.append(Equipped(
          toon = toonObj,
          equipmentId = equipment['equipmentId'],
          slot = equipment['slot'],
          nameKey = equipment['nameKey']
        ))
      objs = Equipped.objects.bulk_create(newEqippedObj)
      print(f'Added gear for {playerObj.name}')
      
      mods = toon['mods']
      newModsObj = []
      for mod in mods:
        newModsObj.append(Mod(
          toon = toonObj,
          modId = mod['id'],
          modLevel = mod['level'],
          tier = mod['tier'],
          set = mod['set'],
          pips = mod['pips']
        ))
      objs = Mod.objects.bulk_create(newModsObj)
      print(f'Added mods for {playerObj.name}')
      
      newStatsObj = []
      for mod in mods:
        modObj = Mod.objects.filter(modId=mod['id'])
        modObj = modObj[0]
        ModStat.objects.create(
          mod = modObj,
          statType = 'P',
          unitStat = mod['primaryStat']['unitStat'],
          value = mod['primaryStat']['value']
        )
        sStats = mod['secondaryStat']
        for sStat in sStats:
          newStat = ModStat.objects.create(
            mod = modObj,
            statType = 'S',
            unitStat = sStat['unitStat'],
            roll = sStat['roll'],
            value = sStat['value']
          )
        print(f'Added stats for {playerObj.name}')