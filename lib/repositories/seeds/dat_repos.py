from .. import repos_db

repositories = [
    {
        "name": "No-Intro",
        "short_name": "nointro",
        "description": "No-Intro is a collection of DATs aimed for video game preservation especialized in cartridge-based and digital systems.",
        "url": "https://wiki.no-intro.org/index.php",
        "icon": "https://www.no-intro.org/favicon.ico",
        "update_script": "lib/nointro/update.py",
        "type": "system"
    },
    {
        "name": "Redump",
        "short_name": "redump",
        "description": "Redump.org is a disc preservation database and internet community dedicated to collecting precise and accurate information about every video game ever released on optical media of any system.",
        "url": "http://redump.org/",
        "icon": "http://redump.org/favicon.ico",
        "update_script": "lib/redump/update",
        "type": "system"
    },
]

# print(repositories_db.get_all())

for repository in repositories:
    repos_db.add_or_update(query=lambda x: x['name'] == repository['name'], new_data=repository)
repos_db.create_index('name')
repos_db.commit()
