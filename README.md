# SCD to IDS Rules (small prototype)

This is a small prototype I built after the interview, to try out the idea
we talked about - generating Zeek/Suricata rules automatically from a
Substation Configuration Description (SCD) file, instead of writing rules
by hand for every device.

I know this is not complete or production-level, it was done in a couple
of days just to test if the idea works and to show that I understood the
feedback from the interview.

## What it does (in short)

1. Reads an SCD (XML) file and finds all the devices (IEDs) and their
   network addresses (IP, MAC).
2. Also finds which device publishes GOOSE messages, and on which
   APPID/MAC.
3. Puts all this into one simple internal list/model (this is basically
   the "asset management" part - know what devices exist before trying
   to detect anything abnormal).
4. From that same list, generates:
   - Suricata rules (`.rules` file)
   - a Zeek script (`.zeek` file)

So the flow is: **SCD file -> asset list -> rules**. I kept these as 3
separate steps/files instead of one big script, because it made more
sense to me after the interview question about parsers/compilers - like
how a compiler first reads code into some internal structure, and only
after that generates the output. Here the "internal structure" is the
asset list, and the "output" is the Suricata/Zeek rules.

## Why Suricata and Zeek are handled separately

They don't work the same way, so I couldn't generate both from one
template:

- Suricata: each rule is one line, like a signature. So for this I just
  generate one rule per condition I care about (e.g. unknown IP, unknown
  GOOSE APPID).
- Zeek: it's more like a small program, not just rules. So instead of
  writing many small rules, I generate one script, and inside that script
  there is a list of the known devices - the script logic itself doesn't
  change between substations, only that list changes.

## Files

```
IDS/
├── sample_data/example.scd     <- sample SCD file (made this myself,
│                                    not a real substation, but same
│                                    structure as a real one)
├── src/
│   ├── parser.py       <- reads the SCD, step 1
│   ├── asset_model.py  <- the asset list / internal structure, step 2
│   ├── rulegen.py       <- generates Suricata + Zeek rules, step 3
│   └── main.py            <- runs everything together
├── output/               <- generated rules end up here
└── tests/
    └── test_parser.py    <- some basic tests, to check the parser
                              actually pulls out the right data
```

## How to run it

```
cd src
python3 main.py ../sample_data/example.scd --out-dir ../output
```

To run the tests:
```
python3 tests/test_parser.py
```

## What I actually checked / didn't check

- I installed Suricata and ran the generated `.rules` file through it
  (`suricata -T`, test mode) just to make sure it's not just
  "rule-looking text" but actually loads without errors. It loaded fine,
  3/3 rules, 0 errors.
- I could NOT test the Zeek script against real Zeek, I didn't have it
  installed/available. So the Zeek script is written based on the syntax
  I found in Zeek's docs, but I have not 100% confirmed it runs. I'm
  being upfront about this instead of pretending it's tested.
- Also the GOOSE part of the Zeek script is left as a comment
  (not active), because I wasn't sure what the real event name is called
  in the Zeek/Malcolm setup for GOOSE messages - didn't want to guess and
  have broken code, so I left it as a placeholder to fill in once I know
  the actual setup.

## What's not done / what I'd do next

- Right now it only reads GOOSE publishers, not who is allowed to
  *receive* them (that needs reading ExtRef data from the SCD, didn't
  get to it).
- Doesn't handle MMS/Report or Sampled Values yet, only GOOSE.
- Would like to try exporting the asset list into NetBox (I read that
  Malcolm already uses NetBox for asset info, but can't fill it
  automatically from an SCD - so this could fill that gap).
- Haven't deployed this on an actual Malcolm/Zeek server yet, only
  tested the rule generation part locally.

This is just a first attempt, happy to extend it further if this is
useful for the actual project.