# mffgear
MFFGear is a Marvel Future Fight (MFF) script that helps in identifying which gear might be useful across your roster.

After a year+ into MFF I started to notice that I was storing a lot of custom gears using up valuable inventory space. I kept telling myself "I'll get back to these later and figure out who to put them on" but I never would and it became a huge PITA managing gear. I created this script to help solve that problem for myself but figured I'd make it available to anyone else if they find themselves in the same boat as me.

Effectively, you pass it a comma delimited set of gear abbreviations and it'll tell you if a characters PVP/PVE optimal gear aligns, sorted by tier, rank, and whether they already have gear on. It has a handful of flags I've added to make usage slightly easier.

```
$ python mffgear.py -h
usage: mffgear.py [-h] [-f <value>] [-m] [-v] [-u] [-d] [-i]

Script for helping find Marvel Future Fight characters to equip gear on.

optional arguments:
  -h, --help            show this help message and exit
  -f <value>, --file <value>
                        The file to use if not "mff.db".
  -m, --merge           Download the latest character DB and merge it with
                        file specified using -f flag.
  -v, --verbose         Prompt for gear updates when listing.
  -u, --update          Update your character DB with changes.
  -d, --defs            Print gear abbreviations
  -i, --init            Setup your characters for the first time.
```

You'll want to learn the gear abbreviations with `-d` to make usage quicker.

```
$ python mffgear.py -d

[+] Gear Abbreviations

{
    "AD": "All Defense",
    "CD": "Cold Damage",
    "CRD": "Critical Damage",
    "CRR": "Critical Rate",
    "DEF": "Ignore Defense",
    "DO": "Dodge",
    "DP": "Damage Proc",
    "FD": "Fire Damage",
    "GB": "Guard Break Immunity",
    "HP": "Max HP",
    "ID": "Ignore Dodge",
    "IP": "Invincible Proc",
    "LD": "Lightning Damage",
    "MD": "Mind Damage",
    "PD": "Poison Damage",
    "RR": "Recovery Rate"
}

[+] CTP Abbreviations

{
    "AUT": "CTP of Authority",
    "DES": "CTP of Destruction",
    "ENR": "CTP of Energy",
    "PAT": "CTP of Patience",
    "RAG": "CTF of Rage",
    "REF": "CTP of Refinement",
    "REG": "CTP of Regeneration",
    "TRA": "CTP of Transcendence"
}
```

To start it off, you can run the `-i` flag to initialize your roster and update it to reflect what you have (tier and gear per character). This will admittedly take a bit of time and you technically can skip it and just show all of the characters as if they were ungeared/default tiers. Additionally, you can use the `-m` flag to download the latest DB file and merge it with your current. While I can't promise I'll always keep it up-to-date, I do plan quite a bit daily and I'm happy to receive pull requests to flush out the existing DB.

```
$ python mffgear.py -m

[!] Downloading latest DB file from https://raw.githubusercontent.com/karttoon/mffgear/master/mff_master.db
[!] Found new gear definitions
[!] Adding new character Juggernaut
[!] Adding new character Sabertooth
[!] Adding new character Warpath
```

