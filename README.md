# The World in One Day — 22 November 2026

A newspaper front page summing up the world's news of Sunday
22 November 2026 in a single image.

## The day's news

- **Lead story — Iran strikes U.S. bases in Bahrain again.** On Saturday
  night, Revolutionary Guards hit Sheikh Isa air base and the U.S. Navy's
  Fifth Fleet home at Juffair; sirens sounded across Manama and a civilian
  industrial facility was set on fire. The fourth attack on Bahrain in
  nine days.
- **Kyiv's bridges hit in a 515-missile night.** Russia fired 27 ballistic
  missiles, 84 cruise missiles and 404 drones at Ukraine overnight on
  19–20 November; three bridges over the Dnipro were damaged, at least
  eight people were killed, and missiles and a drone came down in Poland.
- **Kryvyi Rih: child and paramedic killed.** A Russian double-tap strike
  on 20 November killed a seven-year-old boy and a 20-year-old paramedic
  and injured 52 people, on World Children's Day.
- **Also today:** COP31 deadlocked over fossil fuels; a magnitude 6.9
  earthquake shakes Peru's Andes; drones hit a Russian cargo ship in the
  Gulf of Finland; Cyclone Akvan disrupts flights in eastern India;
  Mexico's army captures drug lord "El Chapo Isidro"; the FBI probes an
  apparent hack of its crime database. Sport: India v New Zealand in
  windy Wellington; Pat Cummins keeps Australia's Test captaincy.

Sources: Reuters, AP, BBC, ISW, U.S. Central Command.

## How it works

`main.py` (Python 3.13, standard library only) draws the front page —
masthead, headlines, a stylised night scene over the Gulf, and the day's
stories — with a hand-built 5×7 bitmap font and a pure-stdlib PNG
encoder (zlib + struct). It writes a deterministic 1024×1024 PNG to
`/output/entry.png` with no network access.

Run it:

```sh
python3 main.py
```
