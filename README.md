# Spellsworn-Ability-Draft-Bot
This project uses the discordpy library to run an "ability draft" for the game Spellsworn using a discord bot.

Users receive a pack of spells, pick a spell, and then pass their pack to the next player.  This process repeats until there are no spells left in the packs.  The bot achieves this by sending each player a private message containing the spells in the pack, then the players send back a message specifying which spell they want.  Once each player has chosen a spell, a new message is sent out to each player with their next pack.

The packs are not completely randomized, each pack is garunteed to have one movement spell and one offensive spell, but the rest of the spells in a pack are completely random.  The two seeded spell slots exist to ensure a balanced and fair draft.