I've built 1.0 to use the data from the character ranks according to [erceyazici](https://www.reddit.com/user/erceyazici)'s [Tier List v4.8.2](https://www.reddit.com/r/future_fight/comments/auw0b5/tier_list_v482/) and the PVP/PVE/CTP gears according to [fmv13](https://www.reddit.com/user/fmv13)'s [Character Building Power Book V.4.7](https://www.reddit.com/r/future_fight/comments/akfzgf/character_building_power_book_v47/). These two deserve a TON of credit for all the amazing work they put into these releases for the community.

So what does it look like when you run it? Here is a sample output looking for a custom gear that has Guard Break Immunity (gb), Lightning Damage (ld), and a Invincible Proc (ip):

```
$ python mffgear.py -f kart_mff.db 'gb,ld,ip' -v

[+] Candidate for Gear

[01] [Tier 2 | Rank S | Gear PVP] Thor - GB, LD, IP

[+] Enter the character number to update or Enter to skip: 1

[+] Updating Thor
	[-] Use format "CRR 25" to indicate Crit Rate 25% or "ENR" for CTP of Energy

Slot 1: gb
Slot 2: ld 31
Slot 3: ip 3
```

Here's a slightly more generic search (intended for when I have an Ignore Defense gear with two other good stats that I want to temporarily use). In this case it's search for characters with either PVP or PVE slots matching Crit Damage and Invincible Proc.

```
$ python mffgear.py -f kart_mff.db -v 'crd,ip'

[+] Candidate for Gear

[01] [Tier 2 | Rank S | Gear PVP] Winter Soldier   - GB, CRD, IP
[02] [Tier 2 | Rank S | Gear PVP] Proxima Midnight - GB, CRD, IP
[03] [Tier 2 | Rank S | Gear PVP] Cull Obsidian    - HP, CRD, IP
[04] [Tier 2 | Rank S | Gear PVP] Invisible Woman  - GB, CRD, IP
[05] [Tier 2 | Rank S | Gear PVP] Corvus Glaive    - GB, CRD, IP
[06] [Tier 2 | Rank S | Gear PVP] Doctor Doom      - GB, CRD, IP
[07] [Tier 2 | Rank S | Gear PVP] Thanos           - GB, CRD, IP
[08] [Tier 2 | Rank S | Gear PVP] Magneto          - GB, CRD, IP
[09] [Tier 2 | Rank S | Gear PVP] Stryfe           - GB, CRD, IP
[10] [Tier 2 | Rank A | Gear PVP] Adam Warlock     - GB, CRD, IP
[11] [Tier 2 | Rank A | Gear PVP] Crystal          - GB, CRD, IP
[12] [Tier 2 | Rank A | Gear PVP] Fantomex         - CRD, HP, IP
[13] [Tier 2 | Rank A | Gear PVP] Domino           - CRD, DO, IP
[14] [Tier 2 | Rank B | Gear ALL] Groot            - HP, CRD, IP
[15] [Tier 2 | Rank B | Gear ALL] Falcon           - GB, CRD, IP
[16] [Tier 1 | Rank S | Gear PVP] Nova             - GB, CRD, IP
[17] [Tier 1 | Rank S | Gear PVP] Weapon Hex       - GB, CRD, IP
[18] [Tier 1 | Rank A | Gear PVP] Magik            - GB, CRD, IP
[19] [Tier 1 | Rank A | Gear ALL] Kid Kaiju        - CRD, GB, IP
[20] [Tier 1 | Rank A | Gear PVP] Morgan Le Fay    - GB, CRD, IP
[21] [Tier 1 | Rank A | Gear PVP] Hyperion         - GB, CRD, IP
[22] [Tier 1 | Rank A | Gear PVP] Star-Lord        - CRD, DO, IP
[23] [Tier 1 | Rank A | Gear PVP] Iron Hammer      - GB, CRD, IP
[24] [Tier 1 | Rank A | Gear PVP] Killmonger       - HP, CRD, IP
[25] [Tier 1 | Rank A | Gear PVP] Titania          - HP, CRD, IP
[26] [Tier 1 | Rank B | Gear ALL] Spider-Gwen      - DO, CRD, IP
[27] [Tier 1 | Rank B | Gear ALL] Goliath          - CRD, HP, IP

[+] Already Geared

[28] [Tier 2 | Rank S | Current ] Doctor Strange   - Critical Rate: 22, Guard Break Immunity: 0, Damage Proc: 100
[29] [Tier 2 | Rank S | Current ] Ebony Maw        - Guard Break Immunity: 0, Invincible Proc: 3, Critical Rate: 26
[30] [Tier 1 | Rank B | Current ] Warwolf          - Critical Rate: 20, Invincible Proc: 2, Critical Rate: 13
[31] [Tier 2 | Rank S | Current ] Ant-Man          - Critical Damage: 22, Invincible Proc: 2, Dodge: 14

[+] Enter the character number to update or Enter to skip: 4

[+] Updating Invisible Woman
	[-] Use format "CRR 25" to indicate Crit Rate 25% or "ENR" for CTP of Energy

Slot 1: crd 25
Slot 2: def 12
Slot 3: ip 4
```

When I run the same search again, Invisible Woman will now be listed under "Already Geared":

```
[29] [Tier 2 | Rank S | Current ] Invisible Woman  - Critical Damage: 25, Invincible Proc: 4, Ignore Defense: 12
```

That's about it. I've included my personal DB file (kart_mff.db) if you want to use it as a test.

--
Additional gears added from [Cynicalex](https://www.reddit.com/user/cynicalex) [Cynicalex Master Guides](https://docs.google.com/spreadsheets/d/1H0Hcl9oVZV9gA266xkJAqPv5bD1qwqhC5NeVbLj_-FE/htmlview?sle=true#)
